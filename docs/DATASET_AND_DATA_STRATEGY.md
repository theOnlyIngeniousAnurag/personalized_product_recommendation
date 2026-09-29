# DATASET_AND_DATA_STRATEGY.md

# Dataset & Data Strategy
## Personalized Product Recommendation Model

---

## Document Control

| Field | Value |
|---|---|
| Project | Personalized Product Recommendation Model |
| Project Number | Project 3 |
| Document | Dataset & Data Strategy |
| Version | 1.0 |
| Status | Approved Technical Baseline |
| Parent Documents | `PRD.md`, `PROJECT_SPECIFICATIONS.md` |
| Current-State Reference | `audit_report.md` |
| Primary Data Modality | User–Item Interaction Data |
| Current Audited Dataset | Monash University FIT5212 S1 2025 Recommender System Challenge dataset |
| Dataset Domain | Amazon product ratings/reviews |
| Primary Data Format | CSV |
| Processing Language | Python |
| Primary Processing Stack | pandas / NumPy / scikit-learn |
| Storage Strategy | Raw → Intermediate → Processed |
| Primary Objective | Establish a legitimate, reproducible, leakage-safe data foundation for Project 3 |

---

# 1. PURPOSE

This document defines the complete data strategy for the Personalized Product Recommendation Model.

It establishes:

- Dataset provenance
- Dataset acquisition
- Dataset restoration
- Raw-data handling
- Schema
- Entity definitions
- Interaction semantics
- Data-quality rules
- Missing-value handling
- Duplicate handling
- Interaction representation
- Product metadata handling
- User representation
- Timestamp strategy
- Temporal validation strategy
- Leakage prevention
- Train/validation/test construction
- Cold-start data strategy
- User-segment data strategy
- Processed-data artifacts
- Reproducibility requirements
- Data validation requirements
- Data limitations
- Data-governance rules
- Recovery strategy for missing repository data

This document is particularly important because the repository audit identified the **data foundation as one of the primary blockers** to executing Project 3.

---

# 2. DATA STRATEGY OBJECTIVE

The objective is to establish a data pipeline that transforms the legitimate source dataset into a set of validated, reproducible, model-ready representations:

```text
Legitimate Source
        ↓
Raw Dataset
        ↓
Source Validation
        ↓
Schema Validation
        ↓
Data Quality Checks
        ↓
Cleaning
        ↓
Interaction Construction
        ↓
User / Product Entity Construction
        ↓
Training / Validation / Test Preparation
        ↓
Model-Ready Data
        ↓
Recommendation Models
        ↓
Evaluation
```

The data pipeline must preserve the meaning of the original dataset.

The pipeline must never modify the semantic meaning of source observations merely to make the project appear compliant with a requirement.

---

# 3. DATA STRATEGY PRINCIPLES

## 3.1 Data Integrity First

The source data must remain the authoritative representation of what was actually observed.

---

## 3.2 No Fabricated Behavioral Events

The project must not fabricate:

- Views
- Clicks
- Carts
- Purchases

and represent them as genuine user behavior.

The audited source contains explicit ratings and related review information rather than separate behavioral event types.

Therefore, ratings must remain ratings.

---

## 3.3 No Fabricated Timestamps

The project must not create artificial timestamps solely to satisfy the temporal-validation requirement.

The following are prohibited:

- Random timestamps
- Sequential timestamps based on row order
- Artificial timestamps assigned according to user/item order
- Randomly distributed historical dates
- Reconstructed chronology without authoritative evidence

If a legitimate timestamp-bearing source can be obtained, it may be used.

If no legitimate timestamp-bearing source can be obtained, the limitation must be documented honestly.

---

## 3.4 Source Data vs Derived Data

Every data field must be classified as one of:

```text
SOURCE
DERIVED
PROXY
SYNTHETIC TEST DATA
```

Example:

| Data Type | Example | Interpretation |
|---|---|---|
| SOURCE | `rating` | Directly present in source |
| SOURCE | `votes` | Directly present in source |
| SOURCE | `product_name` | Directly present in source |
| DERIVED | `interaction_count` | Calculated from source |
| DERIVED | `average_rating` | Calculated from source |
| DERIVED | `popularity_score` | Calculated model feature |
| PROXY | Binary relevance from rating threshold | Derived evaluation definition |
| SYNTHETIC | Test-only mock interaction | Artificial test data |

---

## 3.5 Reproducibility

A reviewer must be able to determine:

1. Where the data came from.
2. How it was acquired.
3. How it was validated.
4. How it was processed.
5. How derived datasets were created.
6. Which version of the data was used.
7. How model-ready datasets were generated.

---

## 3.6 No Silent Data Transformation

Any transformation that changes the semantics or structure of the source data must be explicitly documented.

---

# 4. CURRENT DATASET BASELINE

The repository audit identifies the declared dataset as the:

> **Monash University FIT5212 S1 2025 Recommender System Challenge dataset, derived from Amazon product/review data.**

The audit reports that the dataset contains explicit user-item ratings and associated voting/helpfulness information.

The current repository's preprocessing code expects the following raw fields:

```text
user_id
product_id
product_name
rating
votes
helpful_votes
```

The official competition dataset description also identifies `train.csv` as containing explicit user-item ratings from 1 to 5, together with user ID, product ID, product name, votes, and helpful votes. The competition describes `test.csv` as containing user/item pairs for which ratings are to be predicted. 

---

# 5. CURRENT DATA AVAILABILITY AUDIT

The repository audit identified the following state.

| File | Expected Role | Current Audit State |
|---|---|---|
| `data/raw/train.csv` | Raw training source | Missing |
| `data/raw/test.csv` | Raw competition/test source | Missing |
| `data/processed/interactions.csv` | Processed interaction table | Missing |
| `data/processed/products.csv` | Product entity table | Missing |
| `data/processed/users.csv` | User summary table | Present |
| `data/processed/popular_products.csv` | Popularity artifact | Present |
| `data/processed/user_segment_summary.csv` | User segmentation artifact | Present |

The audit states that the missing raw and processed datasets currently prevent the preprocessing pipeline, recommendation models, recommendation engine, application, and tests from executing normally.

The repository also lacks an automated data-acquisition mechanism capable of rebuilding the missing dataset artifacts from scratch.

---

# 6. DATA SOURCE PROVENANCE

## 6.1 Declared Source

The repository documentation identifies the dataset as originating from the:

> Monash University FIT5212 S1 2025 Recommender System Challenge.

The competition describes its dataset as being collected by crawling Amazon and containing product metadata and review information.

The competition's published description states that the data covers approximately 219,859 different products and that the user-item interaction data is split into training and test sets.

---

## 6.2 Source Verification Policy

Before restoring the missing dataset, the implementation phase must verify:

- Dataset name
- Dataset owner/source
- Dataset version
- Competition/version context
- File names
- File schema
- Download source
- Applicable license/competition rules
- File integrity

The exact downloaded artifact must be documented.

---

## 6.3 Source Version

The project must avoid mixing:

- Different competition versions
- Different Kaggle datasets
- Different Amazon review snapshots
- Different preprocessing versions

unless the combination is explicitly justified and documented.

---

# 7. LEGITIMATE DATA RECOVERY STRATEGY

Because the repository does not contain the raw dataset, data recovery is a P0 task.

The preferred recovery hierarchy is:

```text
Official / Authoritative Dataset Source
            ↓
Official Competition Dataset
            ↓
Verified Corresponding Dataset Version
            ↓
Documented Secondary Mirror
            ↓
Manual Data Acquisition
```

The final project should prefer the highest-authority available source.

---

# 8. DATA RECOVERY WORKFLOW

## Step 1 — Verify Source

