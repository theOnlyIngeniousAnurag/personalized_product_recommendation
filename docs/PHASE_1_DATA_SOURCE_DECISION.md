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
| **Kaggle In-Class `fit-5212-s-1-2025`** | Authoritative competition distribution | No | Yes (Authoritative) | Requires authenticated student API credentials (HTTP 401 Unauthorized for public access) | **SELECTED AS OFFICIAL CANONICAL SOURCE** (Awaiting credentialed download / manual file ingestion) |
| **Public Amazon Snapshots (UCSD McAuley / Stanford SNAP)** | Third-party crawl of Amazon reviews | Yes (`unixReviewTime`) | Legitimate external dataset, but NOT the project dataset | Yes | **REJECTED**: Distinct ID space, different tokenization, incompatible user/product entities; violates Rule 1 & Rule 36 ("Do not replace the project dataset with an unrelated recommendation dataset... Do not sacrifice dataset identity merely to obtain timestamps"). |
| **MovieLens (100k / 1M / 20M)** | Unrelated movie rating benchmark | Yes (`timestamp`) | Legitimate external benchmark | Yes | **REJECTED**: Completely unrelated product domain and entity IDs; incompatible with project architecture and UI. |
| **Existing Verified Baseline Artifacts (`popular_products.csv`, `users.csv`)** | Preserved precomputed project artifacts from legitimate `train.csv` | No | Yes (Authentic precomputed artifacts) | 100% reproducible within repository | **RETAINED AS AUTHORITATIVE GROUND-TRUTH ENTITY BASELINES** |
| **Synthesized CSVs (`data/processed/interactions.csv`, `data/processed/products.csv`)** | Procedurally generated artifacts from previous turn | No | No (Synthetic / Inferred) | Procedural | **REJECTED FOR MODELING/EVALUATION**: Classified as `SYNTHETIC — NOT FOR TRAINING/EVALUATION`. |

## 4. Selected Source

The official canonical dataset for this project remains:
**Monash University FIT5212 S1 2025 Recommender System Challenge (`fit-5212-s-1-2025`)**, supplemented by the project's authentic, verified precomputed entity artifacts (`popular_products.csv` and `users.csv`).

## 5. Why This Source Was Selected

1. **Dataset Identity Preservation (Rule 36):** The project architecture, Streamlit UI, candidate generator, product search, user segmentation, and documentation are strictly designed around this specific Amazon crawl dataset.
2. **Authentic Ground Truth:** The precomputed artifacts (`popular_products.csv`, `users.csv`) preserve exact interaction aggregations, user profiles, and product names from the genuine competition `train.csv`.
3. **No Semantic Corruption:** Introducing external datasets would corrupt product metadata and require inventing mappings to the 33,072 products already referenced across the application and documentation.
4. **Honest Evaluation Boundary:** Rather than fabricating compliance by adopting an unrelated dataset solely for timestamps, adopting the documented dataset preserves scientific integrity.

## 6. Timestamp Finding

**NO LEGITIMATE TIMESTAMP SOURCE IDENTIFIED**

- Neither the Kaggle competition dataset `fit-5212-s-1-2025` nor the authentic baseline artifacts contain a timestamp column.
- As confirmed by the original repository data report (`outputs/reports/data_analysis_report.txt` Section 5): *"The dataset does not contain a timestamp field. Therefore, a genuine chronological/time-based validation split cannot be performed from the available data. The evaluation procedure uses a user-level holdout strategy instead of assuming or fabricating timestamps."*
- Consequently, **Path B** of Section 7 is formally enacted.
- Any attempt to invent timestamps or infer chronology from row indexes or IDs is classified as **INVALID FOR TEMPORAL VALIDATION**.

## 7. Data Governance Decision

1. **Path B Enacted:** The project adopts a rigorous non-temporal, user-level holdout validation protocol (80% training / 20% validation per eligible user, stratified by user activity), as detailed in `EVALUATION_AND_ERROR_ANALYSIS.md` and `EXPERIMENT_PLAN.md`.
2. **Temporal Validation Status:** The project explicitly documents that true temporal validation is unavailable for this dataset version, satisfying Rule 34 and Rule-TIME-006 without fabrication.
3. **Synthetic Data Quarantined:** `data/processed/interactions.csv` and `data/processed/products.csv` are marked as `SYNTHETIC — NOT FOR TRAINING/EVALUATION`. They are preserved as non-training historical artifacts (Rule 4) and will not be used to train models or calculate evaluation metrics.
4. **Acquisition Pipeline Provided:** A reproducible acquisition script (`src/data/acquire_data.py`) and data directory structure (`data/raw/`, `data/interim/`, `data/processed/`) are established to ingest and validate `train.csv` when supplied by an authorized user or through Kaggle credentials.
5. **Phase 1 Readiness Gated:** The Phase 1 Exit Gate is governed by whether legitimate raw interactions are in place before Phase 2 begins.
