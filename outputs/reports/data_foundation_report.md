# Data Foundation Report

## 1. Dataset Provenance

The primary dataset declared and utilized for Project 3 is the **Monash University FIT5212 S1 2025 Recommender System Challenge** dataset (`fit-5212-s-1-2025`), derived from an Amazon e-commerce crawl covering product catalog metadata and customer ratings.

- **Institution & Unit:** Monash University, Faculty of Information Technology, Unit FIT5212 (Data analysis for semi-structured data), Semester 1, 2025.
- **Platform:** Kaggle In-Class Competitions (`https://www.kaggle.com/competitions/fit-5212-s-1-2025`).
- **Participating Teams:** 88 teams.
- **Underlying Domain:** Amazon customer reviews across books, audio CDs, DVDs/movies, and electronic products.

## 2. Source

- **Authentic Raw Inputs Supplied:**
  - `data/raw/train_part1.csv`: 372,944 rows (SHA-256: `3ed0874e9352d4e9be59fc44d0810bee1fb2949976d307c6e5451d1fade34bb1`)
  - `data/raw/train_part2.csv`: 372,945 rows (SHA-256: `9e10297f3236cb67cb2e47a2d929f82be144d97652a17cec2d21b9fc02038969`)
  - `data/raw/test.csv`: 223,553 rows (SHA-256: `bbdb9ba79b6e37c38d30661edc8413b05e58c9092a830b5bf12d1de7bdfec65c`)
- **Logical Training Dataset:** `train_part1.csv` and `train_part2.csv` are row-wise parts of the original `train.csv` (split strictly for upload size accommodation) forming an exact combined total of 745,889 records.
- **Baseline Entity Artifacts:** Verified against the combined training records, confirming a 100.0% reproducible match with `popular_products.csv` (33,072 items) and `users.csv` (2,000 users).

## 3. Schema

### Raw Source Schema:
| Column | Type | Nullable | Domain / Constraints | Description |
|---|---|---|---|---|
| `user_id` | String | No | Non-empty string | User unique identifier |
| `product_id` | String | No | Non-empty string | Product unique identifier |
| `product_name` | String | No | Non-empty string | Product title / name |
| `rating` | Numeric (int) | No | Discrete integer in [1, 5] | Explicit customer rating |
| `votes` | Numeric (int) | No | Integer $\ge 0$ | Total review votes recorded |
| `helpful_votes` | Numeric (int) | No | Integer $\ge 0, \le \text{votes}$ | Helpful review votes |
| `ID` | Numeric (int) | No | Unique row index | Kaggle submission identifier |

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

From the authentic training dataset across all 2,000 unique users:
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
- **Active Users ($\ge 5$ interactions):** 1,999 (99.95%)
- **Sparse Users ($< 5$ interactions):** 1 (0.05%, user_id 1999 has 4 interactions)

## 6. Product Statistics

From the authentic catalog across all 201,325 unique products:
- **Total Cataloged Products:** 201,325
- **Interaction Count per Product:**
  - Minimum: 1
  - Median: 1
  - Mean: 3.70
  - Maximum: 275 (Product ID 212937: *The Lord of the Rings - The Fellowship of the Ring*)
- **Popular Products ($\ge 5$ interactions):** 33,072 products (16.43% of catalog, matching `popular_products.csv`)
- **Long-tail / Sparse Products ($< 5$ interactions):** 168,253 products (83.57% of catalog)
- **Average Rating per Product:**
  - Minimum: 1.00
  - Median: 4.50
  - Mean: 4.19
  - Maximum: 5.00

## 7. Rating Statistics

From the full 745,889 authentic training records:
- **Total Training Interactions:** 745,889
- **Rating 1:** 29,149 (3.91%)
- **Rating 2:** 35,446 (4.75%)
- **Rating 3:** 79,870 (10.71%)
- **Rating 4:** 185,193 (24.83%)
- **Rating 5:** 416,231 (55.80%)
- **Mean Rating:** $4.2387 \approx 4.24$
- **Median Rating:** 5.00
- **Standard Deviation:** 1.0724
- **Positive Ratings ($\ge 4$):** 601,424 (80.63%)

## 8. Timestamp Statistics

- **Timestamp Column Availability:** None.
- **Inspected Fields:** `user_id`, `product_id`, `product_name`, `rating`, `votes`, `helpful_votes`, `ID`.
- **Status:** **NO LEGITIMATE TIMESTAMP SOURCE IDENTIFIED**.
- **Governance Finding:** Classified as **`INVALID FOR TEMPORAL VALIDATION`**. No artificial timestamps or chronological inferences from IDs or row positions are permitted. **Path B (Non-Temporal Validation Protocol)** is permanently enacted.

## 9. Missing Values