Confirm that the dataset corresponds to the repository's documented FIT5212 S1 2025 dataset.

---

## Step 2 — Acquire Raw Files

Obtain the required files:

```text
train.csv
test.csv
```

from the legitimate source.

---

## Step 3 — Preserve Raw Files

Place raw files under:

```text
data/raw/
```

subject to repository licensing and size constraints.

If redistribution is not appropriate, the project should provide a reproducible download procedure rather than committing restricted data.

---

## Step 4 — Validate File Integrity

Verify:

- File exists
- File is readable
- CSV is parseable
- Required columns exist
- Row count is plausible
- Identifier columns are populated
- Rating domain is valid

---

## Step 5 — Record Dataset Metadata

Record:

- Source
- Acquisition date
- Dataset version
- File size
- Row count
- Column count
- Schema
- Optional checksum

---

## Step 6 — Run Data Validation

The dataset must pass the project's validation checks before preprocessing.

---

## Step 7 — Generate Processed Artifacts

Only after validation should the pipeline generate:

```text
interactions.csv
products.csv
users.csv
popular_products.csv
```

and other derived artifacts.

---

# 9. RAW DATA POLICY

Raw data must be treated as immutable.

The preprocessing pipeline must never overwrite the original source files.

Preferred structure:

```text
data/
├── raw/
│   ├── train.csv
│   └── test.csv
│
├── interim/
│   └── ...
│
└── processed/
    ├── interactions.csv
    ├── products.csv
    ├── users.csv
    └── popular_products.csv
```

If the source dataset cannot legally or practically be committed to GitHub, only the acquisition instructions and metadata should be committed.

---

# 10. RAW DATA SCHEMA

The audited preprocessing implementation expects:

| Column | Type | Meaning | Source/Derived |
|---|---|---|---|
| `user_id` | String | User identifier | Source |
| `product_id` | String | Product identifier | Source |
| `product_name` | String | Product title/name | Source |
| `rating` | Numeric | Explicit user rating | Source |
| `votes` | Numeric | Number of votes associated with rating | Source |
| `helpful_votes` | Numeric | Number of helpful votes | Source |

The official competition description also identifies an `ID` field in the competition files.

The implementation must inspect the actual recovered file schema before deciding whether this field should be retained, ignored, or used only for competition-specific identification.

---

# 11. FIELD SEMANTICS

## 11.1 `user_id`

Represents the identifier assigned to a user.

Rules:

- Treat as categorical/string identifier.
- Do not interpret the numeric-looking value as a continuous variable.
- Preserve leading zeros if present.
- Standardize type consistently across all pipeline stages.

Preferred internal representation:

```python
str
```

---

## 11.2 `product_id`

Represents the identifier assigned to a product.

Rules:

- Treat as categorical/string identifier.
- Do not interpret as numeric magnitude.
- Preserve identifier semantics.
- Use consistent string representation.

---

## 11.3 `product_name`

Represents the product title/name.

Used primarily for:

- Content-based recommendation
- Product display
- Product metadata

Potential preprocessing:

- Missing-value handling
- Whitespace normalization
- Text vectorization

Text transformations must not alter the original raw value.

---

## 11.4 `rating`

Represents explicit user feedback.

Expected domain:

```text
1.0 ≤ rating ≤ 5.0
```

The audited preprocessing implementation filters ratings outside this range.

Rating is the primary explicit interaction signal currently available.

---

## 11.5 `votes`

Represents the number of votes associated with a rating.

It is not a user-product interaction event such as:

- Click
- View
- Cart
- Purchase

It must not be interpreted as one.

---

## 11.6 `helpful_votes`

Represents the number of votes indicating that the associated rating/review was helpful.

It is metadata about the rating/review.

It must not be interpreted as purchase or engagement events.

---

# 12. OFFICIAL INTERACTION REQUIREMENT VS DATA REALITY

The official project description asks for user-item interaction data derived from:

- Views
- Clicks
- Carts
- Purchases

The currently audited dataset does not provide those event types.

It provides explicit ratings instead.

Therefore the project shall use the following policy:

```text
Official Requirement
        ↓
Expected multi-action behavior data
        ↓
Available dataset
        ↓
Explicit ratings only
        ↓
Do NOT fabricate missing event types
        ↓
Document dataset limitation
        ↓
Use legitimate rating-based recommendation methodology
```

---

# 13. RATING-BASED INTERACTION STRATEGY

The current dataset supports an explicit-feedback recommendation formulation.

A user-item interaction can therefore be represented as:

```text
(user_id, product_id, rating)
```

with optional supporting metadata:

```text
votes
helpful_votes
product_name
```

The project may create derived representations such as:

### Explicit Rating Matrix

```text
Rows    = Users
Columns = Products
Values  = Ratings
```

---

# 14. BINARY RELEVANCE REPRESENTATION

For ranking evaluation, the project may derive a binary relevance label from ratings.

The current repository methodology uses:

```text
rating >= 4
```

as the relevant threshold.

Therefore:

```text
rating >= 4  → relevant
rating < 4   → non-relevant
```

This is a **derived evaluation definition**, not a source-data event.

The threshold must be configurable and documented.

It must not be described as a purchase/click indicator.

---

# 15. WHY RATINGS MUST NOT BE CONVERTED INTO FAKE EVENTS

A mapping such as:

```text
rating = 1 → view
rating = 2 → click
rating = 3 → cart
rating = 4 → purchase
rating = 5 → purchase
```

would invent behavioral semantics that do not exist in the source.

Likewise:

```text
votes → clicks
helpful_votes → purchases
```

would be semantically invalid.

Therefore this project shall not use such mappings.

---

# 16. OPTIONAL DERIVED INTERACTION WEIGHT

If the recommendation methodology requires a single interaction-strength value, it may use the explicit rating itself or a documented transformation of the rating.

For example:

```text
interaction_strength = normalized_rating
```

where:

```text
normalized_rating = (rating - 1) / 4
```

produces:

```text
1-star → 0.00
2-star → 0.25
3-star → 0.50
4-star → 0.75
5-star → 1.00
```

This remains a rating-derived preference signal.

It must not be described as a behavioral event.

The exact transformation shall be finalized in:

`ML_METHODOLOGY.md`

---

# 17. DUPLICATE INTERACTION STRATEGY

The existing preprocessing implementation currently performs:

```python
drop_duplicates(subset=["user_id", "product_id"])
```

This means multiple user-product observations are reduced to one row.

This behavior must be reviewed before final implementation.

The preferred decision must depend on the actual recovered dataset.

---

## 17.1 Duplicate Questions

The implementation must determine:

1. Are duplicate user-product rows legitimate?
2. Do they represent multiple reviews?
3. Does the dataset guarantee uniqueness?
4. Is one observation intended to represent one rating?
5. If duplicates exist, should they be:
   - Aggregated?
   - Retained?
   - Latest record selected?
   - Maximum/mean rating selected?

Because the current dataset has no legitimate timestamp field, selecting a "latest" record cannot be done unless another authoritative ordering field exists.

---

# 18. RECOMMENDED DUPLICATE POLICY

The final pipeline shall not blindly drop duplicates without first measuring them.

The preprocessing workflow should:

```text
Load raw data
      ↓
Count duplicate user-product pairs
      ↓
Inspect duplicate distributions
      ↓
Determine dataset semantics
      ↓
Choose aggregation/retention rule
      ↓
Document rule
      ↓
Generate processed interactions
```

The final choice must be evidence-based.

---

# 19. MISSING-VALUE STRATEGY

The audited preprocessing implementation currently uses:

```text
Missing user_id       → drop
Missing product_id    → drop
Missing rating        → drop
Missing product_name  → "Unknown Product"
Missing votes         → 0
Missing helpful_votes → 0
```

