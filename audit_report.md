# Project 3 — Personalized Product Recommendation
## Repository Audit Report

---

### 1. Executive Summary

This audit report provides an exhaustive, code-level assessment of the imported repository for **Machine Learning Internship Capstone — Project 3: Personalized Product Recommendation Model** (imported from GitHub repository `theOnlyIngeniousAnurag/personalized_product_recommendation`).

The audit was conducted strictly under **Zero-Modification / Audit-Only rules**. No existing code, dataset, configuration, or environment file was modified, moved, renamed, or deleted.

#### High-Level Audit Findings
1. **Architecture & Scope**: The codebase establishes a coherent modular structure across data processing, standalone recommender models, a hybrid recommendation engine, a FastAPI service, a Streamlit dashboard, offline evaluation metrics, and basic documentation.
2. **Missing Essential Data Files (Blocker)**: Neither the raw datasets (`data/raw/train.csv`, `data/raw/test.csv`) nor the core processed interaction tables (`data/processed/interactions.csv`, `data/processed/products.csv`) are present in the repository. As a result, the preprocessing scripts, model training scripts, recommendation engine, FastAPI service, Streamlit app, and test suites will all fail at runtime with `FileNotFoundError` upon initial execution without data restoration.
3. **Data Source & Requirement Misalignment**:
   - The official requirements demand interaction data spanning **views, clicks, carts, and purchases**. The repository uses the Monash University FIT5212 S1 2025 Recommender Challenge Amazon rating dataset, which contains **only explicit ratings (1–5)**, votes, and helpful votes. Views, clicks, carts, and purchases are absent.
   - The official requirements strictly mandate a **time-based validation split**. The underlying dataset lacks timestamps entirely. The author attempted an offline 80/20 user-level random holdout split (`train_test_split`), which is explicitly non-compliant with the time-based validation mandate.
4. **Model Architecture Inconsistencies & Fracturing**:
   - A standalone Matrix Factorization script exists (`src/models/matrix_factorization.py` using TruncatedSVD), but it is completely orphaned. It is never integrated into `RecommendationEngine`, `recommendation_api.py`, `streamlit_app.py`, or `evaluate_recommendations.py`.
   - The production engine (`src/recommendation/recommendation_engine.py`) implements a 50% Collaborative (User-kNN) + 30% Content-Based (TF-IDF) + 20% Popularity hybrid.
   - The Streamlit application (`app/streamlit_app.py`) bypasses `RecommendationEngine` completely and re-implements an ad-hoc hybrid of 70% Content + 30% Popularity, omitting Collaborative Filtering entirely.
   - The evaluation script (`src/evaluation/evaluate_recommendations.py`) evaluates an ad-hoc seed-based content + popularity heuristic rather than the actual `RecommendationEngine` hybrid or Collaborative/Matrix Factorization models.
5. **Evaluation Placeholders**: The evaluation report (`outputs/reports/evaluation_report.txt`) contains unpopulated placeholders (`[INSERT VALUE]`) for Precision@10, Recall@10, NDCG@10, and RMSE.
6. **User Segment Collapse**: The user segmentation script divides users into Low (<3), Medium (3–10), and High (>10) interactions. Because the processed dataset contains heavily filtered active users (mean interactions = 373), 1,999 out of 2,000 users fall into "High Activity", 1 user into "Medium", and 0 into "Low", collapsing the analysis. Furthermore, recommendation quality is never evaluated across segments.
7. **Environment & Dependency Defects**: `requirements.txt` contains a syntax typo on line 16 (`pytestok` instead of `pytest`), and packages are unpinned. `docs/project_architecture.md` contains a filename typo (`api_documentation.mdv`).

---

### 2. Official Project Requirements

The official internship specification serves as the absolute benchmark for this audit:

| Requirement ID | Specification Requirement | Detailed Criterion |
|---|---|---|
| **REQ-01** | User-Item Interaction Data | Prepare interaction data from views, clicks, carts, and purchases. |
| **REQ-02** | Baseline Model | Create a baseline such as popularity-based recommendations. |
| **REQ-03** | Core Personalized Model | Build collaborative filtering OR matrix-factorization-based recommendations. |
| **REQ-04** | Content-Based Fallback | Add item metadata to create a content-based fallback, particularly for new products / cold-start situations. |
| **REQ-05** | Top-K Ranking Evaluation | Evaluate using Precision@K, Recall@K, and NDCG@K. |
| **REQ-06** | Validation Strategy | Evaluation must use a time-based validation split. |
| **REQ-07** | Recommendation API | Create a simple recommendation API. |
| **REQ-08** | User Segment Analysis | Analyze recommendations for different user segments. |
| **REQ-TECH** | Technology Stack | Python for data/modeling, Git/GitHub, Streamlit/API for deployment. No JavaScript/Node migration. |

---

### 3. Repository Snapshot

- **Repository Root**: `/`
- **Current Commit State**: Imported from `theOnlyIngeniousAnurag/personalized_product_recommendation`
- **Total Tracked Files**: 38 files
- **Python Version in Environment**: Python 3.10.12
- **Primary Languages**: Python, Markdown, Plain Text
- **Existing Directories**:
  - `api/` (FastAPI backend service)
  - `app/` (Streamlit frontend application)
  - `config/` (Project path and hyperparameter configuration)
  - `data/` (Data store; contains `processed/`, missing `raw/`)
  - `docs/` (Architecture, methodology, and API documentation)
  - `outputs/` (Output figures, tables, and reports)
  - `src/` (Core ML pipeline: analysis, data, evaluation, models, recommendation, utils)
  - `tests/` (Pytest unit test suite)

---

### 4. Complete Repository Inventory

