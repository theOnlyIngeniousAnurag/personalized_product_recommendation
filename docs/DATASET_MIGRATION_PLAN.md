# DATASET MIGRATION PLAN: FIT5212 → RETAILROCKET
## Project 3 — Personalized Product Recommendation Model
## Controlled Migration Architecture & Execution Plan

---

## 1. Why FIT5212 Is Being Replaced

The project was initially scaffolded around the **Monash University FIT5212 S1 2025 Recommender System Challenge** dataset. While Phase 1 was initially explored using FIT5212, a fundamental architectural mismatch exists between FIT5212 and the project specifications:

- FIT5212 consists solely of explicit 1–5 star rating reviews extracted from an Amazon crawl.
- FIT5212 contains **no event types** (no views, clicks, add-to-carts, or transactions).
- FIT5212 contains **no timestamps** (no event timestamps, review dates, or epoch seconds).
- Attempting to simulate clicks/views or invent timestamps would violate non-negotiable rules against data fabrication (Rules 1, 2, 7, 8, 9, 10, 11, 12).
- Therefore, to satisfy the required project capabilities authentically, the dataset is migrated to a true e-commerce behavioral benchmark: **RetailRocket**.

---

## 2. Internship Requirement Mismatch Analysis

| Specification Requirement | FIT5212 Capability | Status | Root Cause in FIT5212 |
|---|---|---|---|
| **1. User-item interaction data from views/clicks/carts/purchases** | Explicit 1–5 ratings only | **FAIL** | Only explicit post-purchase review ratings were provided; no clickstream log exists. |
| **2. Popularity baseline** | Mean rating / vote-weighted rating | **PARTIAL** | Can rank by review count, but cannot calculate click/view velocity or conversion rate. |
| **3. Collaborative filtering or matrix factorization** | User-item rating matrix (1–5) | **PASS** | SVD and item-item CF operate on explicit ratings. |
| **4. Item metadata for content-based fallback** | Product title text only (`product_name`) | **PARTIAL** | Titles exist, but no taxonomy, structured attributes, or category tree. |
| **5. Precision@K, Recall@K, NDCG@K using a TIME-BASED validation split** | Random user-holdout split only | **FAIL** | Dataset has zero temporal fields; genuine time-based splitting is impossible without data fabrication. |
| **6. Recommendation API** | FastAPI serving top-N recommendations | **PASS** | Functional endpoints exist (`/recommend/{user_id}`). |
| **7. Recommendation analysis for user segments** | Review activity quartiles | **PARTIAL** | Segmented by review count, not behavioral lifecycle (browsers vs. cart abandoners vs. buyers). |

---

## 3. Why RetailRocket Satisfies the Missing Requirements

1. **Authentic Multi-Type Interactions**: RetailRocket provides explicit clickstream events: `view`, `addtocart`, and `transaction`, matching requirement 1.
2. **True Time-Based Validation Split**: Every single record possesses an authentic Unix millisecond timestamp (`timestamp`), enabling genuine temporal validation splits (train on past, validate on subsequent period, test on final horizon) without data fabrication, satisfying requirement 5.
3. **Structured Item Metadata & Hierarchy**: RetailRocket provides structured property key-values and a multi-level category taxonomy (`category_tree.csv` and `item_properties_*.csv`), enabling true content-based fallback for cold-start items, satisfying requirement 4.
4. **Behavioral User Segmentation**: Visitors can be segmented authentically into behavioral cohorts:
   - *Casual Browsers* (views only)
   - *Active Evaluators* (high view volume + category diversity)
   - *Cart Abandoners* (add-to-cart events without transactions)
   - *Converting Customers* (completed purchases)
   This directly satisfies requirement 7.
5. **Implicit Feedback Matrix Factorization**: Supports standard implicit ALS (Hu, Koren, Volinsky) and implicit collaborative filtering with natural conversion weights ($1 \times \text{view} + 3 \times \text{cart} + 5 \times \text{purchase}$), satisfying requirement 3.

---

## 4. Source Provenance & Verification

