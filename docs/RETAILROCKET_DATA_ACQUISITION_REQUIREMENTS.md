# RetailRocket Data Acquisition Requirements
## Project 3 — Personalized Product Recommendation Model
## Specification for Authentic Dataset Ingestion & Migration

---

## 1. Executive Summary & Purpose

The **Personalized Product Recommendation Model** (Project 3) is undergoing a controlled migration from the legacy Monash University FIT5212 S1 2025 dataset to the **RetailRocket E-Commerce Recommender Dataset**.

This document specifies the exact technical requirements, schema definitions, provenance criteria, and data integrity checks required for the authentic RetailRocket dataset files before any ingestion or pipeline transformation can begin.

---

## 2. Dataset Provenance & Authentic Origin

| Field | Canonical Requirement |
|---|---|
| **Dataset Title** | Retailrocket Recommender System Dataset |
| **Original Publisher** | RetailRocket E-Commerce Personalization Platform |
| **Canonical Public Host** | Kaggle Datasets (`https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset`) |
| **Primary Domain** | E-commerce clickstream events and product catalog hierarchy |
| **Observation Window** | May 3, 2015 – September 18, 2015 (approx. 4.5 months) |
| **Scale Baseline** | ~2,756,101 behavioral events across ~1,407,580 unique visitors and ~235,061 items |
| **Temporal Granularity** | Millisecond-level Unix epoch timestamps (`timestamp`) |
| **Acceptable Formats** | Uncompressed UTF-8 CSV files or compressed `.zip` / `.tar.gz` archives of canonical CSVs |
| **Strict Prohibition** | Synthetic events, simulated timestamps, mock user sessions, or unverified mirrors |

---

## 3. Required Source Files & Structural Specifications

The authentic dataset consists of four standard files:

```text
data/raw/retailrocket/
├── events.csv
├── item_properties_part1.csv
├── item_properties_part2.csv (or merged item_properties.csv)
└── category_tree.csv
```

### 3.1 `events.csv` (Mandatory Core Interaction Table)

The primary interaction log representing authentic user clickstream events.

- **Expected Row Count**: ~2,756,101 rows.
- **Exact Expected Schema**:

| Column Name | Data Type | Nullable | Description & Constraints |
|---|---|---|---|
| `timestamp` | `int64` | No | Millisecond Unix epoch timestamp (e.g., `1433221332035`). Expected range: `1430622000000` to `1442545000000` (May–Sept 2015). |
| `visitorid` | `int64` | No | Unique pseudonymous identifier for an individual site visitor. |
| `event` | `string` | No | Semantic event type. Must strictly be one of `['view', 'addtocart', 'transaction']`. |
| `itemid` | `int64` | No | Unique identifier for the product/item interacted with. |
| `transactionid` | `int64` | Yes | Transaction ID. Valid integer on `transaction` events; `NaN` / empty on `view` and `addtocart`. |

- **Integrity Constraints**:
  - `timestamp` must be strictly positive and within the authentic 2015 collection epoch.
  - `visitorid` > 0, `itemid` > 0.
  - `event` values must match the three known strings exactly (`view`, `addtocart`, `transaction`).
  - `transactionid` must be present when `event == 'transaction'` and null when `event != 'transaction'`.

### 3.2 `category_tree.csv` (Category Hierarchy)

Defines the parent-child relational taxonomy of product categories.

- **Expected Row Count**: ~1,669 rows.
- **Exact Expected Schema**:

| Column Name | Data Type | Nullable | Description & Constraints |
|---|---|---|---|
| `categoryid` | `int64` | No | Unique integer identifier of the product category. |
| `parentid` | `float64` / `int64` | Yes | Parent category ID. Null/`NaN` denotes a top-level root category. |

- **Integrity Constraints**:
  - No cyclic directed graphs in category-parent relationships.
  - Root categories must have null/missing `parentid`.
  - Non-null `parentid` values should resolve to valid `categoryid` keys.

### 3.3 `item_properties_part1.csv` & `item_properties_part2.csv` (Item Metadata)

Contains time-varying and static attribute key-value pairs for items.

- **Expected Row Count**: ~20,275,902 rows combined.
- **Exact Expected Schema**:

| Column Name | Data Type | Nullable | Description & Constraints |
|---|---|---|---|
| `timestamp` | `int64` | No | Snapshot timestamp (Unix epoch milliseconds) of property observation. |
| `itemid` | `int64` | No | Product identifier matching `events.itemid`. |
| `property` | `string` | No | Property identifier (e.g. `'categoryid'`, `'available'`, or hashed alphanumeric string IDs). |
| `value` | `string` | No | Property value. |

- **Integrity Constraints**:
  - `itemid` references must overlap with active items in `events.csv`.
  - Temporal lookahead leakage must be avoided: item metadata used for cold-start content fallback must use the latest known property value prior to the evaluation split cutoff timestamp.

---

## 4. Interaction Semantics & Conversion Mapping

| Event Type | Raw Count (approx.) | Semantic Meaning | Recommended Implicit Weight | Conversion Funnel Order |
|---|---|---|---|---|
| `view` | ~2,664,312 (96.7%) | User viewed product detail page | `1.0` | Step 1 |
| `addtocart` | ~69,332 (2.5%) | User added product to shopping basket | `3.0` | Step 2 |
| `transaction` | ~22,457 (0.8%) | User completed order checkout | `5.0` | Step 3 (Terminal conversion) |

---

## 5. Temporal Splitting Protocol

1. **Temporal Horizon**:
   - Split interactions by time cutoff $T_{\text{train\_split}}$ and $T_{\text{val\_split}}$.
   - **Training Set**: Historical interactions where $\text{timestamp} < T_{\text{split}}$.
   - **Validation Set**: Temporal window $[T_{\text{train\_split}}, T_{\text{val\_split}})$.
   - **Test Set**: Terminal temporal window $[T_{\text{val\_split}}, T_{\text{max}}]$.
2. **Leakage Prevention**:
   - Zero forward-looking leakage.
   - User interaction histories evaluated in the test period must only use training period information for model fitting.

---

## 6. Required Integrity Checks & Acceptance Gates

1. **Gate ACQ-01: File Presence & Checksum Validation**
   - Confirm presence of `events.csv`, `category_tree.csv`, `item_properties_*.csv`.
   - Calculate SHA-256 hashes and verify non-empty file size.
   - Log metadata in `data/raw/raw_data_registry.json`.

2. **Gate ACQ-02: Schema & Data Type Verification**
   - Validate column names match expected headers exactly.
   - Confirm `timestamp`, `visitorid`, `itemid` parse as 64-bit integers.
   - Confirm `event` is categorized into the 3 authentic event types.

3. **Gate ACQ-03: Temporal Monotonicity & Boundary Sanity**
   - Minimum timestamp $\ge 1430000000000$ (approx. May 2015).
   - Maximum timestamp $\le 1450000000000$ (approx. late 2015).

4. **Gate ACQ-04: Referential Integrity**
   - Zero null values in `visitorid`, `itemid`, `event`, or `timestamp`.
   - `transactionid` non-null if and only if `event == 'transaction'`.

5. **Gate ACQ-05: Non-Fabrication Certification**
   - Absolute verification that no rows were synthetically interpolated.