| File Path | Functional Purpose | Actually Referenced? | Functional Status | Redundancy / Notes |
|---|---|---|---|---|
| `/.gitignore` | Specifies git exclusions (`.venv`, `__pycache__`, etc.) | Yes (Git) | Functional | Does not explicitly ignore `data/raw/` though data was not committed |
| `/README.md` | Repository overview, methodology summary, dataset description | User facing | Functional | Mentions FIT5212 S1 2025 dataset and directory structure |
| `/requirements.txt` | Python dependency manifest | Yes (pip) | ⚠️ Defective | Line 16 has typo `pytestok`; unpinned dependencies |
| `/config/config.py` | Central configuration of paths, thresholds, and seeds | Yes (partially) | Functional | Defines `TOP_K=10`, `MIN_INTERACTIONS=5`, `RATING_THRESHOLD=4`, file paths |
| `/api/recommendation_api.py` | FastAPI application serving `/recommend/{user_id}` and `/health` | Standalone app | ⚠️ Runtime Error | Imports `RecommendationEngine`, which fails because `interactions.csv` is missing |
| `/app/streamlit_app.py` | Interactive dashboard for recommendations and analytics | Standalone app | ⚠️ Runtime Error | Re-implements separate recommendation logic; crashes due to missing data |
| `/data/processed/popular_products.csv` | Precomputed product popularity ranks (33,074 rows) | Yes | Functional | Committed artifact; contains popularity scores and ranks |
| `/data/processed/users.csv` | Precomputed user summary statistics (2,001 rows) | Yes | Functional | Committed artifact; lists interaction counts and average ratings |
| `/data/processed/user_segment_summary.csv` | User segment aggregation table (2 rows) | Yes | Functional | Shows 1,999 High Activity vs 1 Medium Activity user |
| `/data/processed/user_segment_interactions.png`| Bar chart of average interactions per segment | Output asset | Static artifact | Visual output from analysis run |
| `/data/processed/user_segment_ratings.png` | Bar chart of average rating per segment | Output asset | Static artifact | Visual output from analysis run |
| `/docs/api.md` | API documentation with endpoint schemas and examples | User facing | Functional | Well structured, but response payloads differ slightly from code |
| `/docs/methodology.md` | Detailed modeling and evaluation methodology document | User facing | Functional | Comprehensive; honestly admits missing timestamps and ratings limitation |
| `/docs/project_architecture.md` | Project architecture and directory map | User facing | ⚠️ Minor Defect | Line 61 contains filename typo `api_documentation.mdv` |
| `/outputs/figures/popular.png` | Plot of top popular products | Static asset | Static artifact | Pre-generated plot |
| `/outputs/figures/rec_score.png` | Plot of recommendation scores | Static asset | Static artifact | Pre-generated plot |
| `/outputs/figures/recommen_ana.png` | Plot of recommendation analysis | Static asset | Static artifact | Pre-generated plot |
| `/outputs/reports/data_analysis_report.txt` | Text summary of dataset statistics and rating distribution | User facing | Functional | Accurately describes dataset of 745,889 ratings |
| `/outputs/reports/evaluation_report.txt` | Top-K and RMSE evaluation methodology and report | User facing | ⚠️ Incomplete | Contains unpopulated `[INSERT VALUE]` placeholders for metrics |
| `/outputs/reports/model_comparison_report.txt`| Comparative analysis of all 5 recommendation approaches | User facing | Functional | Conceptual comparison text |
| `/outputs/tables/popular_prod_table.png` | Rendered table image of popular products | Static asset | Static artifact | Pre-generated visual |
| `/outputs/tables/product_recomm.png` | Rendered table image of product recommendations | Static asset | Static artifact | Pre-generated visual |
| `/outputs/tables/rec_prod_table.png` | Rendered table image of recommendations | Static asset | Static artifact | Pre-generated visual |
| `/src/analysis/user_segment_analysis.py` | Segments users by activity count and exports charts | Standalone script | ⚠️ Runtime Error | Reads `data/processed/interactions.csv` which is missing; 99.95% segment collapse |
| `/src/data/inspect_dataset.py` | Inspects first 5,000 rows of train/test CSVs | Standalone script | ⚠️ Runtime Error | Fails because `data/raw/train.csv` does not exist |
| `/src/data/analyze_dataset.py` | Computes full shapes, nulls, unique values for raw data | Standalone script | ⚠️ Runtime Error | Fails because `data/raw/train.csv` does not exist |
| `/src/data/preprocess_data.py` | Cleans raw train data, removes duplicates, outputs interactions.csv | Pipeline script | ⚠️ Runtime Error | Fails because `data/raw/train.csv` does not exist |
| `/src/data/create_entities.py` | Builds user and product summary tables from interactions | Pipeline script | ⚠️ Runtime Error | Reads `data/processed/interactions.csv` (missing) |
| `/src/evaluation/evaluate_recommendations.py`| Evaluates Precision@10, Recall@10, NDCG@10 via user split | Evaluation script | ⚠️ Runtime Error | Reads `interactions.csv` (missing); evaluates toy model instead of main engine |
| `/src/models/popularity_model.py` | Computes rating * count popularity score | Model script | ⚠️ Runtime Error | Reads `data/processed/products.csv` which is missing |
| `/src/models/collaborative_filtering.py` | User-based k-NN collaborative filtering via sparse matrix | Model script | ⚠️ Runtime Error | Reads `interactions.csv` (missing); standalone demo only |
| `/src/models/matrix_factorization.py` | TruncatedSVD matrix factorization (20 components) | Model script | ⚠️ Disconnected | Reads `interactions.csv` (missing); never integrated into engine or API |
| `/src/models/content_based.py` | TF-IDF on product name + cosine similarity | Model script | ⚠️ Runtime Error | Reads `products.csv` (missing); standalone single-product demo |
| `/src/models/hybrid_recommendation.py` | Standalone hybrid prototype (50% CF + 30% Content + 20% Pop) | Prototype script | ⚠️ Redundant | Prototype predecessor of `recommendation_engine.py` |
| `/src/recommendation/recommendation_engine.py`| Core production class combining CF, Content, Popularity | Core Engine | ⚠️ Runtime Error | Well written, but fails at init due to missing `interactions.csv` and `products.csv` |
| `/src/utils/data_utils.py` | Utility helpers (`load_csv`, `save_csv`, column checks) | Helper module | Functional | Tested in `test_recommendation.py` |
| `/tests/test_recommendation.py` | Pytest suite with 6 test functions | Test suite | ⚠️ Execution Error| Cannot execute: `pytest` not in env (typo in reqs), missing `interactions.csv` |

---

### 5. Current Architecture Reconstruction

The diagram below reflects the **ACTUAL** architecture as verified from code, highlighting component isolation, missing files, and fragmented pipelines:

```
[ MISSING: data/raw/train.csv & test.csv ]
                    │
                    ▼  (Crashes on execution: FileNotFoundError)
         src/data/preprocess_data.py
                    │
                    ▼  (File NOT in repo)
       [ data/processed/interactions.csv ] ──┐
                    │                        │
                    ▼                        │
         src/data/create_entities.py         │
          │                       │          │
          ▼                       ▼          │
  data/processed/users.csv   [ products.csv ]│ (File NOT in repo)
     (Committed, 2001 rows)       │          │
                                  ▼          │
                     src/models/popularity   │
                                  │          │
                                  ▼          │
               data/processed/popular_products.csv
                       (Committed, 33074 rows)
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
src/models/collaborative   src/models/matrix_fact    src/models/content_based
(Standalone script only)   (TruncatedSVD - ORPHANED) (Standalone script only)
         │                        │                        │
         └────────────────┐       │ (Never integrated)     │
                          ▼       ▼                        ▼
               src/recommendation/recommendation_engine.py
               (Hybrid: 50% CF + 30% Content + 20% Pop)
               (CANDIDATE RESTRICTION: Only Top 1000 popular items)
                          │
         ┌────────────────┴────────────────┐
         │                                 │
         ▼                                 ▼
api/recommendation_api.py         [ app/streamlit_app.py ]
(FastAPI - uses Engine)           (Bypasses Engine! Re-implements
                                   70% Content + 30% Pop; NO CF!)

====================== DISCONNECTED PIPELINES ======================

src/evaluation/evaluate_recommendations.py
  ├── Split: Random 80/20 per user (train_test_split) -> NOT TIME-BASED
  ├── Evaluated Model: Toy seed content + 0.2*pop heuristic
  └── Disconnected from: RecommendationEngine, SVD, and CF models

src/analysis/user_segment_analysis.py
  ├── Segments: Low (<3), Medium (3-10), High (>10)
  ├── Reality: 1,999 High, 1 Medium, 0 Low (99.95% collapse)
  └── Evaluates: Only interaction counts & ratings; NO recommendations evaluated
```