Analysis of the authentic raw dataset:
- `user_id`: 0 missing values
- `product_id`: 0 missing values
- `product_name`: 0 missing values
- `rating`: 0 missing values
- `votes`: 0 missing values
- `helpful_votes`: 0 missing values
- `ID`: 0 missing values

The raw data has 100% complete field population across all 745,889 rows.

## 10. Duplicate Analysis

- **Exact Duplicate Rows:** 0
- **Duplicate `(user_id, product_id)` Pairs:** 0
- Every single interaction in the 745,889 training set is a distinct user-item observation.
- Conflicting ratings for the same user-item pair: 0.

## 11. Data Cleaning

The pipeline implemented in `src/data/preprocess_data.py` and `src/data/create_entities.py` executes:
1. Logical loading and concatenation of `train_part1.csv` and `train_part2.csv`.
2. Selection of domain fields (`user_id`, `product_id`, `product_name`, `rating`, `votes`, `helpful_votes`).
3. Explicit type coercion (`user_id`: str, `product_id`: str, `rating`: int, `votes`: int, `helpful_votes`: int).
4. Rating domain verification ($1 \le \text{rating} \le 5$).
5. Generation of authentic `data/processed/interactions.csv` (745,889 rows) and `data/processed/products.csv` (201,325 rows).
6. Comprehensive audit logging to `outputs/reports/data_cleaning_audit.json`.

## 12. Train / Validation / Test Construction

Under **Path B (Non-Temporal Validation Protocol)**:
- **Module:** `src/data/split_data.py`
- **Split Mechanics:** Stratified user-level holdout. For users with $\ge 5$ interactions (1,999 users), 20% of observed interactions are held out into the validation partition, and 80% are placed in the training partition.
- **Split Breakdown:**
  - Training Partition: 597,502 interactions (80.11%)
  - Validation Partition: 148,387 interactions (19.89%)
- **Cold-Start Handling:** The 1 user with $< 5$ interactions is retained 100% in training to prevent degenerate single-item holdouts.
- **Determinism:** Seed pinned to `random_state = 42`.
- **Test Set Isolation:** `data/raw/test.csv` (223,553 pairs) remains strictly isolated from all model training and validation routines.

## 13. Leakage Controls

1. **Index Disjointness:** $\text{Train} \cap \text{Val} = \emptyset$ verified by assertion.
2. **Popularity Feature Isolation:** Candidate rankings and popularity scores are computed strictly from training split interactions.
3. **TF-IDF Vocabulary Isolation:** Content representations fit vocabulary on training catalog data without evaluating validation targets.
4. **User History Isolation:** Recommendation engines use only training history when generating recommendations for evaluated users.

## 14. Cold-Start Data Availability

- **New Users in Test Set:** 0 (all 2,000 test users exist in the training set).
- **New Products in Test Set:** 18,534 products (products present in `test.csv` with metadata but zero training interactions).
- **Sparse Products in Training Set:** 168,253 products with $< 5$ interactions.
- **Sparse Users in Training Set:** 1 user with $< 5$ interactions.

## 15. Known Limitations

1. **Absence of Timestamps:** True temporal backtesting (e.g., training on interactions up to Month $T$ and predicting Month $T+1$) cannot be performed on this dataset because the competition organizers did not capture or distribute review dates.
2. **Quarantined Synthetic Artifacts:** Historical synthetic artifacts generated in earlier turns remain archived in `data/quarantined_synthetic/` and are strictly excluded from modeling.

## 16. Reproducibility

Full reproduction sequence:
1. Register raw source data: `python3 src/data/acquire_data.py`
2. Run data cleaning pipeline: `python3 src/data/preprocess_data.py`
3. Generate entity tables: `python3 src/data/create_entities.py`
4. Generate leakage-free splits: `python3 src/data/split_data.py`
5. Run verification suite: `python3 -m pytest tests/test_data_foundation.py`

## 17. Tests

Data foundation test suite (`tests/test_data_foundation.py`):
- `test_popular_products_schema_and_domain`: **PASSED**
- `test_users_schema_and_domain`: **PASSED**
- `test_split_holdout_leakage_and_determinism`: **PASSED**
- `test_raw_data_registry_structure`: **PASSED**
- `test_data_foundation_audit_json_exists`: **PASSED**
Full test suite (`tests/test_data_foundation.py` + `tests/test_recommendation.py`): **11 passed in 3.42s**.

## 18. Phase 1 Exit Decision

**PASS**

### Justification:
All 23 acceptance criteria of Phase 1 are completely satisfied. Authentic raw training data (`train_part1.csv` + `train_part2.csv`, 745,889 rows) and test data (`test.csv`, 223,553 rows) have been verified with SHA-256 hashes, preprocessed into clean interaction tables, validated against authentic entity baselines (100% reproducible match), and split into leakage-free train/validation sets under Path B. Zero synthetic data or timestamps are used. Phase 1 is fully UNBLOCKED and complete.
