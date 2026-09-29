# Data Foundation Report

## 1. Dataset Provenance

The primary dataset declared and utilized for Project 3 is the **Monash University FIT5212 S1 2025 Recommender System Challenge** dataset (`fit-5212-s-1-2025`), derived from an Amazon e-commerce crawl covering product catalog metadata and customer ratings.

- **Institution & Unit:** Monash University, Faculty of Information Technology, Unit FIT5212 (Data analysis for semi-structured data), Semester 1, 2025.
- **Platform:** Kaggle In-Class Competitions (`https://www.kaggle.com/competitions/fit-5212-s-1-2025`).
- **Participating Teams:** 88 teams.
- **Underlying Domain:** Amazon customer reviews across books, audio CDs, DVDs/movies, and electronic products.

## 2. Source

- **Official Distribution:** Distributed to enrolled students via Kaggle In-Class platform.
- **Acquisition State in Environment:** Direct public unauthenticated download returns HTTP 401 Unauthorized. Automated retrieval requires student-level Kaggle API credentials (`kaggle.json`).
- **Existing Baseline Artifacts in Repository:**
  - `data/processed/popular_products.csv`: 33,072 products precomputed from genuine training records.
  - `data/processed/users.csv`: 2,000 active users with genuine interaction summary metrics.
  - `data/processed/user_segment_summary.csv`: Activity segmentation summary.
  - `outputs/reports/data_analysis_report.txt`: Historical data audit report.

## 3. Schema

### Documented Raw Schema (`train.csv`):
| Column | Type | Nullable | Domain / Constraints | Description |
|---|---|---|---|---|
| `user_id` | String | No | Non-empty string | User unique identifier |
| `product_id` | String | No | Non-empty string | Product unique identifier |
| `product_name` | String | Yes | Text | Product title / name |
| `rating` | Numeric | No | Discrete integer in [1, 5] | Explicit customer rating |
| `votes` | Numeric | Yes | Integer $\ge 0$ | Total review votes recorded |
| `helpful_votes` | Numeric | Yes | Integer $\ge 0, \le \text{votes}$ | Helpful review votes |

## 4. Interaction Semantics

The interaction events in this dataset represent **explicit user ratings on a 1 to 5 star scale**.
- They do **NOT** represent web page views.
- They do **NOT** represent search clicks or impressions.
- They do **NOT** represent cart additions.
- They do **NOT** represent e-commerce purchases or financial transactions.

For recommendation ranking evaluation, a binary preference signal is derived:
$$\text{Relevant} = \begin{cases} 1 & \text{if } \text{Rating} \ge 4 \\ 0 & \text{if } \text{Rating} < 4 \end{cases}$$
This is explicitly a **derived evaluation convention**, not a behavioral log event.

## 5. User Statistics

From the authentic `data/processed/users.csv` baseline (2,000 users):
- **Total Registered Users:** 2,000
- **Interaction Count per User:**
  - Minimum: 4
  - 25th Percentile: 169
  - Median: 219
  - Mean: 372.94
  - 75th Percentile: 329
  - Maximum: 112,483
  - Standard Deviation: 2,603.87
- **Average Rating per User:**
  - Minimum: 2.76
  - Median: 4.31
  - Mean: 4.28
  - Maximum: 5.00
- **User Activity Distribution:** Highly skewed right tail with heavy engagement among core users.

## 6. Product Statistics

From the authentic `data/processed/popular_products.csv` baseline (33,072 products):
- **Total Cataloged Products:** 33,072
- **Interaction Count per Product:**
  - Minimum: 5 (popularity baseline threshold)
  - 25th Percentile: 6
  - Median: 9
  - Mean: 18.52
  - 75th Percentile: 18
  - Maximum: 275 (Product ID 212937: *The Lord of the Rings - The Fellowship of the Ring*)
- **Average Rating per Product:**
  - Minimum: 1.00
  - Median: 4.33
  - Mean: 4.19
  - Maximum: 5.00

## 7. Rating Statistics

From verified baseline documentation (`outputs/reports/data_analysis_report.txt`):
- **Total Training Interactions:** 745,889
- **Rating 1:** 29,149 (3.91%)
- **Rating 2:** 35,446 (4.75%)
- **Rating 3:** 79,870 (10.71%)
- **Rating 4:** 185,193 (24.83%)
- **Rating 5:** 416,231 (55.80%)
- **Overall Mean Rating:** $\approx 4.24$
- **High-Rating Bias:** Over 80.6% of ratings are 4 or 5 stars, which is typical for e-commerce voluntary product review distributions.