---

### 6. Data Pipeline Audit

#### 6.1 Dataset Sources and Availability
- **Declared Source**: The README and `docs/methodology.md` cite the Kaggle Monash University FIT5212 S1 2025 Recommender System Challenge dataset, derived from Amazon reviews.
- **Physical Availability**:
  - `data/raw/train.csv`: **MISSING** (Not present in repository).
  - `data/raw/test.csv`: **MISSING** (Not present in repository).
  - `data/processed/interactions.csv`: **MISSING** (Referenced by 7 files, but not committed).
  - `data/processed/products.csv`: **MISSING** (Referenced by 5 files, but not committed).
  - `data/processed/users.csv`: **PRESENT** (2,001 rows, 44 KB).
  - `data/processed/popular_products.csv`: **PRESENT** (33,074 rows, 1.96 MB).
- **Reproducibility**: There is no automated download script, Kaggle API downloader, or synthetic data generator. The pipeline cannot be re-run from scratch without manually acquiring `train.csv`.

#### 6.2 Schema & Entities
From `src/data/preprocess_data.py` (lines 27–36), the raw schema read from `train.csv` is:
- `user_id` (Identifier, cast to string)
- `product_id` (Identifier, cast to string)
- `product_name` (Text title of product)
- `rating` (Float/Integer, 1.0 to 5.0)
- `votes` (Numeric, community votes)
- `helpful_votes` (Numeric, helpfulness count)

**Entity Comparison**:
- Users: 2,001 unique users in `users.csv`.
- Products: 33,074 products with $\ge 5$ interactions in `popular_products.csv` (reports state 201,325 unique products originally).
- Interaction counts: 745,889 claimed in reports, but raw files are omitted.

---

### 7. User-Item Interaction Audit

#### 7.1 Interaction Types (Requirement Gap)
- **Official Requirement REQ-01**: Prepare user-item interaction data from **views, clicks, carts, and purchases**.
- **Repository Reality**: The project uses **only explicit ratings** ($1.0 \le \text{rating} \le 5.0$).
- **Evidence**:
  - `src/data/preprocess_data.py` lines 27–36 select `["user_id", "product_id", "product_name", "rating", "votes", "helpful_votes"]`.
  - There are no event type columns (`event_type`, `action`, `interaction_type`).
  - Views, clicks, carts, and purchases are neither individually represented, nor combined, nor weighted. They are **completely unavailable** in the chosen Kaggle dataset.
- **Documentation Acknowledgment**: `docs/methodology.md` line 288 honestly states: *"Second, the available interactions are primarily explicit ratings rather than separate event types such as views, clicks, carts, and purchases."*

#### 7.2 Aggregation and Deduplication
- `src/data/preprocess_data.py` lines 44–46:
  ```python
  df = df.drop_duplicates(subset=["user_id", "product_id"])
  ```
  Duplicate user-product interactions are dropped rather than aggregated. If multiple reviews existed, only the first occurrence was retained.

---

### 8. Preprocessing Audit

#### 8.1 Data Cleaning Logic
In `src/data/preprocess_data.py`:
- **Missing Value Handling**:
  - Rows with null `user_id`, `product_id`, or `rating` are dropped (`dropna(subset=...)`).
  - `product_name` nulls filled with `"Unknown Product"`.
  - `votes` and `helpful_votes` nulls filled with `0`.
- **Type Coercion**:
  - `user_id` and `product_id` cast to `str`.
  - `rating`, `votes`, `helpful_votes` coerced via `pd.to_numeric(..., errors="coerce")`.
- **Domain Validation**:
  - Ratings filtered to strictly $[1, 5]$ (`(df["rating"] >= 1) & (df["rating"] <= 5)`).
- **Weaknesses**:
  - No user/item minimum support filtering (k-core pruning) is done during preprocessing. This means sparse users and single-interaction items remained in `interactions.csv`.
  - No text normalization (lowercasing, punctuation stripping) is applied at the preprocessing stage; text preprocessing is deferred to the TF-IDF vectorizers in model files.

---

### 9. Popularity Baseline Audit

#### 9.1 Baseline Formulation
- **File**: `src/models/popularity_model.py`
- **Minimum Threshold**: `MIN_INTERACTIONS = 5` (line 33). Products with fewer than 5 interactions are excluded from the popularity pool.
- **Scoring Function**:
  $$\text{popularity\_score} = \text{average\_rating} \times \text{interaction\_count}$$
  (lines 48–51).
- **Ranking**: Sorted descending by `popularity_score`.
- **Output Artifact**: Pre-computed and saved to `data/processed/popular_products.csv`.
- **Strengths**:
  - Simple, robust baseline.
  - Correctly pre-filtered for low-support items.
- **Weaknesses**:
  - The multiplication of raw average rating and interaction count is dominated by interaction count (e.g., an item with 250 interactions and 4.0 rating scores 1,000, whereas an item with 50 interactions and 5.0 rating scores 250). This is essentially a count-weighted rating, which is standard for popularity.
  - Lacks time-decay: No recency weighting is applied because timestamps do not exist.
  - The baseline model is used as a fallback for cold users, but it is not evaluated independently side-by-side against personalized models in `outputs/reports/evaluation_report.txt`.

---

### 10. Collaborative Filtering / Matrix Factorization Audit

The project implements **both** Collaborative Filtering and Matrix Factorization in standalone scripts, satisfying the "collaborative filtering OR matrix factorization" requirement in theory, but with major architectural disconnects.

#### 10.1 Collaborative Filtering
- **File**: `src/models/collaborative_filtering.py`
- **Methodology**: User-based Collaborative Filtering using Nearest Neighbors (`sklearn.neighbors.NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=6)`).
- **Matrix Construction**:
  - Builds a SciPy CSR sparse matrix of shape $(\text{users} \times \text{products})$ populated with explicit ratings (`float32`).
  - Correctly maps arbitrary IDs to integer indices via `user_to_index` and `product_to_index`.
- **Candidate Scoring**:
  - For a target user, retrieves the 5 nearest neighbor users ($k=6$, excluding self).
  - For each neighbor, calculates similarity $s = 1 - \text{cosine\_distance}$.
  - Accumulates candidate score: $\sum s \times \text{rating}$.
  - Excludes products the target user has already rated.
