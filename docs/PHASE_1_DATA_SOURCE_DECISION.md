# Phase 1 Data Source Decision

## 1. Original Project Dataset

The original project dataset is the **Monash University FIT5212 S1 2025 Recommender System Challenge** dataset, derived from a crawl of Amazon product catalog metadata and user reviews.

- **Declared Context:** In-class machine learning competition for postgraduate unit FIT5212 ("Data analysis for semi-structured data") at Monash University, Faculty of Information Technology, Semester 1, 2025.
- **Hosted On:** Kaggle In-Class Competitions platform under competition slug `fit-5212-s-1-2025` (`https://www.kaggle.com/competitions/fit-5212-s-1-2025`).
- **Original Scale:** 745,889 training records (`train.csv`), 223,553 test pairs (`test.csv`), across 201,325 unique products and explicit ratings on a 1–5 discrete scale.
- **Original Documented Fields:** `user_id`, `product_id`, `product_name`, `rating`, `votes`, `helpful_votes`.
- **Temporal Status in Original Source:** No review timestamps, event dates, or UNIX epoch seconds were included in the competition distribution.

## 2. Documented Provenance

1. **Course & Institution:** Monash University, Faculty of Information Technology, Unit FIT5212.
2. **Competition Platform:** Kaggle In-Class Competition (`fit-5212-s-1-2025`), with 88 participating student teams.
3. **Primary Source Data:** Amazon e-commerce product catalog crawl (books, audio CDs, DVDs/movies, consumer electronics) with associated explicit customer star ratings and review helpfulness voting metrics.
4. **Historical Repository Artifacts:**
   - `outputs/reports/data_analysis_report.txt`: Established on 2026-09-29 18:43:57, documenting exact training record counts (745,889), rating distribution (Rating 1: 29,149; Rating 2: 35,446; Rating 3: 79,870; Rating 4: 185,193; Rating 5: 416,231), and the explicit absence of timestamps.
   - `data/processed/popular_products.csv`: Precomputed table of 33,072 products with exact interaction counts, unique users, average ratings, and popularity scores.
   - `data/processed/users.csv`: Precomputed table of 2,000 users with exact interaction counts, unique products, average ratings, and total votes.
   - `data/processed/user_segment_summary.csv`: Precomputed user segmentation artifact.

## 3. Candidate Source(s)

| Source | Relationship | Timestamp? | Legitimate? | Reproducible? | Decision |
|---|---|---|---|---|---|
| **Supplied Authentic Raw Data (`train_part1.csv` + `train_part2.csv`, `test.csv`)** | Authoritative competition files supplied by user | No | Yes (Authoritative, verified SHA-256) | 100% reproducible within repository | **SELECTED & INGESTED AS OFFICIAL CANONICAL SOURCE** (Unblocks Phase 1) |
| **Public Amazon Snapshots (UCSD McAuley / Stanford SNAP)** | Third-party crawl of Amazon reviews | Yes (`unixReviewTime`) | Legitimate external dataset, but NOT the project dataset | Yes | **REJECTED**: Distinct ID space, different tokenization, incompatible user/product entities; violates Rule 1 & Rule 36. |
| **MovieLens (100k / 1M / 20M)** | Unrelated movie rating benchmark | Yes (`timestamp`) | Legitimate external benchmark | Yes | **REJECTED**: Incompatible with project domain, entities, and UI. |
| **Existing Verified Baseline Artifacts (`popular_products.csv`, `users.csv`)** | Preserved precomputed project artifacts from legitimate `train.csv` | No | Yes (Authentic precomputed artifacts) | 100% reproducible within repository | **CONFIRMED & REPRODUCED (100.0% EXACT MATCH)** |
| **Quarantined Synthetic CSVs (`data/quarantined_synthetic/`)** | Procedurally generated artifacts from previous turn | No | No (Synthetic / Inferred) | Procedural | **QUARANTINED**: Archived into `data/quarantined_synthetic/`, strictly excluded from all modeling and evaluation. |

## 4. Selected Source

The official canonical dataset for this project is:
**Monash University FIT5212 S1 2025 Recommender System Challenge (`fit-5212-s-1-2025`)**, ingested via `data/raw/train_part1.csv` (372,944 rows) and `data/raw/train_part2.csv` (372,945 rows) forming 745,889 authentic interactions, accompanied by `data/raw/test.csv` (223,553 rows).

## 5. Why This Source Was Selected

1. **Exact Historical Match:** 745,889 training interactions and 223,553 test pairs match the documented FIT5212 competition baseline to the exact row count.
2. **Entity Consistency:** Re-aggregating the supplied data reproduces `data/processed/users.csv` and `data/processed/popular_products.csv` with a 100.0% exact match across all 2,000 users and 33,072 products.
3. **Dataset Identity Preservation (Rule 36):** Preserves complete alignment with the repository architecture, models, API, UI, and documentation without entity corruption.

## 6. Timestamp Finding

**NO LEGITIMATE TIMESTAMP SOURCE IDENTIFIED**

- Neither the Kaggle competition dataset `fit-5212-s-1-2025` (`train_part1.csv`, `train_part2.csv`, `test.csv`) nor the baseline artifacts contain a timestamp column.
- As confirmed by the original repository data report (`outputs/reports/data_analysis_report.txt` Section 5): *"The dataset does not contain a timestamp field. Therefore, a genuine chronological/time-based validation split cannot be performed from the available data. The evaluation procedure uses a user-level holdout strategy instead of assuming or fabricating timestamps."*
- Consequently, **Path B** of Section 7 is formally enacted.
- Any attempt to invent timestamps or infer chronology from row indexes or IDs is classified as **INVALID FOR TEMPORAL VALIDATION**.

## 7. Data Governance Decision

1. **Path B Enacted:** The project adopts a rigorous non-temporal, user-level holdout validation protocol (80% training / 20% validation per eligible user, stratified by user activity, random seed = 42), as detailed in `EVALUATION_AND_ERROR_ANALYSIS.md` and `EXPERIMENT_PLAN.md`.
2. **Temporal Validation Status:** The project explicitly documents that true temporal validation is unavailable for this dataset version, satisfying Rule 34 and Rule-TIME-006 without fabrication.
3. **Synthetic Data Quarantined:** Old synthetic files are safely moved to `data/quarantined_synthetic/` under a strict quarantine policy. All operational processed files are 100% authentic and derived from the supplied raw data.
4. **Acquisition & Pipeline Verified:** `src/data/acquire_data.py`, `src/data/preprocess_data.py`, `src/data/create_entities.py`, and `src/data/split_data.py` are executed and verified.
5. **Phase 1 Unblocked:** With authentic raw training and test data verified in the environment, the Phase 1 blocker is resolved.