- **Origin**: RetailRocket Recommender System Dataset published by RetailRocket.
- **Hosting**: Publicly hosted on Kaggle (`retailrocket/ecommerce-dataset`).
- **Files**: `events.csv`, `category_tree.csv`, `item_properties_part1.csv`, `item_properties_part2.csv`.
- **Integrity Baseline**:
  - Verification via SHA-256 hashes registered in `data/raw/raw_data_registry.json`.
  - Observation timeframe: May 3, 2015 – September 18, 2015.
  - Zero tolerance for synthetic data or modified rows.

---

## 5. File Mapping Strategy

| Source File | Destination in Pipeline | Processing Purpose |
|---|---|---|
| `data/raw/retailrocket/events.csv` | `data/processed/interactions.csv` | Filtered, cleaned, and weighted interaction records with timestamps |
| `data/raw/retailrocket/category_tree.csv` | `data/processed/categories.csv` | Cleaned category DAG with root and depth assignments |
| `data/raw/retailrocket/item_properties_*.csv` | `data/processed/products.csv` | Aggregated item profile table (category, availability, structured tokens) |
| Output from split pipeline | `data/interim/train_interactions.csv` | Chronological training set ($t < T_{\text{train}}$) |
| Output from split pipeline | `data/interim/val_interactions.csv` | Chronological validation set ($T_{\text{train}} \le t < T_{\text{val}}$) |
| Output from split pipeline | `data/interim/test_interactions.csv` | Chronological test holdout set ($t \ge T_{\text{val}}$) |

---

## 6. Schema Mapping

### Entity ID Alignment
- Canonical RetailRocket: `visitorid` (int64) → mapped internally as `user_id`, `itemid` (int64) → mapped as `item_id`.
- Clean interfaces ensure the recommendation engine, API, and Streamlit UI remain compatible.

### Interaction Table Schema (`interactions.csv`)
```sql
CREATE TABLE interactions (
    interaction_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,          -- visitorid
    item_id BIGINT NOT NULL,          -- itemid
    event_type VARCHAR(20) NOT NULL,  -- view, addtocart, transaction
    weight FLOAT NOT NULL,            -- 1.0 (view), 3.0 (cart), 5.0 (purchase)
    timestamp BIGINT NOT NULL,        -- unix epoch ms
    datetime TIMESTAMP NOT NULL       -- UTC converted timestamp for human inspection
);
```

### Product Metadata Table Schema (`products.csv`)
```sql
CREATE TABLE products (
    item_id BIGINT PRIMARY KEY,
    category_id BIGINT,
    available INT,
    property_tokens TEXT,             -- concatenated property values for TF-IDF
    interaction_count INT DEFAULT 0,
    view_count INT DEFAULT 0,
    cart_count INT DEFAULT 0,
    purchase_count INT DEFAULT 0
);
```

---

## 7. Interaction Semantics & Weighting

RetailRocket interactions are implicit feedback events along an e-commerce conversion funnel:
$$\text{Weight}(e) = \begin{cases} 
1.0 & \text{if } e = \text{'view'} \\
3.0 & \text{if } e = \text{'addtocart'} \\
5.0 & \text{if } e = \text{'transaction'}
\end{cases}$$

Aggregated affinity score between user $u$ and item $i$:
$$s_{ui} = \sum_{e \in \mathcal{E}_{ui}} \text{Weight}(e)$$

This implicit affinity directly feeds:
1. Frequency-weighted Popularity Baseline.
2. Implicit Matrix Factorization ($c_{ui} = 1 + \alpha s_{ui}$, $p_{ui} = \mathbb{I}(s_{ui} > 0)$).
3. Item-Item Cosine / Jaccard Co-occurrence Collaborative Filtering.

---

## 8. Timestamp Semantics & Temporal Splitting Protocol

1. **Authentic Timestamps**: Every event possesses a 64-bit integer millisecond timestamp `timestamp` generated by the RetailRocket web tracking engine.
2. **Zero Temporal Leakage**:
   - Training window: $T_{\text{start}} \le t < T_{\text{split1}}$ (chronological past).
   - Validation window: $T_{\text{split1}} \le t < T_{\text{split2}}$ (intermediate horizon).
   - Test window: $T_{\text{split2}} \le t \le T_{\text{end}}$ (final evaluation horizon).