- **Cold-Start Handling**: Fails if target user has no interactions (index error or zero similarity vector).
- **Integration**: Re-implemented inside `RecommendationEngine.collaborative_scores()`.

#### 10.2 Matrix Factorization
- **File**: `src/models/matrix_factorization.py`
- **Methodology**: Truncated SVD (`sklearn.decomposition.TruncatedSVD(n_components=20, random_state=42)`).
- **Latent Dimensions**: 20 components.
- **Prediction Formula**:
  $$\hat{R}_{\text{user}} = U_{\text{user}} \times V^T$$
  where $U$ is the user factor matrix and $V^T$ is `svd.components_`.
- **Item Masking**: Interacted items are explicitly masked to $-\infty$ (`predicted_scores[list(already_interacted)] = -np.inf`).
- **Mathematical Flaw in Implementation**:
  - Applying `TruncatedSVD` directly to a sparse user-item matrix treats **all unobserved entries as a rating of 0.0**.
  - In explicit rating systems (ratings 1 to 5), an unobserved item does not mean a rating of 0; it means "unrated". Standard SVD without missing-value imputation or ALS (Alternating Least Squares) / FunkSVD biases the latent space toward 0.
- **CRITICAL ARCHITECTURAL GAP**:
  - `matrix_factorization.py` is a **standalone script only**.
  - It is **never saved as a serialized artifact** (`.joblib` or `.pkl`).
  - It is **never imported or utilized** in `RecommendationEngine`, `recommendation_api.py`, `streamlit_app.py`, or `evaluate_recommendations.py`.
  - It is an orphaned proof-of-concept.

---

### 11. Content-Based Fallback Audit

#### 11.1 Metadata Used
- **Source Feature**: `product_name` **only**.
- **Missing Metadata**: Categories, brands, product descriptions, prices, specifications, and keywords are **absent**.
- **Feature Pipeline**:
  - Missing names filled with `"Unknown Product"`.
  - Text lowercased: `products["product_text"] = products["product_name"].astype(str).str.lower()`.
  - Vectorization: `TfidfVectorizer(stop_words="english", max_features=30000)`.
  - Metric: Cosine similarity (`cosine_similarity`).

#### 11.2 Seeding & Candidate Retrieval
In `src/recommendation/recommendation_engine.py` (lines 326–388):
- Takes the user's top 5 highest-rated products from history as seeds.
- Computes cosine similarity between each seed and the entire catalog's TF-IDF matrix.
- Extracts the top 50 most similar candidates per seed using `np.argpartition`.
- Candidate score is the maximum similarity score across all seeds.

#### 11.3 Cold-Start Item Fallback Limitation (CRITICAL FLAW)
- **Requirement REQ-04**: Add item metadata to create a content-based fallback, **particularly for new products / cold-start situations**.
- **Flaw in `recommendation_engine.py` (lines 460–469)**:
  ```python
  popular_candidates = self.popular_products.head(1000)
  candidates = set(popular_candidates["product_id"])
  candidates -= history
  ```
  The candidate pool is **strictly restricted to the top 1,000 items in `popular_products.csv`**!
  - Because `popular_products.csv` requires $\ge 5$ interactions, **a new product with 0 interactions is NOT in `popular_products.csv`**.
  - Therefore, even though the content-based TF-IDF vectorizer could compute similarity for a brand-new item, **the candidate filter eliminates all new products before content scoring occurs**!
  - The content-based component cannot function as a new-product cold-start fallback under the current implementation.

---

### 12. Recommendation Generation Audit

#### 12.1 Hybrid Combination Logic
In `src/recommendation/recommendation_engine.py`:
- **Components**:
  - $S_{\text{collab}}$: User-kNN collaborative score (min-max normalized to $[0, 1]$).
  - $S_{\text{content}}$: Seed-based TF-IDF cosine similarity (min-max normalized to $[0, 1]$).
  - $S_{\text{pop}}$: Popularity score combining average rating and interaction count (min-max normalized to $[0, 1]$).
- **Weighting Formula**:
  $$\text{Score}_{\text{hybrid}} = 0.50 \times S_{\text{collab}} + 0.30 \times S_{\text{content}} + 0.20 \times S_{\text{pop}}$$
- **Deduplication / Seen Items**: Interacted items are explicitly removed (`candidates -= history`).
- **Cold User Fallback**: If user has no history (`not history`), returns top $N$ popular products:
  ```python
  if not history:
      recommendations = self.popular_products.head(n).copy()
      recommendations["recommendation_reason"] = "Popular products for new user"
      return recommendations
  ```

#### 12.2 Architectural Disconnect Between Engine and Apps
1. **API (`api/recommendation_api.py`)**: Uses `RecommendationEngine.recommend(user_id, n=n)`. Compliant with the 50/30/20 hybrid logic.
2. **Streamlit App (`app/streamlit_app.py`)**:
   - Does **NOT** import or call `RecommendationEngine`.
   - Re-implements its own `generate_recommendations()` function (lines 156–350).
   - Weights: **70% Content + 30% Popularity** (`0.70 * content + 0.30 * popularity`).
   - **Collaborative Filtering is completely absent from the Streamlit UI**!
3. **Evaluation Script (`src/evaluation/evaluate_recommendations.py`)**:
   - Does **NOT** import or evaluate `RecommendationEngine`.
   - Re-implements an ad-hoc combination of Seed Content + 0.2 * Popularity Rank.

---

### 13. Evaluation Audit

#### 13.1 Metrics Implemented
In `src/evaluation/evaluate_recommendations.py` (lines 236–314):
- **Precision@K**:
  $$\text{Precision@K} = \frac{|\text{Recommended}_{1:K} \cap \text{Relevant}|}{K}$$
- **Recall@K**:
  $$\text{Recall@K} = \frac{|\text{Recommended}_{1:K} \cap \text{Relevant}|}{|\text{Relevant}|}$$
- **NDCG@K**:
  $$\text{DCG@K} = \sum_{i=1}^K \frac{\mathbb{I}(\text{item}_i \in \text{Relevant})}{\log_2(i + 1)}, \quad \text{IDCG@K} = \sum_{i=1}^{\min(|\text{Relevant}|, K)} \frac{1}{\log_2(i + 1)}$$
  $$\text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$

#### 13.2 Relevance Definition
- Explicit ratings $\ge 4.0$ in the held-out set are treated as binary relevant items (`validation_data[validation_data["rating"] >= 4]`).
- Ratings $< 4.0$ are treated as non-relevant.

#### 13.3 Audit Findings & Critical Deficiencies
1. **Unpopulated Report**: `outputs/reports/evaluation_report.txt` (lines 112–114) literally contains raw placeholders:
   ```text
   Metric | Score
   Precision@10 | [INSERT VALUE]
   Recall@10 | [INSERT VALUE]
   NDCG@10 | [INSERT VALUE]
   ...
   RMSE = [INSERT KAGGLE SCORE]
   ```
   No verifiable offline benchmark numbers are recorded in the repository.