This is a reasonable starting point, but it must be revalidated against the recovered dataset.

---

# 20. REQUIRED MISSING-VALUE RULES

## User ID

Rows without `user_id` shall be removed.

Reason:

A recommendation system cannot associate the interaction with a user.

---

## Product ID

Rows without `product_id` shall be removed.

Reason:

The interaction cannot be associated with an item.

---

## Rating

Rows without a valid rating shall be excluded from the explicit-rating interaction dataset unless a separate legitimate interaction signal exists.

---

## Product Name

Missing product names may be represented internally as:

```text
Unknown Product
```

but the original raw field must remain unchanged.

---

## Votes

Missing votes may be represented as:

```text
0
```

provided that missingness semantically means "no recorded votes" rather than unknown.

---

## Helpful Votes

Missing helpful votes may similarly be represented as:

```text
0
```

if appropriate to the recovered source schema.

---

# 21. TYPE VALIDATION

The preprocessing pipeline shall explicitly validate:

```text
user_id          → string
product_id       → string
product_name     → string
rating           → numeric
votes            → numeric
helpful_votes    → numeric
```

Numeric fields must be safely coerced.

Invalid numeric values should become missing and then be handled according to the missing-data policy.

---

# 22. RATING DOMAIN VALIDATION

Valid ratings are expected to satisfy:

```text
1 ≤ rating ≤ 5
```

Any value outside this domain must be:

1. Reported.
2. Excluded or corrected only if authoritative evidence supports correction.

The pipeline must not silently clip:

```text
6 → 5
0 → 1
```

because that changes source semantics.

---

# 23. USER ENTITY TABLE

The project shall derive a user-level table.

Possible fields include:

```text
user_id
interaction_count
unique_product_count
average_rating
rating_std
total_votes
total_helpful_votes
```

Additional fields may be added if justified.

The user table is derived data.

---

# 24. PRODUCT ENTITY TABLE

The project shall derive a product-level table.

Possible fields include:

```text
product_id
product_name
interaction_count
unique_user_count
average_rating
rating_std
total_votes
total_helpful_votes
```

These fields should be calculated only from data permitted by the relevant training/evaluation context when they are used as model features.

---

# 25. IMPORTANT LEAKAGE RULE FOR ENTITY TABLES

A global entity table is safe for descriptive reporting only if it does not feed evaluation-time predictions.

For model evaluation:

```text
Training Data
     ↓
Training-Derived User/Product Features
     ↓
Model
     ↓
Validation/Test
```

must be used.

The project must not calculate model features using validation/test observations before evaluating the model.

---

# 26. PRODUCT METADATA STRATEGY

The primary currently available product metadata is:

```text
product_id
product_name
```

This may support a TF-IDF content-based recommendation model.

The project should inspect whether additional legitimate product metadata exists in the recovered source.

If additional metadata is unavailable, the content-based model must be described as:

> **Product-name/text-based content recommendation**

rather than as a rich product-metadata recommender.

---

# 27. CONTENT FEATURE STRATEGY

Potential content representation:

```text
product_name
      ↓
Text preprocessing
      ↓
TF-IDF vectorization
      ↓
Product feature matrix
      ↓
Cosine similarity
```

The exact methodology will be specified in:

`ML_METHODOLOGY.md`

---

# 28. TF-IDF LEAKAGE PREVENTION

The audit identified that the current evaluation implementation fits TF-IDF over the entire product table, including products appearing in the validation data.

This must be reviewed.

The final evaluation design shall ensure that the content-model fitting process does not leak evaluation-specific information into the model in a way that affects measured performance.

At minimum, the pipeline must clearly distinguish:

```text
Training-period content/model fitting
```

from:

```text
Validation-period recommendation evaluation
```

---

# 29. USER-ITEM MATRIX STRATEGY

The project may construct a sparse matrix:

```text
              Product 1  Product 2  Product 3 ...
User 1           5.0        0         3.0
User 2           0          4.0       0
User 3           2.0        0         5.0
...
```

where:

```text
0 = no observed interaction
```

However, the implementation must distinguish between:

```text
missing interaction
```

and:

```text
actual rating of zero
```

because zero is outside the valid rating domain.

Sparse representations should be preferred where appropriate.

---

# 30. SPARSITY STRATEGY

The user-item matrix is expected to be sparse.

The project should:

- Use sparse matrices where practical.
- Avoid unnecessary dense matrix construction.
- Document matrix dimensions.
- Document sparsity.
- Monitor memory usage.

---

# 31. MINIMUM SUPPORT / K-CORE STRATEGY

The existing preprocessing does not perform minimum-support filtering.

The final strategy must not introduce arbitrary filtering simply to make the dataset easier to model.

Instead, the project should evaluate:

- Number of users with one interaction
- Number of users with few interactions
- Number of products with one interaction
- Long-tail distribution
- Effect of filtering on coverage
- Effect of filtering on cold-start evaluation

If filtering is necessary, it must be documented.

---

# 32. FILTERING POLICY

Any user/item support threshold must specify:

```text
Threshold
Reason
Affected rows
Affected users
Affected products
Effect on sparsity
Effect on cold start
Effect on evaluation
```

---

# 33. IMPORTANT EXISTING DATA DISTRIBUTION FINDING

The audit reports that the existing processed user population contains approximately:

```text
2,000 active users
```

and that the mean interaction count is approximately:

```text
373 interactions/user
```

This distribution explains why the existing hard-coded user segments:

```text
Low    < 3
Medium 3–10
High   > 10
```

collapse almost entirely into the High Activity segment.

The final pipeline must recompute all such statistics after legitimate dataset restoration rather than blindly reusing existing derived artifacts.

---

# 34. USER SEGMENT DATA STRATEGY

The final segmentation should be based on the actual distribution.

Potential strategy:

```text
Interaction Count
        ↓
Distribution Analysis
        ↓
Quantiles / Data-Driven Thresholds
        ↓
Meaningful Segments
```

Possible example:

```text
Low Activity
Medium Activity
High Activity
```

using quantiles rather than fixed thresholds.

The exact thresholds must be determined after the restored dataset is analyzed.

---

# 35. SEGMENTATION DATA IS NOT MODEL TRAINING DATA

User segments may be used for analysis.

However, segment definitions must not accidentally leak evaluation information into the recommendation model.

If segment-level recommendation quality is evaluated, the segmentation process must follow the same temporal/data-isolation rules as other evaluation features.

---

# 36. POPULARITY DATA STRATEGY

The existing popularity model uses:

```text
minimum interactions = 5
```

and:

```text
popularity_score =
average_rating × interaction_count
```

This is a valid baseline formulation to preserve initially.

However, it must be recomputed from the appropriate training data during final evaluation.

---

# 37. TEMPORAL POPULARITY REQUIREMENT

If a legitimate timestamp-bearing dataset becomes available, popularity for a historical evaluation point must be calculated only from interactions available before that point.

For example:

```text
Historical Training Period
        ↓
Popularity Statistics
        ↓
Recommendation
        ↓
Future Validation Period
```

Future interaction counts must not influence the historical popularity score.

---

# 38. CURRENT TIMESTAMP STATUS

The repository audit found no timestamp field such as:

```text
timestamp
created_at
unix_time
```

in the audited dataset.

Therefore the existing random 80/20 per-user split is not a valid time-based validation strategy.

The project must resolve this through legitimate source investigation rather than synthetic timestamp generation.

---

# 39. TIMESTAMP RECOVERY STRATEGY

This is a critical Project 3 data task.

The investigation shall proceed in the following order:

