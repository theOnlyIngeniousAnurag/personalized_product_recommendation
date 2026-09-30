# Personalized Product Recommendation System
## Machine Learning Internship Capstone — Project 3

An end-to-end, production-grade recommendation engine built in Python using Scikit-learn, SciPy, FastAPI, and Streamlit on the authentic Monash FIT5212 S1 2025 dataset.

---

## 🚀 Key Features

- **Multi-Model Recommendation Engine**:
  - **Popularity Baseline**: Fast global ranking ($Rating \times Count$) with minimum interaction threshold ($\ge 5$) for cold users.
  - **Collaborative Filtering**: User-based k-NN with sparse cosine similarity over explicit user-item ratings.
  - **Matrix Factorization**: TruncatedSVD with 20 latent factor components.
  - **Content-Based Filtering**: TF-IDF text vectorization on 201,325 catalog product titles with seed-based cosine matching.
  - **Hybrid Orchestrator**: Balanced weighted combination (50% CF + 30% Content + 20% Popularity) with deterministic cold-start fallback.
- **REST API**: Production FastAPI service (`/recommend/{user_id}`, `/health`, `/`) supporting dynamic model selection.
- **Interactive Web App**: Streamlit dashboard with KPI metrics, exploratory rating/segment tabs, model dropdowns, and score distribution charts.
- **Rigorous Leakage-Controlled Validation**: Non-temporal user-level 80/20 stratified holdout on 745k authentic records.
- **Automated QA**: 20/20 passing Pytest test suite.

---

## 📊 Offline Benchmark Results (1,999 Validation Users)

Evaluated under strict offline holdout (relevance: rating $\ge 4.0$):

| Model | P@5 | R@5 | NDCG@5 | P@10 | R@10 | NDCG@10 | P@20 | R@20 | NDCG@20 | Catalog Coverage | Diversity (1-Jaccard) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Popularity Baseline** | 0.0345 | 0.0040 | 0.0424 | 0.0296 | 0.0069 | 0.0362 | 0.0218 | 0.0098 | 0.0286 | 78 | 0.2489 |
| **Collaborative Filtering (User-kNN)** | **0.1975** | **0.0282** | **0.2116** | **0.1604** | **0.0440** | **0.1812** | **0.1215** | **0.0646** | **0.1481** | **7,259** | **0.9964** |
| **Matrix Factorization (TruncatedSVD)** | 0.1129 | 0.0140 | 0.1207 | 0.0947 | 0.0230 | 0.1054 | 0.0747 | 0.0356 | 0.0882 | 961 | 0.9443 |
| **Content-Based (TF-IDF)** | 0.0713 | 0.0109 | 0.0853 | 0.0466 | 0.0135 | 0.0634 | 0.0327 | 0.0177 | 0.0483 | 947 | 0.9424 |
| **Hybrid Model (50% CF + 30% CB + 20% Pop)** | 0.1611 | 0.0226 | 0.1666 | 0.1393 | 0.0383 | 0.1494 | 0.1090 | 0.0577 | 0.1260 | 5,974 | 0.9581 |

*Note: Temporal validation could not be performed because the authentic FIT5212 dataset contains no legitimate timestamp field.*

---

## 🏗️ Architecture & Project Structure

```text
├── api/
│   └── recommendation_api.py      # FastAPI REST service (/recommend/{user_id}, /health)
├── app/
│   └── streamlit_app.py           # Streamlit Web Analytics & Recommendation Dashboard
├── config/
│   └── config.py                  # Project thresholds, paths, random seeds
├── data/
│   ├── raw/                       # Authentic FIT5212 raw train (parts 1 & 2) and test.csv
│   ├── interim/                   # Zero-leakage train_interactions.csv & val_interactions.csv
│   └── processed/                 # interactions.csv, products.csv, popular_products.csv, users.csv
├── docs/
│   ├── FINAL_PROJECT_REPORT.md    # Master 15-section capstone report
│   ├── TASK_TRACKER.md            # Execution tracker across all phases
│   ├── ML_METHODOLOGY.md          # Machine learning algorithms & mathematics
│   ├── EVALUATION_AND_ERROR_ANALYSIS.md # Evaluation metrics & diagnostic specs
│   └── SYSTEM_ARCHITECTURE.md     # Software architecture & component contracts
├── outputs/
│   ├── reports/                   # evaluation_results.json, error_analysis.json, text reports
│   └── tables/                    # model_comparison_table.csv, user_segment_summary.csv
├── src/
│   ├── analysis/                  # user_segment_analysis.py (Empirical activity tertiles)
│   ├── data/                      # preprocess_data.py, split_data.py, acquire_data.py
│   ├── evaluation/                # evaluate_recommendations.py (Multi-model evaluation runner)
│   ├── models/                    # popularity, collaborative, matrix factorization, content, hybrid
│   ├── recommendation/            # recommendation_engine.py (Canonical Unified Engine)
│   └── utils/                     # data_utils.py
└── tests/
    ├── test_data_foundation.py    # Schema, domain, leakage, and registry tests
    ├── test_models_and_api.py     # All 5 models, metric math, API endpoints, cold-start
    └── test_recommendation.py     # RecommendationEngine interface tests
```

---

## ⚡ Quickstart

### 1. Run Tests
```bash
python3 -m pytest -v
```

### 2. Run Comprehensive Model Evaluation
```bash
python3 src/evaluation/evaluate_recommendations.py
```

### 3. Run User Segment Analysis
```bash
python3 src/analysis/user_segment_analysis.py
```

### 4. Launch FastAPI REST Service
```bash
uvicorn api.recommendation_api:app --host 0.0.0.0 --port 8000
```
Query recommendations:
```bash
curl "http://localhost:8000/recommend/1813?n=5&model=hybrid"
```

### 5. Launch Streamlit Dashboard
```bash
streamlit run app/streamlit_app.py --server.port 3000
```
Visit `http://localhost:3000` to interact with the dashboard.