2. **Wrong Model Evaluated**: `evaluate_recommendations.py` evaluates an ad-hoc heuristic script, **not** the `RecommendationEngine` hybrid model, not Collaborative Filtering, and not Matrix Factorization.
3. **Truncated Evaluation**: Line 362 caps evaluated users at 1,000 (`if evaluated_users >= 1000: break`), omitting half the user population.
4. **Data Leakage in Vectorizer**: Line 132 fits `TfidfVectorizer` on all products in `products.csv`, which includes products present in the validation set.

---

### 14. Time-Based Validation Audit

#### 14.1 Requirement Check
- **Official Requirement REQ-06**: *"Evaluation must use a time-based validation split."*
- **Instruction Directive**: *"A random train/test split does NOT count as satisfying the time-based validation requirement. If only random splitting exists: mark the requirement as NOT SATISFIED."*

#### 14.2 Code Evidence
In `src/evaluation/evaluate_recommendations.py` lines 37–50:
```python
for user_id, user_data in data.groupby("user_id"):
    if len(user_data) >= 2:
        train_part, validation_part = train_test_split(
            user_data,
            test_size=0.20,
            random_state=42
        )
        train_data.append(train_part)
        validation_data.append(validation_part)
```
- **Finding**: The project performs a **random 80/20 train/test split per user** using `sklearn.model_selection.train_test_split`.
- **Root Cause**: The raw Kaggle dataset has no timestamp column (`timestamp`, `created_at`, `unix_time`).
- **Audit Assessment**: **⚠️ NOT SATISFIED (NON-COMPLIANT)**.
- While `docs/methodology.md` acknowledges this data limitation, from a formal internship grading standpoint, the hard requirement for a time-based validation split is unfulfilled.

---

### 15. Recommendation API Audit

#### 15.1 Framework & Implementation
- **File**: `api/recommendation_api.py`
- **Framework**: FastAPI with Uvicorn.
- **Endpoints**:
  1. `GET /`: Returns service metadata, status, model name, and weights.
  2. `GET /recommend/{user_id}?n=10`:
     - Validates $1 \le n \le 50$.
     - Calls `engine.recommend(user_id=user_id, n=n)`.
     - Converts `NaN` values to `None` for valid JSON output.
     - Returns JSON with `user_id`, `number_of_recommendations`, and record list.
     - Catches exceptions and raises `HTTPException(status_code=500)`.
  3. `GET /health`: Returns `{"status": "healthy", "recommendation_engine": "loaded"}`.

#### 15.2 Deficiencies & Verification
- **Runtime Execution**: Fails at initialization on line 43 (`engine = RecommendationEngine()`) because `RecommendationEngine` tries to load `data/processed/interactions.csv` and `data/processed/products.csv`, which do not exist.
- **Documentation Mismatch**: `docs/api.md` states `GET /` returns `{"message": "Recommendation API is running"}`. In reality, code returns an extended object with `status`, `model`, and `weights`.
- **Response Format**: Well-designed JSON response with product attributes, scores, and recommendation reasons.

---

### 16. Streamlit / Application Audit

#### 16.1 UI Design & Structure
- **File**: `app/streamlit_app.py`
- **Page Config**: Wide layout, title "🛍️ Personalized Product Recommendation System".
- **Sidebar**: User ID input (default `"1813"`), recommendation slider (5–20), "Generate Recommendations" primary button.
- **Metrics Bar**: Total Users, Products, Interactions.
- **Analytics Tabs**:
  1. *Rating Analysis*: Rating frequency bar chart, Average / Max / Min rating metrics.
  2. *User Segments*: User counts by activity level, average rating by segment, summary dataframe.
  3. *Popular Products*: Top 10 popular products bar chart and full dataframe.
- **Output Section**: Recommendation results table with rank, product name, score, and score distribution chart.

#### 16.2 Critical Deficiencies
1. **Broken Data Dependencies**: Line 41 crashes on launch with `FileNotFoundError: data/processed/interactions.csv`.
2. **Missing Collaborative Filtering**: As noted in Section 12, the Streamlit app calculates recommendations using only **Content (70%) + Popularity (30%)**. Collaborative Filtering is completely omitted from the UI code.
3. **Type Coercion Bug in User Search**:
   Line 693 converts user input to integer: `user_id_numeric = int(user_id)`.
   Line 727 queries: `user_history = interactions[interactions["user_id"] == user_id_numeric]`.
   However, `preprocess_data.py` explicitly converted `user_id` to string (`df["user_id"].astype(str)`). Comparing integer against string series results in an empty match, causing known users to be erroneously flagged as new users!

---

### 17. User Segment Analysis Audit

#### 17.1 Script Implementation
- **File**: `src/analysis/user_segment_analysis.py`
- **Segmentation Criteria**:
  - Low Activity: $< 3$ interactions
  - Medium Activity: $3 \le \text{interactions} \le 10$
  - High Activity: $> 10$ interactions
- **Charts Generated**:
  - `data/processed/user_segment_interactions.png`
  - `data/processed/user_segment_ratings.png`

#### 17.2 Critical Audit Finding: 99.95% Segment Collapse
Inspection of the generated output file `data/processed/user_segment_summary.csv` reveals:
```csv
segment,users,average_interactions,average_rating,average_products,average_votes
High Activity,1999,373.13,4.17,373.13,2764.40
Medium Activity,1,4.00,4.25,4.00,4.00
```
- **High Activity**: 1,999 users (99.95% of the user base).
- **Medium Activity**: Exactly 1 user (0.05%).
- **Low Activity**: Exactly 0 users (0.00%).
- **Why this occurred**: The underlying dataset was pre-filtered to dense users (average 373 reviews per user). Hardcoding threshold boundaries at 3 and 10 was inappropriate for this dataset's distribution.
- **Requirement Gap on Recommendations**: The official requirement states: *"Analyze recommendations for different user segments."* The script only computes descriptive statistics on interaction counts and ratings. It **never analyzes recommendation performance, accuracy, or score distribution across segments**.

---

### 18. Testing Audit

#### 18.1 Test Inventory
- **File**: `tests/test_recommendation.py` (76 lines)
- **Functions**:
  1. `test_load_interactions()`: Verifies `interactions.csv` loads into a non-empty DataFrame.
  2. `test_required_columns()`: Checks for `user_id`, `product_id`, `product_name`, `rating`.
  3. `test_unique_users()`: Asserts unique user count $> 0$.
  4. `test_recommendation_engine()`: Instantiates `RecommendationEngine` and asserts recommendations $\le 5$.
  5. `test_recommendation_columns()`: Checks returned dataframe contains expected column names.
  6. `test_recommendation_not_empty()`: Asserts recommendations returned $> 0$.