```text
1. Inspect repository documentation
        ↓
2. Identify exact dataset/version
        ↓
3. Inspect authoritative competition source
        ↓
4. Inspect official dataset files/schema
        ↓
5. Determine whether timestamp fields exist
        ↓
6. Search for an authoritative corresponding dataset version
        ↓
7. Compare schemas and identifiers
        ↓
8. Determine whether timestamps can legitimately be joined/restored
        ↓
9. Validate temporal semantics
        ↓
10. Use timestamps only if provenance is defensible
```

---

# 40. TIMESTAMP RECOVERY — ACCEPTABLE SOURCES

A timestamp may be used if it originates from:

1. The original authoritative dataset.
2. An authoritative version of the same dataset.
3. A documented corresponding source containing the same underlying interaction records.
4. A legitimate metadata table with a one-to-one or otherwise defensible mapping to the source interactions.

The relationship must be demonstrated rather than assumed.

---

# 41. TIMESTAMP RECOVERY — UNACCEPTABLE SOURCES

The following are not acceptable:

- Randomly generated timestamps.
- Sequential timestamps based on row order.
- Timestamps inferred from product IDs.
- Timestamps inferred from user IDs.
- Timestamps copied from unrelated datasets.
- Dates invented from file ordering.
- Dates generated solely to make a chronological split possible.

---

# 42. TIMESTAMP JOIN VALIDATION

If an external timestamp-bearing source is discovered, it must be validated.

Potential join keys:

```text
user_id + product_id
```

or, where available:

```text
unique interaction ID
```

The join must be tested for:

- Match rate
- Duplicate matches
- Missing timestamps
- Conflicting timestamps
- One-to-many relationships
- Many-to-one relationships

A timestamp join must not be used merely because it produces a high match rate.

---

# 43. TIMESTAMP SEMANTICS

A timestamp is useful for temporal validation only if it actually represents the temporal occurrence of the interaction.

For example:

```text
review_created_at
interaction_time
purchase_time
```

may be suitable depending on the source semantics.

A timestamp representing:

```text
dataset download time
processing time
crawl time
file modification time
```

would not necessarily represent user interaction chronology.

The final project must document the meaning of any timestamp used.

---

# 44. TEMPORAL VALIDATION STRATEGY

If a legitimate timestamp is recovered:

```text
All valid interactions
        ↓
Sort by timestamp
        ↓
Choose temporal cutoff
        ↓
Training period
        ↓
Validation period
        ↓
Optional final test period
```

The model must never use future interactions when predicting earlier interactions.

---

# 45. USER-WISE TEMPORAL SPLIT

Where the dataset supports it, the project may use a global temporal cutoff or another explicitly justified chronological strategy.

The selected strategy must preserve realistic recommendation conditions.

For example:

```text
Training:
All interactions before cutoff

Validation:
Interactions after cutoff
```

The exact approach will be finalized in:

`EXPERIMENT_PLAN.md`

and:

`EVALUATION_AND_ERROR_ANALYSIS.md`

---

# 46. COLD-START DATA STRATEGY

The data pipeline must preserve the information necessary to evaluate cold-start scenarios.

The project should distinguish:

### New User

User absent from training interactions.

### Sparse User

User with insufficient training history.

### New Product

Product absent from training interactions but available in product metadata.

### Sparse Product

Product with very few training interactions.

---

# 47. NEW USER DATA HANDLING

A new user cannot be processed by standard collaborative filtering without history.

Therefore the data layer must support a fallback path.

Potential fallback:

```text
New User
   ↓
Popularity
```

or, where context is available:

```text
New User
   ↓
Context/Product Selection
   ↓
Content-Based Recommendation
```

The exact strategy belongs to `ML_METHODOLOGY.md`.

---

# 48. NEW PRODUCT DATA HANDLING

A new product with valid metadata should not automatically be discarded merely because it has no historical interactions.

The content-based system should be capable of representing the product from its metadata.

This directly addresses the current candidate-pool restriction identified in the audit.

---

# 49. CANDIDATE COVERAGE REQUIREMENT

The data pipeline must not define:

```text
Candidate Products = Top 1,000 Popular Products
```

as the only possible candidate pool.

Such a restriction can prevent long-tail and cold-start products from ever reaching the content-based stage.

Candidate generation must be designed according to the recommendation methodology.

---

# 50. TRAINING DATA STRATEGY

The final training dataset must contain only information permitted by the evaluation protocol.

For temporal evaluation:

```text
TRAIN
  ↓
Models
  ↓
Recommendations
```

must be isolated from:

```text
VALIDATION
```

and:

```text
TEST
```

---

# 51. VALIDATION DATA STRATEGY

Validation data is used to:

- Evaluate ranking quality.
- Compare models.
- Tune approved hyperparameters where appropriate.
- Analyze errors.

Validation data must not be used to train the final model before its performance is reported.

---

# 52. FINAL TEST DATA STRATEGY

If a final test set exists, it must remain isolated until the final evaluation stage.

The project must avoid repeatedly using the final test set to make modeling decisions.

---

# 53. CURRENT `train.csv` AND `test.csv` INTERPRETATION

The official competition description indicates:

### `train.csv`

Contains historical user-item ratings and associated information.

### `test.csv`

Contains user-item pairs for which ratings were intended to be predicted in the competition.

The project's offline ranking evaluation requirements are different from simply reproducing a competition submission.

Therefore, the final evaluation design must explicitly define which dataset partition is used for:

- Model training
- Offline validation
- Final testing

rather than assuming that the competition's `test.csv` automatically represents the required temporal validation set.

---

# 54. IMPORTANT DISTINCTION: COMPETITION TEST VS PROJECT VALIDATION

The project must distinguish between:

```text
Competition Test File
```

and:

```text
Offline Temporal Validation Set
```

They are not automatically equivalent.

The official competition test structure may contain user-item pairs without observed ratings, whereas ranking evaluation requires a known relevance signal.

Therefore the final evaluation strategy must establish a valid evaluation target before using any dataset partition for Precision@K, Recall@K, or NDCG@K.

---

# 55. RELEVANCE TARGET STRATEGY

For ranking evaluation, the project requires a ground-truth set of relevant items.

With explicit ratings, the current repository methodology uses:

```text
rating >= 4
```

as the relevant threshold.

The final methodology shall document:

- Threshold
- Why it is used
- Whether it is binary or graded
- Which ratings are considered relevant
- How ties/duplicates are handled

---

# 56. PRECISION@K DATA REQUIREMENT

For each eligible evaluation user:

```text
Recommended Top-K Items
          +
Ground-Truth Relevant Items
          ↓
Precision@K
```

The ground-truth relevant items must come from held-out evaluation data.

They must not be derived from training observations.

---

# 57. RECALL@K DATA REQUIREMENT

Recall@K requires the complete set of relevant held-out items for the user, subject to the defined evaluation protocol.

The system must avoid artificially restricting the ground-truth set to only the recommended candidates.

---

# 58. NDCG@K DATA REQUIREMENT

NDCG@K may use:

### Binary relevance

```text
Relevant = 1
Non-relevant = 0
```

or:

### Graded relevance

Potentially based on rating magnitude.

The chosen strategy must be explicitly documented.

---

# 59. DATA LEAKAGE CONTROL MATRIX

| Data Component | Training Allowed | Validation Allowed | Future Test Allowed |
|---|---:|---:|---:|
| User history before cutoff | Yes | No | No |
| User history after cutoff | No | Evaluation only | Evaluation only |
| Training popularity | Yes | Derived from train only | Derived from permitted train |
| Validation popularity | No | Yes for analysis only | No |
| Training TF-IDF fitting | Yes | No | No |
| Validation labels | No | Yes | No |
| Test labels | No | No | Yes only at final stage |
| Future interactions | No | No | No |

---

# 60. LEAKAGE RISKS TO MONITOR

