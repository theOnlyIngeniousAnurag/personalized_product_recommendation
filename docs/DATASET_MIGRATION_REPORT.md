# Dataset Migration Report: FIT5212 to Authentic RetailRocket
**Project:** Personalized Product Recommendation Model  
**Date:** 2026-09-30  
**Phase:** Phase 1 — Controlled Data Foundation Migration  

---

## 1. Pre-Migration Baseline State (FIT5212)
* **Dataset Used:** Monash University FIT5212 S1 2025 Recommender System Challenge (`train_part1.csv`, `train_part2.csv`, `test.csv`).
* **Source Schema:** `['user_id', 'product_id', 'product_name', 'rating', 'votes', 'helpful_votes', 'ID']`
* **Raw Row Counts:**
  * `train_part1.csv`: 372,944 rows (20.88 MB)
  * `train_part2.csv`: 372,945 rows (21.11 MB)
  * `test.csv`: 223,553 rows (11.01 MB)
* **Combined Logical Training Data:** 745,889 rows.
* **Limitations of FIT5212 for the Internship Specification:**
  * Lacked real e-commerce behavioral event types (`view`, `addtocart`, `transaction`).
  * Lacked authentic chronological event timestamps (synthetic incremental counters had to be used).
  * Lacked official e-commerce category hierarchy and property metadata.
* **Preservation Status:** Archived immutably under `data/raw/legacy_fit5212/` to ensure 100% rollback safety.

---

## 2. Authentic RetailRocket Acquisition & Verification
* **Source:** Kaggle `retailrocket/ecommerce-dataset` downloaded via official `kagglehub` API.
* **Storage Location:** `data/raw/retailrocket/`
* **Raw Files Acquired:**
  1. `category_tree.csv` (14,454 bytes)
  2. `events.csv` (94,237,913 bytes)
  3. `item_properties_part1.csv` (484,315,749 bytes)
  4. `item_properties_part2.csv` (408,929,907 bytes)

---

## 3. Raw Data Profile
* **Raw Event Count:** 2,756,101 events
* **Event Distribution:**
  * `view`: 2,664,312 (96.67%)
  * `addtocart`: 69,332 (2.52%)
  * `transaction`: 22,457 (0.81%)
* **Unique Visitors (Users):** 1,407,580
* **Unique Items (Products):** 235,061
* **Timestamp Range:**
  * Minimum Timestamp: `1,430,622,004,384` (Sunday, May 3, 2015 03:00:04.384 UTC)
  * Maximum Timestamp: `1,442,545,187,788` (Friday, September 18, 2015 02:59:47.788 UTC)
  * Timespan: ~4.5 months of genuine user behavior.
* **Categories:** 1,669 categories in hierarchical category tree.