#### 18.2 Verification Attempt & Execution Status
- Command executed: `python3 -m pytest tests/test_recommendation.py`
- Result: Exited with code 1 (`/usr/bin/python3: No module named pytest`).
- **Root Causes**:
  1. `requirements.txt` contains a syntax error: line 16 has `pytestok` instead of `pytest`.
  2. Even if `pytest` were installed, all 6 tests would fail with `FileNotFoundError` because `data/processed/interactions.csv` is missing.
- **Audit Classification**: **⚠️ Execution Failed / Incomplete**.
- **Missing Test Coverage**:
  - Zero tests for `api/recommendation_api.py`.
  - Zero tests for evaluation metrics (`precision_at_k`, `recall_at_k`, `ndcg_at_k`).
  - Zero tests for `matrix_factorization.py` or `collaborative_filtering.py`.
  - Zero tests for cold-start edge cases or invalid inputs.

---

### 19. Reproducibility Audit

| Dimension | Verification Finding | Status |
|---|---|---|
| **Dependency Specification** | `requirements.txt` contains unpinned packages and a fatal syntax typo `pytestok`. | ⚠️ Broken |
| **Python Version Compatibility** | Environment uses Python 3.10.12. Code uses standard standard-library and SciPy/Scikit-learn syntax. | ✅ Compatible |
| **Raw Dataset Reproduction** | No raw data files and no automated download/acquisition script. | 🔴 Missing |
| **Processed Data Reproduction** | `preprocess_data.py` cannot run because `data/raw/train.csv` is missing. | 🔴 Blocked |
| **Random Seeds** | `RANDOM_STATE = 42` defined in `config/config.py` and used in SVD and train_test_split. | ✅ Deterministic |
| **Path Handling** | Code uses `pathlib.Path` or relative paths assuming project root as CWD. | 🟡 Inconsistent |

---

### 20. Documentation Audit

1. **`README.md`**: Clean overview, lists project goals and algorithms. Accurately describes the intended hybrid approach, but does not warn the reader that data files are missing or that TruncatedSVD is orphaned.
2. **`docs/methodology.md`**: Well written and technical. It candidly documents that the dataset lacks timestamps and explicit event types. However, it claims Top-K evaluation was performed, while the report files show `[INSERT VALUE]` placeholders.
3. **`docs/project_architecture.md`**: Good overview, but contains a typo on line 61 (`api_documentation.mdv` instead of `api.md`).
4. **`docs/api.md`**: Quality API guide with curl/PowerShell examples and OpenAPI notes. Minor divergence in JSON keys compared to actual FastAPI code.
5. **`outputs/reports/`**:
   - `data_analysis_report.txt`: Complete and informative.
   - `model_comparison_report.txt`: Good theoretical comparison.
   - `evaluation_report.txt`: Incomplete due to unfilled template placeholders.

---

### 21. GitHub / Repository Structure Audit

- **Structure Rating**: Good modular layout following common ML project conventions (`api/`, `app/`, `config/`, `data/`, `docs/`, `outputs/`, `src/`, `tests/`).
- **Defects in Structure**:
  - `data/raw/` directory was completely omitted from Git (likely via untracked status or forgotten commit).
  - Pre-generated images in `outputs/` and `data/processed/` are checked into Git as binary blobs.
  - Model weights/factors are not serialized into a `models/` directory; `RecommendationEngine` rebuilds the TF-IDF matrix and k-NN index in memory from CSV on every single cold start.

---

### 22. Security / Secrets Audit

- **Static Secret Inspection**:
  - Checked `.gitignore`: Properly excludes `.env`, `__pycache__`, `.venv`.
  - Searched repository code for API keys, tokens, hardcoded credentials, database connection strings, or cloud secret URLs.
- **Finding**: **✅ CLEAN / NO SECRETS FOUND**. No credentials or private tokens are present.

---

### 23. Requirement-to-Implementation Gap Matrix

| # | Official Requirement | Repository Evidence | Status | Gap Description | Required Action | Priority |
|---|---|---|---|---|---|---|
| **REQ-01** | User-item interaction data from views, clicks, carts, purchases | `src/data/preprocess_data.py` lines 27–36; `data/processed/users.csv` | ⚠️ INCORRECT / NON-COMPLIANT | Dataset contains only explicit ratings (1–5) from Amazon/Kaggle. No views, clicks, carts, or purchases exist. | Map explicit ratings into synthetic implicit multi-action interactions OR weight ratings as implicit engagement proxies. | 🔴 CRITICAL |
| **REQ-02** | Popularity-based baseline | `src/models/popularity_model.py`; `data/processed/popular_products.csv` | ✅ COMPLETE | Implemented via interaction count $\times$ average rating with min-interaction threshold ($\ge 5$). | Preserve baseline, but evaluate standalone performance in evaluation report. | 🟡 IMPROVEMENT |
| **REQ-03** | Collaborative filtering OR Matrix Factorization | `src/models/collaborative_filtering.py`; `src/models/matrix_factorization.py` | 🟡 PARTIALLY COMPLETE | Both exist as standalone scripts, but Matrix Factorization is completely orphaned, and CF is only used in engine. | Formally integrate chosen model into unified engine and compare against baseline. | 🔴 CRITICAL |
| **REQ-04** | Content-based fallback with metadata (especially for cold-start items) | `src/models/content_based.py`; `src/recommendation/recommendation_engine.py` | ⚠️ INCORRECT / NON-COMPLIANT | Candidate generation restricts pool to top 1,000 popular items, preventing new/cold-start items from ever being recommended. | Remove candidate restriction for content fallback to allow true new-product recommendations. | 🔴 CRITICAL |
| **REQ-05** | Evaluate using Precision@K, Recall@K, NDCG@K | `src/evaluation/evaluate_recommendations.py`; `outputs/reports/evaluation_report.txt` | 🟡 PARTIALLY COMPLETE | Metric formulas implemented, but evaluated an ad-hoc heuristic; report contains `[INSERT VALUE]` placeholders. | Evaluate the actual Hybrid engine and populate verified benchmark numbers. | 🔴 CRITICAL |
| **REQ-06** | Time-based validation split | `src/evaluation/evaluate_recommendations.py` line 42 | ⚠️ INCORRECT / NON-COMPLIANT | Uses random 80/20 train_test_split per user because dataset lacks timestamps. | Synthesize or simulate temporal order / temporal split or state formal defense. | 🔴 CRITICAL |
| **REQ-07** | Simple recommendation API | `api/recommendation_api.py` | 🟡 PARTIALLY COMPLETE | FastAPI service is implemented, but crashes on startup due to missing data CSVs. | Restore missing data tables so API can boot and serve endpoints. | 🔴 CRITICAL |
| **REQ-08** | Analyze recommendations for different user segments | `src/analysis/user_segment_analysis.py`; `data/processed/user_segment_summary.csv` | ⚠️ INCORRECT / NON-COMPLIANT | Segments collapsed (99.95% High Activity); script analyzes only user counts, not recommendation quality across segments. | Redefine segment thresholds by quantiles and evaluate recommendation metrics per segment. | 🔴 CRITICAL |
| **REQ-TECH**| Python, Git, Streamlit/API stack; no Node/React | Entire repository | ✅ COMPLETE | Built cleanly in Python with FastAPI and Streamlit. | Preserve pure Python architecture strictly. | 🔵 MANDATORY |