The implementation must explicitly inspect for:

1. Global popularity computed using future data.
2. TF-IDF fitted on evaluation-specific information where inappropriate.
3. User features calculated using held-out interactions.
4. Product features calculated using future interactions.
5. Segment assignments using future information.
6. Hyperparameter tuning against final test data.
7. Duplicate records appearing across train and validation.
8. Candidate generation using held-out relevance information.

---

# 61. USER/PRODUCT IDENTITY LEAKAGE

The same identifier appearing in training and validation is not itself leakage.

For example:

```text
User A
Training interaction → Product 1
Validation interaction → Product 2
```

is expected in personalized recommendation evaluation.

The issue is whether information about the validation interaction itself is exposed during training.

---

# 62. DATASET VERSION CONTROL

The project should record a dataset metadata file such as:

```text
data/dataset_metadata.json
```

or an equivalent documented artifact.

Suggested fields:

```json
{
  "dataset_name": "...",
  "source": "...",
  "version": "...",
  "acquisition_date": "...",
  "train_filename": "train.csv",
  "test_filename": "test.csv",
  "row_count": "...",
  "column_count": "...",
  "timestamp_available": false,
  "notes": "..."
}
```

The exact implementation format may differ.

---

# 63. DATA CHECKSUM STRATEGY

Where raw data is too large or restricted to commit to GitHub, checksums should be considered.

Potential metadata:

```text
SHA-256
```

This allows the project to verify that the acquired file corresponds to the documented dataset artifact.

---

# 64. PROCESSED DATA ARTIFACTS

The expected processed data layer should include:

```text
data/processed/
├── interactions.csv
├── products.csv
├── users.csv
├── popular_products.csv
└── user_segment_summary.csv
```

Additional artifacts may be created when justified.

---

# 65. `interactions.csv`

Purpose:

Canonical processed user-item interaction table.

Expected fields may include:

```text
user_id
product_id
product_name
rating
votes
helpful_votes
```

Optional derived fields may include:

```text
interaction_strength
relevance
```

but must be clearly identified as derived.

---

# 66. `products.csv`

Purpose:

Canonical product entity table.

Expected fields:

```text
product_id
product_name
```

plus legitimate derived statistics where appropriate.

---

# 67. `users.csv`

Purpose:

Canonical user entity/summary table.

Potential fields:

```text
user_id
interaction_count
unique_product_count
average_rating
```

plus other justified statistics.

---

# 68. `popular_products.csv`

Purpose:

Popularity ranking artifact.

Potential fields:

```text
product_id
product_name
interaction_count
average_rating
popularity_score
rank
```

This artifact must be regenerated from the correct training data when used for evaluation.

---

# 69. `user_segment_summary.csv`

Purpose:

User segmentation summary.

Potential fields:

```text
segment
users
average_interactions
average_rating
average_products
```

The final version should additionally support recommendation-quality analysis where required.

---

# 70. INTERMEDIATE DATA

The project may use:

```text
data/interim/
```

for temporary transformations such as:

- Cleaned raw data
- Deduplicated data
- Training-only features
- Evaluation-specific data

Intermediate artifacts should not be confused with final processed datasets.

---

# 71. DATA PIPELINE CONTRACT

The data pipeline should conceptually implement:

```text
load_raw_data()
        ↓
validate_raw_schema()
        ↓
validate_values()
        ↓
clean_data()
        ↓
resolve_duplicates()
        ↓
construct_interactions()
        ↓
construct_users()
        ↓
construct_products()
        ↓
save_processed_data()
```

Evaluation-specific processing should remain separate from generic preprocessing where necessary.

---

# 72. RECOMMENDED DATA MODULE RESPONSIBILITIES

Existing modules should be preserved where appropriate.

Potential responsibilities:

### `inspect_dataset.py`

Inspect:

- Shape
- Columns
- Nulls
- Unique counts
- Basic distributions

---

### `analyze_dataset.py`

Produce:

- Dataset statistics
- Distribution analysis
- Data-quality report

---

### `preprocess_data.py`

Perform:

- Cleaning
- Type conversion
- Validation
- Interaction construction

---

### `create_entities.py`

Produce:

- User table
- Product table

---

### `data_utils.py`

Provide:

- Loading
- Saving
- Column validation
- Reusable data helpers

---

# 73. DATA VALIDATION CHECKLIST

Before model training, the following checks must pass.

## File Checks

- [ ] Required raw file exists.
- [ ] Required test file exists if applicable.
- [ ] Files are readable.
- [ ] File format is valid.

---

## Schema Checks

- [ ] Required columns exist.
- [ ] Column names are correct.
- [ ] Data types are valid.

---

## Identifier Checks

- [ ] No invalid user IDs.
- [ ] No invalid product IDs.
- [ ] IDs are consistently represented as strings.

---

## Rating Checks

- [ ] Ratings are numeric.
- [ ] Ratings are within valid domain.
- [ ] Invalid ratings are handled.

---

## Missing Data Checks

- [ ] Null user IDs handled.
- [ ] Null product IDs handled.
- [ ] Null ratings handled.
- [ ] Product-name nulls handled.
- [ ] Vote fields handled.

---

## Duplicate Checks

- [ ] Duplicate user-product pairs measured.
- [ ] Duplicate policy applied.
- [ ] Result documented.

---

## Leakage Checks

- [ ] No train/validation overlap in evaluation observations.
- [ ] No future feature leakage.
- [ ] No validation information used during training.

---

# 74. DATA QUALITY REPORT

The final pipeline should generate a data-quality report containing at least:

```text
Dataset shape
Number of users
Number of products
Number of interactions
Missing-value counts
Duplicate counts
Rating distribution
Interaction distribution
Product support distribution
User support distribution
Timestamp availability
```

---

# 75. EXPECTED DATA STATISTICS

The audit currently reports:

```text
~745,889 claimed interactions/ratings
~2,001 users
~201,325 unique products reported in existing project artifacts
33,074 products in the existing popularity artifact after minimum-support filtering
```

These numbers are **audit-era repository findings**, not permanent assumptions.

After dataset restoration, the pipeline must recompute the statistics directly from the recovered raw files.

The project must not hardcode these values as authoritative if the restored source produces different verified counts.

---

# 76. IMPORTANT COUNT RECONCILIATION

Because existing repository artifacts and the authoritative source may differ due to:

- Filtering
- Deduplication
- Dataset version
- Preprocessing
- Competition-specific splits

the project must explicitly reconcile:

```text
Raw rows
    ↓
Valid rows
    ↓
Unique interactions
    ↓
Unique users
    ↓
Unique products
    ↓
Products after support filtering
```

The final report should explain every major reduction.

---

# 77. DATASET CARD REQUIREMENT

The project should maintain a dataset summary containing:

### Dataset Name

Monash University FIT5212 S1 2025 Recommender System Challenge dataset.

### Domain

Amazon products/reviews.

### Data Type

Explicit user-item ratings and review metadata.

### Users

To be recomputed from restored source.

### Products

To be recomputed from restored source.

### Interactions

To be recomputed from restored source.

### Rating Range

1–5.

### Event Types

Explicit ratings; no separate views/clicks/carts/purchases in the audited source.

### Timestamp

Not present in the audited source.

### Limitations

Documented explicitly.

---

# 78. DATASET LIMITATIONS

The following limitations are currently known.

## Limitation 1 — No Multi-Action Events

The source does not contain:

- Views
- Clicks
- Carts
- Purchases

as separate interaction types.

---

## Limitation 2 — No Timestamp

The audited source lacks a legitimate interaction timestamp.

---

## Limitation 3 — Explicit Feedback

The source is primarily explicit rating data.

---

## Limitation 4 — Sparse/Long-Tail Distribution