3. **No Shuffling / No Row-Index Inference**: All temporal operations strictly filter by `df['timestamp'] < cutoff`.
4. **Cold Users and Warm Users in Test Period**:
   - Warm users: Have interactions in both train and test windows; evaluated for personalized recommendation ranking.
   - Cold users: Have interactions only in test window; evaluated for cold-start fallback (popularity / category recommendations).

---

## 9. Item Metadata & Cold-Start Strategy

1. **Taxonomy Hierarchies**: `category_tree.csv` allows climbing up the category tree if a specific sub-category has few items.
2. **Cold-Start Fallback Pipeline**:
   - When a user is completely new (zero interaction history), serve top-N globally popular items.
   - When an item is new (zero interaction history in training set), recommend it to users based on Content-Based TF-IDF similarity computed from item properties and category overlap with items in the user's recent history.
   - When a user views an item detail page, serve Item-to-Item Content-Based similar products as "Related Products" fallback.

---

## 10. Train / Validation / Test Strategy

- **Train Split**: Chronological window from start through training cutoff.
- **Validation Split**: Chronological window between training cutoff and validation cutoff.
- **Test Split**: Chronological window from validation cutoff through end of dataset.
- **Evaluation Metrics**:
  - Precision@5, Precision@10
  - Recall@5, Recall@10
  - NDCG@5, NDCG@10
  - Catalog Coverage (%)
  - Hit Rate@K

---

## 11. Legacy FIT5212 Handling

To comply with Rules 1, 4, 5:
- FIT5212 artifacts and references are quarantined and documented as `LEGACY / HISTORICAL — NOT ACTIVE`.
- **Zero cross-contamination**: No FIT5212 IDs, ratings, or products are merged into the active RetailRocket pipeline.

---

## 12. Existing Architecture Preservation Strategy

We strictly preserve the working Python + Scikit-learn + SciPy + FastAPI + Streamlit architecture:
1. **`src/models/`**:
   - `popularity_model.py`: Event-weighted interaction velocity.
   - `collaborative_filtering.py`: Implicit feedback frequencies / item-item co-occurrences.
   - `matrix_factorization.py`: Implicit matrix factorization on interaction matrix.
   - `content_based.py`: TF-IDF vectorizer on category and property tokens.
   - `hybrid_recommendation.py`: Hybrid ensemble blending collaborative scores with content fallback and popularity.
2. **`api/recommendation_api.py`**:
   - Preserve endpoint paths: `/health`, `/recommend/{user_id}`, `/recommend/popular`, `/recommend/similar/{item_id}`.
3. **`app/streamlit_app.py`**:
   - Interactive dashboard, real-time recommendation tester, model metrics, segment insights.
4. **`tests/`**:
   - Unit tests validating data foundation, temporal ordering, and recommendation metrics.

---

## 13. Risk Management & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Data Sparsity** | High sparsity (~99.99%) in large visitor-item clickstreams | Filter users/items with insufficient interactions (e.g. 3-core or 5-core) for personalized training matrix while retaining full catalog for popularity and cold-start fallback. |
| **Memory Consumption** | Raw properties file is ~900MB | Use streaming/chunking and selective loading of active item properties; store processed matrices as sparse matrices (`scipy.sparse.csr_matrix`). |

---

## 14. Validation Gates for Phase 1 Redesign

1. **Gate M1 (Provenance)**: SHA-256 verification and registry in `raw_data_registry.json`.
2. **Gate M2 (Schema)**: 100% adherence to `visitorid`, `itemid`, `event`, `timestamp`.
3. **Gate M3 (Temporal Split)**: Verification of chronological split order ($t_{\text{train}} < t_{\text{val}} < t_{\text{test}}$) with zero temporal inversion or leakage.
4. **Gate M4 (Entity Integrity)**: `users.csv`, `products.csv`, and `popular_products.csv` generated purely from authentic raw data.
5. **Gate M5 (Test Suite)**: `pytest tests/` passing 100% against new data foundation.

---

## 15. Rollback Strategy

If migration is disrupted:
- Documentation and scripts are versioned and reproducible.
- Quarantine directories isolate legacy data completely.