---

### 24. Component-Level Findings

| Component | Current State | Evidence | Requirement | Gap | Action |
|---|---|---|---|---|---|
| **Data Ingestion** | Broken / Missing Data | `data/raw/` missing; `interactions.csv` missing | REQ-01 | Scripts crash with `FileNotFoundError` | Restore raw or processed interaction data |
| **Interaction Construction** | Explicit ratings only | `preprocess_data.py` lines 27–36 | REQ-01 | Missing views, clicks, carts, purchases | Synthesize/map interactions to multi-behavior weights |
| **Preprocessing** | Functional logic, unrunnable | `src/data/preprocess_data.py` | REQ-01 | Cannot run due to missing raw data | Clean and restore reproducible pipeline |
| **Popularity Baseline** | Complete & Precalculated | `data/processed/popular_products.csv` | REQ-02 | Not evaluated side-by-side in evaluation | Benchmark against personal models |
| **Collaborative Filtering** | Working in Engine; Standalone | `collaborative_filtering.py`; `recommendation_engine.py` | REQ-03 | Re-implemented twice; not in Streamlit UI | Unify engine and restore to Streamlit |
| **Matrix Factorization** | Orphaned Proof of Concept | `src/models/matrix_factorization.py` | REQ-03 | Never used in Engine, API, or Streamlit | Integrate or designate as experimental alternative |
| **Content-Based Fallback** | Defective Candidate Filter | `recommendation_engine.py` line 460 | REQ-04 | Filters out cold-start items | Fix candidate generation for new products |
| **Hybrid Logic** | Inconsistent across apps | `engine.py` vs `streamlit_app.py` | REQ-03, REQ-04 | Streamlit omits CF (uses 70/30 Content/Pop) | Make Streamlit use `RecommendationEngine` directly |
| **Evaluation Metrics** | Code exists, report blank | `evaluate_recommendations.py`; report.txt | REQ-05 | Placeholders in report; evaluated wrong model | Run evaluation on hybrid engine and record metrics |
| **Validation Strategy** | Random holdout | `evaluate_recommendations.py` line 42 | REQ-06 | Requirement mandates time-based split | Implement temporal split strategy |
| **API** | Complete code, broken init | `api/recommendation_api.py` | REQ-07 | Crashes on startup (missing CSV) | Provide processed data files |
| **Streamlit Dashboard** | Rich UI, fractured logic | `app/streamlit_app.py` | REQ-TECH | Bypasses engine; int/str search bug | Refactor to import `RecommendationEngine` |
| **User Segmentation** | 99.95% single-bucket collapse | `user_segment_analysis.py` | REQ-08 | 3/10 thresholds collapse; no rec analysis | Quantile segmentation + segment-level Precision/Recall |
| **Test Suite** | Fails to run | `tests/test_recommendation.py` | QA | Typo in `requirements.txt` (`pytestok`); missing data | Fix typo; verify tests against mock/real data |
| **Configuration** | Central config exists | `config/config.py` | Reproducibility | Not imported uniformly across scripts | Standardize config imports |
| **Documentation** | Comprehensive but inaccurate | `docs/`, `outputs/reports/` | Portfolio quality | Evaluation report blank; minor typos | Populate actual metrics; fix typos |

---

### 25. KEEP

The following components are architecturally sound, well-crafted, and must be **PRESERVED**:
1. **Core Recommendation Engine Class Structure** (`src/recommendation/recommendation_engine.py`): The object-oriented design cleanly encapsulates data loading, sparse matrix construction, user-kNN, TF-IDF cosine similarity, score normalization, and weighted combination.
2. **FastAPI Application Design** (`api/recommendation_api.py`): Clean REST design with proper status endpoints, health checks, path parameter validation, error handling, and JSON serialization.
3. **Streamlit UI Layout & Visual Presentation** (`app/streamlit_app.py`): Clean 3-column metrics, tabbed interface, interactive sliders, and dual display of data tables and native charts.
4. **Metric Calculation Functions** (`src/evaluation/evaluate_recommendations.py`): The implementations of `precision_at_k`, `recall_at_k`, and `ndcg_at_k` are mathematically correct and should be retained.
5. **Popularity Model Formulation** (`src/models/popularity_model.py`): Sensible thresholding ($\ge 5$ interactions) and count-weighted average rating score.
6. **Utility Module** (`src/utils/data_utils.py`): Clean file loading, saving, and column validation helpers.
7. **Technology Stack**: Pure Python, Scikit-learn, SciPy, FastAPI, Streamlit.

---

### 26. IMPROVE

1. **Streamlit App Integration**: Modify `app/streamlit_app.py` to instantiate and use `RecommendationEngine` instead of maintaining a fragmented, divergent recommendation implementation that ignores collaborative filtering.
2. **Candidate Generation in `RecommendationEngine`**: Expand candidate generation beyond the top 1,000 popular items so that content-based similarity can actually surface long-tail and cold-start items.
3. **User Segmentation Thresholds**: Replace the rigid $<3, 3–10, >10$ cutoffs with statistical quantiles (e.g., Low: bottom 25%, Medium: middle 50%, High: top 25%) to reflect the true interaction distribution and eliminate the 99.95% collapse.
4. **User Segment Evaluation**: Extend `user_segment_analysis.py` to evaluate Precision@10, Recall@10, and NDCG@10 separately for each user segment to satisfy REQ-08.
5. **Configuration Consistency**: Ensure all scripts read paths from `config/config.py` rather than hardcoding relative string paths (`data/processed/interactions.csv`).

---

### 27. FIX

1. **Fatal Typo in `requirements.txt`**: Change line 16 from `pytestok` to `pytest`, and pin package versions.
2. **Missing Processed Data Files**: Restore or generate `data/processed/interactions.csv` and `data/processed/products.csv` so the codebase can execute.
3. **User ID Type Coercion Bug in Streamlit**: In `app/streamlit_app.py`, change `user_id_numeric = int(user_id)` to string handling (`str(user_id).strip()`) to prevent type mismatch failures against `interactions["user_id"]`.
4. **Typo in `docs/project_architecture.md`**: Change `api_documentation.mdv` on line 61 to `api.md`.
5. **Evaluation Target**: In `src/evaluation/evaluate_recommendations.py`, evaluate the actual `RecommendationEngine` hybrid model rather than an ad-hoc toy heuristic.
6. **Evaluation Report Placeholders**: Populate the `[INSERT VALUE]` placeholders in `outputs/reports/evaluation_report.txt` with verified offline evaluation numbers.