The product/user distribution requires analysis before final filtering decisions.

---

## Limitation 5 — Missing Repository Data

The repository currently lacks critical raw/processed files.

---

# 79. DATA STRATEGY RESPONSE TO LIMITATIONS

The project response must be:

```text
Missing data
    ↓
Recover legitimate source

Missing interaction types
    ↓
Do not fabricate
    ↓
Document limitation
    ↓
Use rating-based methodology

Missing timestamps
    ↓
Investigate authoritative corresponding source
    ↓
If legitimate timestamp found → use it
    ↓
Otherwise → document non-compliance/limitation honestly

Sparse/imbalanced data
    ↓
Analyze distribution
    ↓
Use defensible modeling strategy

Missing processed artifacts
    ↓
Regenerate reproducibly
```

---

# 80. DATA ACQUISITION AUTOMATION

A reproducible acquisition mechanism should be added where legally and technically appropriate.

Possible design:

```text
src/data/
└── download_data.py
```

or:

```text
scripts/
└── download_data.py
```

The script should:

1. Verify source.
2. Download/acquire data.
3. Save to `data/raw/`.
4. Validate files.
5. Report success/failure.
6. Avoid silently overwriting valid files.

If authentication is required, credentials must not be hardcoded.

---

# 81. DATA DOWNLOAD SAFETY

The acquisition process must not:

- Download unrelated datasets.
- Overwrite user data without warning.
- Modify repository source code.
- Generate fake data when download fails.
- Silently fall back to a different dataset.

If the official source is unavailable, the pipeline must fail clearly.

---

# 82. DATASET FALLBACK POLICY

A different dataset must not be substituted merely because it is easier to use.

Any dataset substitution would require:

1. Explicit justification.
2. Requirement review.
3. Schema review.
4. Modeling review.
5. Documentation update.
6. Approval before implementation.

---

# 83. SYNTHETIC DATA POLICY

Synthetic data is allowed only for:

- Unit tests
- Integration tests
- Edge-case testing
- Development diagnostics

Synthetic data must never be used as:

- Final training evidence
- Final evaluation evidence
- Real-world dataset statistics
- Evidence of actual user behavior

Every synthetic dataset must be explicitly labeled.

---

# 84. DATA TESTING STRATEGY

Tests should include:

### Schema Tests

```text
Required columns exist
```

### Domain Tests

```text
1 <= rating <= 5
```

### Integrity Tests

```text
No null user/product identifiers
```

### Relationship Tests

```text
All product IDs in interactions exist in product table
```

where such referential integrity is expected.

---

# 85. TRAIN/VALIDATION CONSISTENCY

The final pipeline must ensure that the same entity encoding is used consistently.

For example:

```text
Training user ID
Validation user ID
```

must use identical normalization rules.

The same applies to product IDs.

---

# 86. USER ID TYPE CONSISTENCY

The audit identified a bug in Streamlit where:

```python
int(user_id)
```

was compared against a string-valued `user_id` column.

The final data strategy therefore mandates:

> `user_id` must be consistently represented as a string across ingestion, processing, modeling, API, Streamlit, and evaluation.

---

# 87. PRODUCT ID TYPE CONSISTENCY

The same rule applies to `product_id`.

Do not allow:

```text
integer product ID
```

in one module and:

```text
string product ID
```

in another.

---

# 88. DATA CONFIGURATION

Data paths should be centralized.

Preferred pattern:

```text
config/config.py
```

rather than scattering:

```python
"data/processed/interactions.csv"
```

throughout the repository.

---

# 89. CONFIGURATION REQUIREMENTS

Configuration should define, where appropriate:

```text
RAW_DATA_PATH
TEST_DATA_PATH
INTERACTIONS_PATH
PRODUCTS_PATH
USERS_PATH
POPULAR_PRODUCTS_PATH
TOP_K
MIN_INTERACTIONS
RATING_THRESHOLD
RANDOM_SEED
```

Temporal configuration should be added only when a legitimate timestamp source is available.

---

# 90. DATA PIPELINE OUTPUT CONTRACT

After successful preprocessing, the pipeline should guarantee:

```text
data/processed/interactions.csv exists
data/processed/products.csv exists
data/processed/users.csv exists
```

and any additional required artifact exists.

Each file must satisfy its schema contract.

---

# 91. FAILURE BEHAVIOR

The data pipeline should fail loudly when:

- Raw file is missing.
- Required column is missing.
- Data type is invalid.
- Dataset is empty.
- Rating domain is invalid.
- Required metadata cannot be recovered.

It should not silently create fake replacement data.

---

# 92. DATA PIPELINE LOGGING

The preprocessing process should report:

```text
Input file
Input rows
Rows removed
Rows retained
Duplicate count
Null counts
Unique users
Unique products
Final interaction count
Output paths
```

This creates an audit trail for data processing.

---

# 93. DATA VERSIONING STRATEGY

The project should maintain a clear distinction between:

```text
SOURCE VERSION
PROCESSING VERSION
MODEL VERSION
EVALUATION VERSION
```

A model result should ideally be traceable to:

```text
Dataset version
+
Processing configuration
+
Model configuration
+
Evaluation configuration
```

---

# 94. DATA LINEAGE

The final project should support the following lineage:

```text
Official Dataset
      │
      ▼
data/raw/train.csv
      │
      ▼
Validation
      │
      ▼
Cleaning
      │
      ▼
interactions.csv
      │
 ┌────┼──────────────┐
 ▼    ▼              ▼
Users Products    Popularity
 │      │              │
 └──────┼──────────────┘
        ▼
Recommendation Engine
        ▼
Evaluation
```

---

# 95. DATA-TO-MODEL CONTRACT

The recommendation models may consume only documented data fields.

For example:

### Popularity

```text
product_id
rating
interaction_count
```

### Collaborative Filtering

```text
user_id
product_id
rating / interaction strength
```

### Content-Based

```text
product_id
product_name
```

### Hybrid

Consumes model outputs rather than independently bypassing data contracts.

---

# 96. DATA-TO-EVALUATION CONTRACT

The evaluation system must consume:

```text
Training Data
+
Held-Out Ground Truth
+
Recommendation Outputs
```

It must not independently recreate a separate hidden dataset or recommendation heuristic.

---

# 97. DATA-TO-SEGMENT CONTRACT

User segmentation should consume user-level features derived from the appropriate data partition.

For final recommendation-quality evaluation:

```text
Training-derived user characteristics
        ↓
Segment assignment
        ↓
Recommendation generation
        ↓
Held-out evaluation
```

This avoids using future interaction counts to define historical user segments.

---

# 98. DATA COVERAGE METRICS

The final analysis should consider:

- User coverage
- Product coverage
- Interaction coverage
- Recommendation coverage
- Long-tail coverage

These are complementary to Precision@K, Recall@K, and NDCG@K.

---

# 99. COLD-START COVERAGE METRICS

Where practical, report:

```text
Percentage of products unseen during training
Percentage of users unseen during training
Percentage of sparse users
Percentage of sparse products
```

and evaluate fallback behavior separately.

---

# 100. DATA QUALITY GATES

## Gate A — Acquisition

- [ ] Legitimate source verified.
- [ ] Required files obtained.
- [ ] File integrity checked.

---

## Gate B — Schema

- [ ] Required fields present.
- [ ] Types valid.
- [ ] IDs consistent.

---

## Gate C — Quality

- [ ] Missing values handled.
- [ ] Duplicates measured.
- [ ] Rating domain valid.

---

## Gate D — Semantics

- [ ] Interaction meaning documented.
- [ ] No fabricated events.
- [ ] Derived fields labeled.

---

## Gate E — Temporal