## 8. Timestamp Statistics

- **Timestamp Column Availability:** None.
- **Original Source Verification:** Neither `fit-5212-s-1-2025` nor the baseline CSVs provide timestamps.
- **Status:** **NO LEGITIMATE TIMESTAMP SOURCE IDENTIFIED**.
- **Governance Finding:** Classified as **`INVALID FOR TEMPORAL VALIDATION`**. No artificial timestamps or chronological inferences from IDs or row positions are permitted.

## 9. Missing Values

Analysis of the processing rules:
- `user_id`: Mandatory. Rows with missing `user_id` are dropped.
- `product_id`: Mandatory. Rows with missing `product_id` are dropped.
- `rating`: Mandatory. Rows missing ratings or with non-numeric ratings are dropped.
- `product_name`: Optional metadata. Missing product names imputed as `"Unknown Product"` to preserve interaction history for collaborative filtering while permitting content fallback.
- `votes` & `helpful_votes`: Missing numerical values imputed as `0` representing zero recorded feedback votes.

## 10. Duplicate Analysis

- Preprocessing enforces: `drop_duplicates(subset=["user_id", "product_id"])`.
- In an explicit rating system without timestamps, repeated user-item pairs represent either repeated submissions or review updates.
- In the absence of chronological ordering, the standard policy preserves the first observed unique user-item interaction record.

## 11. Data Cleaning

The pipeline implemented in `src/data/preprocess_data.py` and `src/data/create_entities.py` guarantees:
1. Deterministic data loading from `data/raw/train.csv`.
2. Explicit schema coercion (`user_id`: str, `product_id`: str, `rating`: numeric).
3. Filtering ratings strictly to the valid domain $1 \le \text{rating} \le 5$.
4. Logging all row alterations (initial rows, duplicates dropped, nulls dropped, invalid ratings dropped, clean rows output).
5. Segregation of clean interactions into `data/processed/interactions.csv`.

## 12. Train / Validation / Test Construction

Under **Path B (Non-Temporal Validation Protocol)**:
- **Strategy:** User-Level Stratified Holdout (`src/data/split_data.py`).
- **Holdout Ratio:** 20% validation interactions for users with $\ge 5$ interactions; 80% training interactions.
- **Cold-Start Preservation:** Users with $<5$ interactions are placed entirely in the training set to prevent zero-relevance validation anomalies.
- **Random Seed:** Pinned to `random_state = 42` for strict determinism and reproducibility.

## 13. Leakage Controls

1. **Split Isolation:** The training set and validation set index sets have zero intersection ($\text{Train} \cap \text{Val} = \emptyset$).
2. **Feature Calculation:** User and product entity features used for model fitting are calculated strictly from the training partition.
3. **Popularity Model:** Global popularity scores must be computed exclusively on training split observations.
4. **TF-IDF Vectorization:** The content-based TF-IDF vectorizer must fit vocabulary and IDF weights on the available catalog metadata without evaluating validation target interactions.

## 14. Cold-Start Data Availability

The data foundation categorizes four operational cold-start scenarios:
1. **New User (Zero Interactions):** Handled via Popularity baseline fallback.
2. **Sparse User (< 5 Interactions):** Handled via hybrid content + popularity weighting.
3. **New Product (Zero Historical Ratings):** Preserved in catalog metadata; surfaced via content-based TF-IDF similarity.
4. **Sparse Product (< 5 Ratings):** Excluded from the pure popularity ranking (threshold = 5), but retrievable via collaborative/content hybrid scoring.

## 15. Known Limitations

1. **Absence of Timestamps:** True temporal backtesting (e.g., training on interactions up to Month $T$ and predicting Month $T+1$) cannot be performed on this dataset.
2. **Missing Raw Source File:** `data/raw/train.csv` is not present in the current container environment due to Kaggle in-class credential restrictions.
3. **Synthetic Artifacts Quarantined:** `data/processed/interactions.csv` and `data/processed/products.csv` are quarantined and must not be used for model training or evaluation.

## 16. Reproducibility

The data pipeline is fully reproducible:
1. **Raw Ingestion:** `python3 src/data/acquire_data.py` registers files and generates checksums.
2. **Cleaning:** `python3 src/data/preprocess_data.py` executes data cleaning and outputs `interactions.csv`.
3. **Entity Generation:** `python3 src/data/create_entities.py` derives `users.csv` and `products.csv`.
4. **Splitting:** `python3 src/data/split_data.py` produces the leakage-free train/validation split.