---

### 28. ADD

1. **Multi-Action Interaction Model (REQ-01)**: Since raw Amazon data only has ratings, add a data-processing mapping that translates ratings and votes into an interaction weighting scheme (or synthetic event simulation) representing views (weight 1), clicks (weight 2), carts (weight 3), and purchases (weight 5).
2. **Time-Based Validation Split (REQ-06)**: Implement a time-aware splitting mechanism (or simulated chronological timestamp sequence) to satisfy the strict internship requirement for time-based evaluation.
3. **Matrix Factorization Integration**: Formally connect TruncatedSVD into either the engine or the comparative evaluation pipeline so it is not an orphaned script.
4. **Comprehensive Test Cases**: Add unit tests for API endpoints, evaluation metric calculations, cold-start handling, and user segmentation.
5. **Data Acquisition / Generation Script**: Add a reproducible script (`src/data/download_or_generate_data.py`) so any reviewer can clone the repo and immediately populate the missing datasets.

---

### 29. Potentially Redundant / Review Later

*(Per safety rules, nothing is deleted during this audit; items below are flagged for future review)*
1. `src/models/hybrid_recommendation.py`: Appears to be an early procedural prototype of what became `src/recommendation/recommendation_engine.py`. Review whether it should be retained as an educational script or consolidated.
2. Duplicate Hybrid Logic in `app/streamlit_app.py`: Once Streamlit imports `RecommendationEngine`, lines 156–350 in `streamlit_app.py` will become redundant.
3. Static binary PNG images in `outputs/tables/` and `data/processed/`: Should eventually be generated via scripts rather than committed as static binary blobs in Git.

---

### 30. Critical Gaps

1. **Missing Data Files Prevent Any Code Execution**: The absence of `interactions.csv` and `products.csv` causes immediate crashes across `recommendation_engine.py`, `recommendation_api.py`, `streamlit_app.py`, `evaluate_recommendations.py`, and `test_recommendation.py`.
2. **Non-Compliant Validation Strategy (REQ-06)**: Random per-user holdout directly violates the explicit requirement for a time-based validation split.
3. **Missing Views, Clicks, Carts, Purchases (REQ-01)**: The dataset only models explicit ratings; implicit interaction behaviors are unrepresented.
4. **Blank Evaluation Report (REQ-05)**: `evaluation_report.txt` has no quantitative results, only placeholder text.
5. **User Segment Collapse (REQ-08)**: 99.95% of users fall into a single segment, and recommendation quality is never evaluated across segments.

---

### 31. Important Gaps

1. **Orphaned Matrix Factorization (REQ-03)**: TruncatedSVD is implemented in isolation and completely absent from the serving and evaluation pipelines.
2. **Streamlit Logic Divergence**: Streamlit omits collaborative filtering, advertising a hybrid system that is actually only Content + Popularity.
3. **Cold-Start Item Filter Flaw (REQ-04)**: Candidate pool truncation to the top 1,000 popular items prevents cold-start products from ever being recommended.
4. **Dependency Typo & Test Failure**: `pytestok` prevents clean environment installation, and the test suite cannot execute.

---

### 32. Improvement Opportunities

1. **Model Persistence**: Serialize precomputed TF-IDF matrices, nearest-neighbor indices, and latent matrices to disk (`models/`) to eliminate repetitive training on every startup.
2. **Quantile-Based User Segmentation**: Use quartile splits (Q1, Q2–Q3, Q4) to provide balanced, actionable user segments.
3. **Comparative Evaluation**: Generate a comparative table reporting Precision@10, Recall@10, and NDCG@10 across all 4 models: Popularity Baseline, Collaborative Filtering, Matrix Factorization, and Hybrid.

---

### 33. Optional Enhancements

1. Add Dockerfile for reproducible containerized execution of the API and Streamlit apps.
2. Implement an automated script to benchmark API latency and throughput under concurrent requests.
3. Add interactive Swagger UI testing documentation directly linked in the Streamlit sidebar.

---

### 34. Proposed Completion Roadmap

The following phased roadmap outlines the exact sequence required to bring Project 3 into 100% compliance with internship requirements:

```
Phase 1: Environment & Data Pipeline Stabilization (Fix Blockers)
  ├── 1.1 Fix `requirements.txt` typo (`pytestok` -> `pytest`) and pin versions.
  ├── 1.2 Implement reproducible data acquisition/synthesis for missing interaction files.
  ├── 1.3 Map ratings & interactions to incorporate view/click/cart/purchase weights (REQ-01).
  └── 1.4 Restore `data/processed/interactions.csv` and `data/processed/products.csv`.

Phase 2: Architectural Unification & Model Integration
  ├── 2.1 Refactor `RecommendationEngine` to remove the 1000-popular candidate restriction for content fallback (REQ-04).
  ├── 2.2 Integrate Matrix Factorization alongside Collaborative Filtering (REQ-03).
  ├── 2.3 Refactor `app/streamlit_app.py` to import and use `RecommendationEngine` directly.
  └── 2.4 Fix string/integer ID matching bug in Streamlit.

Phase 3: Time-Based Validation & Rigorous Evaluation (REQ-05, REQ-06)
  ├── 3.1 Implement a time-based validation split (or simulated temporal sequence).
  ├── 3.2 Evaluate all 4 models (Popularity, CF, MF, Hybrid) on Precision@10, Recall@10, NDCG@10.
  └── 3.3 Replace placeholders in `outputs/reports/evaluation_report.txt` with verified empirical scores.

Phase 4: Meaningful User Segment Recommendation Analysis (REQ-08)
  ├── 4.1 Re-segment user base using quantile boundaries to avoid 99.95% single-bucket collapse.
  ├── 4.2 Compute and plot Precision@10, Recall@10, and NDCG@10 across each segment.
  └── 4.3 Update segment analysis summary and visualizations.

Phase 5: API Verification, Testing & Final Polish
  ├── 5.1 Verify FastAPI endpoints (`/recommend/{user_id}`, `/health`) with live data.
  ├── 5.2 Expand `tests/test_recommendation.py` to cover API, metrics, and cold-start fallbacks.
  ├── 5.3 Fix documentation typos (`api_documentation.mdv`).
  └── 5.4 Execute final end-to-end verification run.
```

---

### 35. Final Audit Conclusion

The repository shows solid foundational engineering in its modular architecture, clean FastAPI endpoints, Streamlit dashboard layout, and standalone modeling scripts. However, it currently cannot execute due to missing core data files, fails to satisfy the official requirements for multi-event interaction types (REQ-01) and time-based validation (REQ-06), exhibits architectural fracturing between the core engine and the Streamlit UI, suffers from a 99.95% user segment collapse, and contains an unpopulated evaluation report.

Following the structured 5-phase roadmap will resolve all technical defects and bring the project into complete compliance with internship evaluation standards.