- [ ] Timestamp availability determined.
- [ ] Timestamp provenance verified.
- [ ] Temporal strategy selected.
- [ ] No artificial chronology.

---

## Gate F — Leakage

- [ ] Training/validation isolation verified.
- [ ] Feature leakage checked.
- [ ] Popularity leakage checked.
- [ ] Content-model leakage checked.

---

## Gate G — Reproducibility

- [ ] Acquisition reproducible.
- [ ] Processing reproducible.
- [ ] Outputs reproducible.

---

# 101. DATA RECOVERY DECISION TREE

```text
Is official dataset available?
        │
       YES
        │
        ▼
Acquire official dataset
        │
        ▼
Validate schema
        │
        ▼
Continue
        │
       NO
        │
        ▼
Is an authoritative corresponding source available?
        │
       YES
        │
        ▼
Validate equivalence
        │
        ▼
Use only if defensible
        │
       NO
        │
        ▼
Document blocker
        │
        ▼
Do NOT fabricate replacement data
```

---

# 102. TIMESTAMP DECISION TREE

```text
Does recovered source contain legitimate timestamps?
                │
          ┌─────┴─────┐
         YES           NO
          │             │
          ▼             ▼
Validate semantics   Search authoritative
          │           corresponding source
          ▼             │
Use temporal split     ▼
                      Found?
                    ┌───┴───┐
                   YES      NO
                    │        │
                    ▼        ▼
             Validate join   Document
                    │        limitation
                    ▼        │
             Use temporal     ▼
             validation   No fabricated timestamps
```

---

# 103. FINAL DATA STRATEGY FOR TIMESTAMP REQUIREMENT

The project's preferred outcome is:

> Obtain a legitimate timestamp-bearing source corresponding to the project dataset and use it for chronological validation.

However:

> If such a source cannot be legitimately established, the project must explicitly document that the available dataset cannot satisfy the temporal-validation requirement rather than manufacture timestamps.

This is a deliberate methodological integrity rule.

---

# 104. FINAL DATA STRATEGY FOR MULTI-ACTION REQUIREMENT

The project's preferred outcome is:

> Use a legitimate dataset containing actual multi-action user behavior if such a dataset is part of the approved project source.

If the current approved dataset remains the FIT5212 rating dataset:

```text
Do not fabricate:
views
clicks
carts
purchases
```

Instead:

```text
Use explicit ratings
        ↓
Construct legitimate rating-based interactions
        ↓
Document limitation
        ↓
Build recommender correctly
```

---

# 105. DATA STRATEGY AND PROJECT ARCHITECTURE

The data layer must support the canonical recommendation architecture:

```text
             RAW DATA
                 │
                 ▼
          DATA VALIDATION
                 │
                 ▼
         DATA PREPROCESSING
                 │
        ┌────────┼─────────┐
        ▼        ▼         ▼
    INTERACTIONS USERS   PRODUCTS
        │                  │
        ▼                  ▼
 COLLABORATIVE         CONTENT MODEL
        │                  │
        └────────┬─────────┘
                 ▼
       CANONICAL ENGINE
                 │
                 ▼
             EVALUATION
```

---

# 106. DATA STRATEGY AND RECOMMENDATION ENGINE

The Recommendation Engine must consume the same validated data artifacts used by evaluation.

This avoids situations where:

```text
API → Dataset A
Streamlit → Dataset B
Evaluation → Dataset C
```

The target is:

```text
Validated Data
      ↓
Canonical Models
      ↓
Canonical Recommendation Engine
      ↓
API + Streamlit + Evaluation
```

---

# 107. DATA STRATEGY AND EVALUATION

The final evaluation must be built after the data foundation is restored.

The correct implementation order is:

```text
Restore Data
     ↓
Validate Data
     ↓
Establish Evaluation Split
     ↓
Build Training Data
     ↓
Train Models
     ↓
Generate Recommendations
     ↓
Evaluate
```

Not:

```text
Write Metrics
     ↓
Invent/Assume Data
     ↓
Generate Numbers
```

---

# 108. DATA STRATEGY AND REPRODUCIBILITY

A fresh clone should ideally support:

```text
Clone Repository
      ↓
Install Dependencies
      ↓
Acquire Dataset
      ↓
Validate Dataset
      ↓
Run Preprocessing
      ↓
Generate Processed Data
      ↓
Train Models
      ↓
Run Evaluation
      ↓
Run API / Streamlit
```

No undocumented manual file manipulation should be required.

---

# 109. DATA STRATEGY AND GITHUB

Because raw data may have size/licensing restrictions, the repository should not blindly commit large datasets.

The repository should instead contain, where appropriate:

```text
data/
├── README.md
├── raw/
│   └── .gitkeep
├── interim/
│   └── .gitkeep
└── processed/
    └── .gitkeep
```

plus:

```text
Data acquisition instructions
Dataset metadata
Validation instructions
```

The exact Git strategy will be defined in:

`GIT_GITHUB_STRATEGY.md`.

---

# 110. DATA REPRODUCIBILITY CHECKLIST

A final reviewer should be able to answer "YES" to:

- [ ] Is the dataset source documented?
- [ ] Is the dataset version identifiable?
- [ ] Can the raw data be acquired?
- [ ] Can preprocessing be reproduced?
- [ ] Are schema rules documented?
- [ ] Are missing-value rules documented?
- [ ] Are duplicate rules documented?
- [ ] Are interaction semantics documented?
- [ ] Is timestamp availability documented?
- [ ] Is temporal validation methodology documented?
- [ ] Is leakage prevention documented?
- [ ] Can processed artifacts be regenerated?
- [ ] Can model inputs be traced back to source data?

---

# 111. DATA STRATEGY ACCEPTANCE CRITERIA

## DS-AC-001 — Source

The exact dataset source/version is documented.

---

## DS-AC-002 — Acquisition

A legitimate acquisition procedure exists.

---

## DS-AC-003 — Raw Data

Raw data can be loaded successfully.

---

## DS-AC-004 — Schema

Required fields are validated.

---

## DS-AC-005 — Cleaning

Cleaning produces a documented valid dataset.

---

## DS-AC-006 — Interactions

User-item interactions are constructed correctly.

---

## DS-AC-007 — Products

Product entity data is generated correctly.

---

## DS-AC-008 — Users

User entity data is generated correctly.

---

## DS-AC-009 — Popularity

Popularity artifacts can be reproduced.

---

## DS-AC-010 — No Fabricated Events

No synthetic behavioral events are presented as source observations.

---

## DS-AC-011 — Timestamp Integrity

No artificial timestamps are used as real temporal observations.

---

## DS-AC-012 — Leakage

Training/evaluation leakage is prevented.

---

## DS-AC-013 — Reproducibility

Processed datasets can be regenerated.

---

# 112. DATA REQUIREMENT TRACEABILITY

| Requirement | Strategy |
|---|---|
| User-item interaction data | Explicit rating-based interaction representation |
| Views | Not available in audited source; do not fabricate |
| Clicks | Not available in audited source; do not fabricate |
| Carts | Not available in audited source; do not fabricate |
| Purchases | Not available in audited source; do not fabricate |
| Popularity baseline | Derived from legitimate training data |
| Product metadata | `product_id`, `product_name`, plus verified available metadata |
| Collaborative filtering | Sparse user-item representation |
| Matrix factorization | Sparse interaction representation |
| Content-based recommendation | Product-name/text representation |
| Cold-start | Preserve product metadata and full candidate coverage |
| Precision@K | Held-out relevant items |
| Recall@K | Held-out relevant items |
| NDCG@K | Held-out ranked relevance |
| Time-based validation | Legitimate timestamp source only |
| Segment analysis | Training-derived user characteristics |
| API | Processed/canonical data artifacts |
| Streamlit | Same canonical data/model pipeline |

---

# 113. DATA STRATEGY IMPLEMENTATION PRIORITY

## P0 — Must Resolve First

1. Dataset provenance.
2. Raw dataset recovery.
3. Schema verification.
4. Data-quality validation.
5. Missing processed data restoration.
6. Interaction semantics.
7. Timestamp investigation.
8. Leakage-safe evaluation data design.

---

## P1 — Must Resolve Before Final QA

1. Duplicate strategy.
2. Product/user entity generation.
3. Cold-start data support.
4. Segment data strategy.
5. Reproducible acquisition.
6. Dataset metadata.
7. Data-quality reporting.

---

## P2 — Quality Enhancements

1. Checksum support.
2. Expanded data diagnostics.
3. Coverage statistics.
4. Long-tail analysis.
5. Additional data-quality visualizations.

---

# 114. DATA STRATEGY DO-NOT-DO LIST

The implementation must NOT:

- Download an unrelated dataset because the intended source is inconvenient.
- Rename ratings to purchases.
- Rename votes to clicks.
- Rename helpful votes to carts.
- Generate fake timestamps.
- Assign timestamps from row order.
- Claim temporal validation without legitimate temporal information.
- Use future interactions to calculate historical popularity.
- Fit evaluation-sensitive features using held-out information.
- Delete raw data after preprocessing.
- Hardcode dataset statistics.
- Hardcode user segmentation thresholds without distribution analysis.
- Use missing data artifacts as if they were verified source data.
- Generate synthetic data and present it as real.
- silently substitute a different dataset.

---

# 115. FINAL DATA PIPELINE SPECIFICATION

The target pipeline is:

```text
                    ┌───────────────────────┐
                    │ Authoritative Source  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Raw Dataset Acquisition│
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Source / Schema Check │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Data Quality Checks   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Cleaning / Validation │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Interaction Builder   │
                    └───────────┬───────────┘
                                │
                  ┌─────────────┼─────────────┐
                  │             │             │
                  ▼             ▼             ▼
             Interactions     Users       Products
                  │             │             │
                  └─────────────┼─────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Evaluation Split      │
                    │ / Temporal Strategy   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Model-Ready Dataset   │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
         Popularity       Collaborative     Content-Based
              │                 │                 │
              └─────────────────┼─────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Recommendation Engine│
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Evaluation + Analysis │
                    └───────────────────────┘
```

---

# 116. FINAL DATA DECISION FRAMEWORK

Whenever a data-related implementation decision is required, use:

```text
Is the information present in the source?
            │
       ┌────┴────┐
      YES        NO
       │          │
       ▼          ▼
Use source     Can it be
semantics      legitimately
               derived?
                  │
             ┌────┴────┐
            YES        NO
             │          │
             ▼          ▼
         Label as     Document
         derived      limitation
                         │
                         ▼
                  Do not fabricate
```

---

# 117. FINAL DATA GOVERNANCE RULE

The following rule is absolute:

> **The dataset is not a resource that can be reshaped arbitrarily to satisfy an implementation requirement. The implementation requirements must respect what the dataset legitimately contains.**

Therefore:

```text
Data Reality
     ↓
Methodology
     ↓
Implementation
     ↓
Evaluation
```

rather than:

```text
Required Metric
     ↓
Invent Data
     ↓
Generate Result
```

---

# 118. FINAL DATA STRATEGY STATEMENT

The final Project 3 data foundation shall be:

> **Legitimate, reproducible, validated, semantically faithful, leakage-safe, and sufficient for defensible recommendation modeling and evaluation.**

The project will preserve the audited dataset's real characteristics:

- Explicit ratings
- Product identifiers
- User identifiers
- Product names
- Votes
- Helpful votes

while explicitly acknowledging the absence of:

- Views
- Clicks
- Carts
- Purchases
- Legitimate timestamps in the audited source

The project will actively investigate whether authoritative corresponding data can legitimately resolve the timestamp requirement.

If it can:

```text
Recover
    ↓
Validate
    ↓
Integrate
    ↓
Use for temporal validation
```

If it cannot:

```text
Document limitation
    ↓
Do not fabricate chronology
    ↓
Do not falsely claim compliance
```

The same integrity standard applies to interaction types.

---

# 119. FINAL DATA DEFINITION OF DONE

The data layer is considered complete only when:

```text
Dataset Source
      ↓
Verified

Raw Data
      ↓
Available / Reproducibly Acquirable

Schema
      ↓
Validated

Data Quality
      ↓
Validated

Interactions
      ↓
Correctly Represented

Users
      ↓
Generated

Products
      ↓
Generated

Timestamp
      ↓
Legitimately Resolved or Explicitly Documented

Train / Validation
      ↓
Leakage-Safe

Cold Start
      ↓
Supported by Data Design

Processed Artifacts
      ↓
Reproducible

Data Lineage
      ↓
Documented

Model Inputs
      ↓
Traceable to Source

Final Data Layer
      ↓
QA Verified
```

---

# 120. FINAL DATA STRATEGY STANDARD

The final standard for the data layer is not:

> "The CSV files exist."

It is:

> **"The origin, meaning, processing, limitations, temporal properties, evaluation role, and reproducibility of every important dataset component are understood and documented."**

The project must therefore prioritize:

```text
Data Integrity
      >
Data Convenience

Legitimate Source
      >
Easy Substitute

Real Semantics
      >
Artificial Compliance

Reproducibility
      >
Manual Reconstruction

Leakage Prevention
      >
Convenient Feature Engineering

Honest Limitation
      >
Fabricated Requirement Satisfaction
```

---

# 121. RELATIONSHIP WITH OTHER CONTROL DOCUMENTS

This document defines **what data exists, how it is acquired, validated, transformed, and partitioned**.

It does not define the complete recommendation algorithms.

Those responsibilities belong to:

### `ML_METHODOLOGY.md`

Defines:

- Collaborative filtering
- Matrix factorization
- Content-based recommendation
- Hybrid recommendation
- Candidate generation
- Ranking
- Cold-start modeling

---

### `EXPERIMENT_PLAN.md`

Defines:

- Experimental datasets
- Model experiments
- Hyperparameters
- Comparisons
- Ablations
- Reproducibility

---

### `EVALUATION_AND_ERROR_ANALYSIS.md`

Defines:

- Precision@K
- Recall@K
- NDCG@K
- Temporal evaluation
- Segment evaluation
- Error analysis
- Leakage controls

---

### `SYSTEM_ARCHITECTURE.md`

Defines:

- Data flow
- Components
- Module boundaries
- Application integration

---

# 122. FINAL AUTHORIZATION

No model-training or evaluation implementation should proceed against an unverified dataset.

Before the main implementation begins, the following must be resolved:

```text
[ ] Legitimate dataset source identified
[ ] Raw data restored/acquirable
[ ] Actual schema verified
[ ] Dataset statistics recomputed
[ ] Interaction semantics confirmed
[ ] Duplicate behavior analyzed
[ ] Missing values analyzed
[ ] Timestamp availability investigated
[ ] Timestamp provenance resolved or limitation documented
[ ] Evaluation data strategy defined
[ ] Leakage controls defined
```

Only after these conditions are sufficiently resolved should the project proceed to full modeling implementation.

---

# 123. FINAL DOCUMENT STATEMENT

`DATASET_AND_DATA_STRATEGY.md` establishes the authoritative data contract for Project 3.

The project shall build its recommendation system on:

> **what the data legitimately contains, not what would be convenient for the implementation.**

Every downstream model, evaluation result, API response, visualization, and report must ultimately be traceable to this data foundation.

---

**END OF DATASET_AND_DATA_STRATEGY.md**
