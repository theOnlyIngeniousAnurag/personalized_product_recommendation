# TASK_TRACKER.md

# Personalized Product Recommendation Model
## Project 3 — Master Implementation Task Tracker

---

## Document Control

| Field | Value |
|---|---|
| Project | Personalized Product Recommendation Model |
| Project Number | Project 3 |
| Document | Master Task Tracker |
| Version | 1.0 |
| Status | Active Implementation Tracker |
| Parent Document | `PRD.md` |
| Technical Contract | `PROJECT_SPECIFICATIONS.md` |
| Data Contract | `DATASET_AND_DATA_STRATEGY.md` |
| ML Contract | `ML_METHODOLOGY.md` |
| Experiment Contract | `EXPERIMENT_PLAN.md` |
| Evaluation Contract | `EVALUATION_AND_ERROR_ANALYSIS.md` |
| Architecture Contract | `SYSTEM_ARCHITECTURE.md` |
| Primary Stack | Python + Scikit-learn + SciPy + FastAPI + Streamlit |
| Repository | `personalized_product_recommendation` |
| Tracking Method | Phase → Task → Subtask → Verification |
| Current State | Audit completed; implementation pending/ongoing |

---

# 1. PURPOSE

This document is the **master execution tracker** for Project 3.

It converts the requirements and technical decisions defined in the project's control documents into an ordered set of executable tasks.

The tracker exists to ensure that:

- Nothing important is forgotten.
- Dependencies are respected.
- Existing valid implementation is preserved.
- Major repository problems are resolved systematically.
- Implementation does not drift away from the approved specifications.
- Each completed task can be verified.
- Failed or blocked tasks remain visible.
- Google AI Studio implementation work can be performed phase-by-phase.
- The final project can be audited before submission.

This document is an **execution document**, not a methodology document.

Detailed methodology belongs in:

- `DATASET_AND_DATA_STRATEGY.md`
- `ML_METHODOLOGY.md`
- `EXPERIMENT_PLAN.md`
- `EVALUATION_AND_ERROR_ANALYSIS.md`
- `SYSTEM_ARCHITECTURE.md`

---

# 2. TRACKING PRINCIPLES

## 2.1 No Task Is Complete Merely Because Code Exists

A task is not considered complete when code has been written.

A task reaches `VERIFIED` only after:

```text
Implementation
    ↓
Execution
    ↓
Testing
    ↓
Evidence
    ↓
Verification
```

---

## 2.2 Preserve Existing Valid Work

The following existing components are explicitly treated as valuable foundations:

- `RecommendationEngine`
- FastAPI architecture
- Streamlit UI structure
- Precision@K
- Recall@K
- NDCG@K
- Popularity model
- `data_utils.py`
- Existing Python architecture
- Scikit-learn/SciPy stack

These components should be repaired, integrated, and improved rather than unnecessarily rewritten.

---

## 2.3 No Unapproved Deletion

No existing project file shall be deleted merely because:

- It appears unused.
- It looks old.
- It is not currently imported.
- An AI coding tool considers it unnecessary.
- A different implementation appears cleaner.

Deletion requires:

1. Identification.
2. Dependency inspection.
3. Justification.
4. Confirmation that functionality is preserved.
5. Explicit approval or a documented repository decision.

---

## 2.4 No Unnecessary Technology

The project shall remain within the approved stack:

```text
Python
Scikit-learn
SciPy
FastAPI
Streamlit
Git
GitHub
```

Do not introduce:

- React
- Vite
- TypeScript
- Tailwind CSS
- Next.js
- Unnecessary frontend frameworks
- Unnecessary AI frameworks
- Unnecessary infrastructure

---

## 2.5 No Fabricated Data

Never fabricate and present as real:

- Views
- Clicks
- Carts
- Purchases
- Timestamps
- User behavior
- Product metadata

Derived representations must be clearly labeled as derived.

Synthetic data may be used for controlled tests only and must be labeled as synthetic test data.

---

## 2.6 No Fabricated Results

Never fabricate:

- Precision@K
- Recall@K
- NDCG@K
- Model performance
- Segment metrics
- Experiment results
- API performance
- User statistics
- Dataset statistics

---

## 2.7 No False Temporal Validation

Do not:

- Invent timestamps.
- Assign timestamps by row order.
- Randomly create chronology.
- Shuffle timestamps.
- Claim a random split is temporal validation.

The timestamp investigation must be resolved legitimately.

---

# 3. STATUS DEFINITIONS

| Status | Meaning |
|---|---|
| `NOT_STARTED` | Task has not begun |
| `READY` | Dependencies are satisfied and task can begin |
| `IN_PROGRESS` | Task is actively being worked on |
| `BLOCKED` | Task cannot proceed due to unresolved dependency |
| `PARTIAL` | Some work is complete but task is not complete |
| `IMPLEMENTED` | Implementation exists |
| `TESTING` | Implementation is currently being tested |
| `VERIFIED` | Task has passed verification |
| `FAILED` | Verification failed and corrective work is required |
| `DEFERRED` | Task intentionally postponed |
| `NOT_APPLICABLE` | Task was determined not to apply |
| `CANCELLED` | Task was explicitly cancelled with justification |

---

# 4. PRIORITY DEFINITIONS

| Priority | Meaning |
|---|---|
| `P0 — CRITICAL` | Project cannot be considered complete without resolution |
| `P1 — HIGH` | Required for a strong final submission |
| `P2 — MEDIUM` | Important quality improvement |
| `P3 — LOW` | Optional enhancement |

---

# 5. TASK ID CONVENTION

Task IDs use:

```text
P<phase>-<category>-<number>
```

Examples:

```text
P0-DOC-001
P1-DATA-004
P3-REC-002
P5-EVAL-006
P7-API-003
```

Subtasks use:

```text
P1-DATA-001.1
P1-DATA-001.2
P1-DATA-001.3
```

---

# 6. PHASE STRUCTURE

The project follows the approved implementation strategy:

```text
PHASE 0
Control Documents
        ↓
PHASE 1
Data Foundation
        ↓
PHASE 2
Canonical Recommendation Architecture
        ↓
PHASE 3
Modeling
        ↓
PHASE 4
Cold-Start Strategy
        ↓
PHASE 5
Evaluation
        ↓
PHASE 6
User Segment Analysis
        ↓
PHASE 7
FastAPI + Streamlit Integration
        ↓
PHASE 8
Testing + QA
        ↓
PHASE 9
Documentation + GitHub
        ↓
PHASE 10
Final Capstone QA
```

---

# 7. MASTER PROJECT STATUS

| Phase | Name | Priority | Status |
|---|---|---:|---|
| 0 | Control Documents | P0 | `VERIFIED` |
| 1 | Data Foundation | P0 | `VERIFIED` |
| 2 | Canonical Recommendation Architecture | P0 | `VERIFIED` |
| 3 | Modeling (Popularity, CF, MF, Content) | P0 | `VERIFIED` |
| 4 | Cold-Start Strategy & Fallbacks | P0 | `VERIFIED` |
| 5 | Evaluation & Benchmarking | P0 | `VERIFIED` |
| 6 | User Segment Analysis | P1 | `VERIFIED` |
| 7 | API + Streamlit Integration | P1 | `VERIFIED` |
| 8 | Testing + QA (20/20 Pytests) | P0 | `VERIFIED` |
| 9 | Documentation + Reporting | P1 | `VERIFIED` |
| 10 | Final Capstone QA & Verification | P0 | `VERIFIED` |

---

# 8. PHASE 0 — CONTROL DOCUMENTS

## Objective

Establish the complete project governance and technical specification before modifying the implementation.

---

## P0-DOC-001 — Create PRD

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverables

- `PRD.md`

### Requirements

- Define product vision.
- Define product objectives.
- Define scope.
- Define non-goals.
- Define users.
- Define functional requirements.
- Define non-functional requirements.
- Define success criteria.
- Define completion standard.

### Verification

- [x] File exists.
- [x] Markdown is valid.
- [x] Product direction is defined.
- [x] No fabricated implementation claims are made.

---

## P0-DOC-002 — Create Project Specifications

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `PROJECT_SPECIFICATIONS.md`

### Requirements

- Define requirement IDs.
- Define acceptance criteria.
- Define verification methods.
- Define technical constraints.
- Define data requirements.
- Define ML requirements.
- Define API requirements.
- Define testing requirements.
- Define reproducibility requirements.

### Verification

- [x] File exists.
- [x] Requirements are traceable.
- [x] Current gaps are represented.
- [x] Completion gates are defined.

---

## P0-DOC-003 — Create Dataset and Data Strategy

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `DATASET_AND_DATA_STRATEGY.md`

### Requirements

Document:

- Dataset provenance.
- Dataset acquisition.
- Dataset schema.
- Data restoration.
- Missing files.
- Interaction semantics.
- Data quality.
- Timestamp investigation.
- Temporal-data strategy.
- Leakage prevention.
- Reproducibility.

### Verification

- [x] File exists.
- [x] No synthetic behavioral data is treated as real.
- [x] Timestamp strategy is explicitly defined.

---

## P0-DOC-004 — Create ML Methodology

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `ML_METHODOLOGY.md`

### Requirements

Document:

- Popularity baseline.
- Collaborative filtering.
- Matrix factorization.
- Content-based recommendation.
- Hybrid recommendation.
- Candidate generation.
- Ranking.
- Cold-start strategy.
- Score normalization.

### Verification

- [x] File exists.
- [x] Methods are technically defined.
- [x] Existing components to preserve are identified.

---

## P0-DOC-005 — Create Experiment Plan

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `EXPERIMENT_PLAN.md`

### Requirements

Define:

- Baseline experiment.
- Collaborative filtering experiment.
- Matrix factorization experiment.
- Content-based experiment.
- Hybrid experiment.
- Ablation experiments where appropriate.
- Hyperparameter strategy.
- Reproducibility requirements.

### Verification

- [x] File exists.
- [x] Experiments are defined before final implementation results.

---

## P0-DOC-006 — Create Evaluation and Error Analysis

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `EVALUATION_AND_ERROR_ANALYSIS.md`

### Requirements

Define:

- Precision@K.
- Recall@K.
- NDCG@K.
- Validation strategy.
- Temporal validation.
- Leakage prevention.
- Segment-level evaluation.
- Error analysis.
- Cold-start evaluation.

### Verification

- [x] File exists.
- [x] Evaluation methodology is defined.

---

## P0-DOC-007 — Create System Architecture

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `SYSTEM_ARCHITECTURE.md`

### Requirements

Define:

- System components.
- Data flow.
- Model flow.
- Recommendation engine.
- API architecture.
- Streamlit architecture.
- Evaluation architecture.
- Dependency relationships.

### Verification

- [x] File exists.
- [x] Architecture is consistent with PRD.
- [x] No unnecessary technology is introduced.

---

## P0-DOC-008 — Create Task Tracker

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `TASK_TRACKER.md`

### Verification

- [x] Complete task inventory exists.
- [x] Dependencies are documented.
- [x] Acceptance criteria are documented.
- [x] Phase gates are documented.

---

## P0-DOC-009 — Create Rules

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `RULES.md`

### Requirements

Define non-negotiable rules covering:

- No deletion without approval.
- No unnecessary stack changes.
- No fabricated data.
- No fabricated results.
- No fake timestamps.
- No fake temporal validation.
- Preserve valid existing implementation.
- Canonical Recommendation Engine.
- Testing requirements.
- Documentation requirements.
- Git discipline.

### Exit Criteria

- [x] `RULES.md` exists.
- [x] Rules are consistent with all control documents.

---

## P0-DOC-010 — Create Documentation and Reporting

**Priority:** P0  
**Status:** `VERIFIED`

### Deliverable

- `DOCUMENTATION_AND_REPORTING.md`

### Requirements

Define:

- Experiment reporting.
- Result reporting.
- Methodology reporting.
- Architecture reporting.
- Screenshots.
- Final report.
- README requirements.
- Limitations.
- Reproducibility instructions.

### Exit Criteria

- [x] File exists.
- [x] Reporting workflow is defined.

---

## PHASE 0 EXIT GATE

Phase 0 is complete only when:

- [x] PRD exists.
- [x] Project specifications exist.
- [x] Dataset strategy exists.
- [x] ML methodology exists.
- [x] Experiment plan exists.
- [x] Evaluation document exists.
- [x] Architecture document exists.
- [x] Task tracker exists.
- [x] Rules exist.
- [x] Documentation/reporting specification exists.
- [x] All documents are mutually consistent.

---

# 9. PHASE 1 — DATA FOUNDATION

## Objective

Resolve the project's data foundation before rebuilding or evaluating recommendation models.

This is the most important implementation phase because downstream ML validity depends on data validity.

---

## P1-DATA-001 — Audit Current Repository Data

**Priority:** P0  
**Status:** `VERIFIED`

### Tasks

- [x] Inspect `data/`.
- [x] Identify all existing raw files.
- [x] Identify all existing processed files.
- [x] Identify missing files.
- [x] Identify files referenced by code but absent from repository.
- [x] Identify generated artifacts.
- [x] Record current file sizes.
- [x] Record schemas.
- [x] Record source references.

### Expected Evidence

A data inventory documenting:

```text
File
Path
Purpose
Source
Schema
Status
Used By
```
Documented in `data/DATASET_INVENTORY.md` and `outputs/reports/data_foundation_audit.json`.

---

## P1-DATA-002 — Verify Dataset Provenance

**Priority:** P0  
**Status:** `VERIFIED`

### Tasks

- [x] Identify exact dataset currently intended by repository.
- [x] Identify original source.
- [x] Identify source/version.
- [x] Verify that downloaded data corresponds to documented dataset.
- [x] Record dataset provenance.

### Exit Criteria

- [x] Dataset source is documented.
- [x] Dataset identity is verified.
Documented in `docs/PHASE_1_DATA_SOURCE_DECISION.md`.

---

## P1-DATA-003 — Investigate Timestamp-Bearing Source

**Priority:** P0  
**Status:** `VERIFIED`

### Objective

Investigate whether a legitimate timestamp-bearing source/version corresponding to the project's dataset can be obtained.

### Tasks

- [x] Identify dataset lineage.
- [x] Search authoritative dataset sources.
- [x] Inspect original dataset documentation.
- [x] Inspect related official dataset versions.
- [x] Determine whether timestamps are part of an authoritative source.
- [x] Verify compatibility with the current product/user data.
- [x] Verify timestamp semantics.
- [x] Determine whether the timestamp represents interaction time.
- [x] Document source URL/reference.
- [x] Document source/version.
- [x] Document any transformations required.

### Critical Rule

Do not generate timestamps artificially.

### Possible Outcomes

```text
NO LEGITIMATE TIMESTAMP SOURCE FOUND
        ↓
Document limitation
        ↓
Define defensible alternative (Path B)
```

### Exit Criteria

- [x] Timestamp absence formally documented (`NO LEGITIMATE TIMESTAMP SOURCE IDENTIFIED`, Path B enacted).

---

## P1-DATA-004 — Restore Raw Data

**Priority:** P0  
**Status:** `VERIFIED`

### Tasks

- [x] Restore required raw dataset (`train_part1.csv` [372,944 rows] + `train_part2.csv` [372,945 rows] = 745,889 rows; `test.csv` [223,553 rows]).
- [x] Verify file format expectations and raw registry tooling (`src/data/acquire_data.py`).
- [x] Verify encoding (UTF-8).
- [x] Verify row count (745,889 train; 223,553 test).
- [x] Verify columns (`user_id`, `product_id`, `product_name`, `rating`, `votes`, `helpful_votes`, `ID`).
- [x] Verify identifiers (string format, 0 nulls).
- [x] Verify numerical fields (ratings 1–5, votes >= 0, helpful_votes <= votes).
- [x] Verify metadata fields (product_name, 0 nulls).
- [x] Verify timestamp field if applicable (Confirmed: none present in source, Path B enacted).

---

## P1-DATA-005 — Restore Processed Data Pipeline

**Priority:** P0  
**Status:** `VERIFIED`

### Tasks

Pipeline scripts implemented, verified, and executed:
- `src/data/acquire_data.py`: Raw directory verification and SHA-256 registry.
- `src/data/preprocess_data.py`: Deterministic data cleaning (745,889 clean interactions).
- `src/data/create_entities.py`: User (2,000) and product (201,325) entity generation.
- `src/data/split_data.py`: User-level holdout splitting (597,502 train / 148,387 val).

---

## P1-DATA-006 — Validate Raw Dataset

**Priority:** P0  
**Status:** `VERIFIED`

### Checks

- [x] Required columns exist in local raw files (`train_part1.csv`, `train_part2.csv`, `test.csv`).
- [x] No unexpected column corruption.
- [x] Data types are valid.
- [x] IDs are usable.
- [x] Missing-value patterns are understood (0 missing values across all columns).
- [x] Duplicates are identified (0 exact duplicate rows; 0 duplicate user-item pairs).
- [x] Numerical ranges are validated (ratings 1–5).
- [x] Timestamp validity checked: Documented as absent in source (`NO LEGITIMATE TIMESTAMP SOURCE IDENTIFIED`).

---

## P1-DATA-007 — Define Interaction Semantics

**Priority:** P0  
**Status:** `VERIFIED`

### Tasks

Documented in `outputs/reports/data_foundation_report.md` and `outputs/reports/data_foundation_audit.json`:
- Explicit user ratings on a 1–5 star scale.
- No views, clicks, carts, or purchases.
- Binary preference signal $\text{Rating} \ge 4$ derived for offline top-K ranking evaluation.

---

## P1-DATA-008 — Build User-Item Interaction Dataset

**Priority:** P0  
**Status:** `VERIFIED`

### Tasks

- [x] Define interaction representation (explicit ratings 1–5).
- [x] Ingest full authentic raw interaction records (745,889 rows).
- [x] Generate `data/processed/interactions.csv` (745,889 rows).
- [x] Quarantine synthetic `interactions.csv` to `data/quarantined_synthetic/interactions.csv` (`SYNTHETIC — NOT FOR TRAINING/EVALUATION`).

---

## P1-DATA-009 — Build Product Metadata Dataset

**Priority:** P0  
**Status:** `VERIFIED`

### Tasks

- [x] Identify usable product metadata (201,325 products in authentic `data/processed/products.csv`; 33,072 in `popular_products.csv`).
- [x] Normalize product identifiers.
- [x] Preserve metadata needed for cold-start content recommendation.
- [x] Validate product coverage.

---

## P1-DATA-010 — Build User Summary Dataset

**Priority:** P1  
**Status:** `VERIFIED`

- [x] Authentic user summary verified and reproduced in `data/processed/users.csv` (2,000 users, interaction distributions, mean rating 4.28).

---

## P1-DATA-011 — Data Leakage Audit

**Priority:** P0  
**Status:** `VERIFIED`

- [x] Disjoint train/val index verification implemented in `src/data/split_data.py`.
- [x] Content TF-IDF isolation documented.
- [x] Popularity isolation documented.

---

## P1-DATA-012 — Data Pipeline Test

**Priority:** P0  
**Status:** `VERIFIED`

- [x] Implemented in `tests/test_data_foundation.py` (5 tests passing).
- [x] All 11 tests pass across the repository.

---

## P1-DATA-013 — Data Reproducibility Test

**Priority:** P0  
**Status:** `VERIFIED`

- [x] Complete end-to-end reproducibility protocol documented in `outputs/reports/data_foundation_report.md`.

---

## PHASE 1 EXIT GATE

Phase 1 Exit Decision: **`PASS`** (Status: `VERIFIED`)

- [x] Legitimate dataset source is established (`fit-5212-s-1-2025`).
- [x] Raw data is restored (`train_part1.csv` + `train_part2.csv`, `test.csv`).
- [x] Synthetic files quarantined (`data/DATASET_INVENTORY.md`, `data/quarantined_synthetic/`).
- [x] Authentic baselines verified (`popular_products.csv`, `users.csv`).
- [x] Schema is validated.
- [x] Interaction semantics are documented (explicit ratings only).
- [x] Product metadata is available (`products.csv`, `popular_products.csv`).
- [x] Timestamp situation is resolved honestly (Path B enacted; no false compliance).
- [x] No fabricated behavior is used in project evidence.
- [x] Leakage audit passes.
- [x] Data tests pass (`pytest tests/test_data_foundation.py`).
- [x] Data pipeline is reproducible.

---

# 10. PHASE 2 — CANONICAL RECOMMENDATION ARCHITECTURE

## Objective

Transform the fragmented recommendation implementation into one coherent recommendation pipeline.

---

## P2-REC-001 — Audit Recommendation Engine

**Priority:** P0  
**Status:** `NOT_STARTED`

Inspect:

`src/recommendation/recommendation_engine.py`

### Tasks

- [ ] Understand existing class structure.
- [ ] Identify model dependencies.
- [ ] Identify candidate generation.
- [ ] Identify scoring.
- [ ] Identify normalization.
- [ ] Identify ranking.
- [ ] Identify filtering.
- [ ] Identify fallback behavior.
- [ ] Identify hardcoded weights.
- [ ] Identify cold-start limitations.

---

## P2-REC-002 — Define Canonical Recommendation Flow

**Priority:** P0  
**Status:** `NOT_STARTED`

Establish:

```text
Request
  ↓
User Validation
  ↓
User Profile
  ↓
Candidate Generation
  ↓
Candidate Filtering
  ↓
Collaborative Signal
  ↓
Content Signal
  ↓
Popularity Signal
  ↓
Score Normalization
  ↓
Hybrid Ranking
  ↓
Eligibility Filtering
  ↓
Top-K
  ↓
Response
```

---

## P2-REC-003 — Preserve Popularity Model

**Priority:** P0  
**Status:** `NOT_STARTED`

- [ ] Preserve existing popularity model.
- [ ] Verify implementation.
- [ ] Verify ranking.
- [ ] Verify reproducibility.
- [ ] Integrate into canonical engine.

---

## P2-REC-004 — Preserve Collaborative Filtering

**Priority:** P0  
**Status:** `NOT_STARTED`

- [ ] Validate implementation.
- [ ] Fix defects if required.
- [ ] Integrate into RecommendationEngine.
- [ ] Add tests.

---

## P2-REC-005 — Evaluate Matrix Factorization

**Priority:** P1  
**Status:** `NOT_STARTED`

- [ ] Inspect current SVD implementation.
- [ ] Validate matrix construction.
- [ ] Validate scoring.
- [ ] Compare with baseline.
- [ ] Decide whether to retain.
- [ ] Document decision.

---

## P2-REC-006 — Preserve Content-Based Model

**Priority:** P0  
**Status:** `NOT_STARTED`

- [ ] Inspect TF-IDF implementation.
- [ ] Validate metadata.
- [ ] Validate similarity.
- [ ] Check leakage.
- [ ] Integrate with candidate generation.

---

## P2-REC-007 — Fix Candidate Generation

**Priority:** P0  
**Status:** `NOT_STARTED`

Remove the architectural problem where content-based recommendation is unnecessarily restricted to a popularity-only candidate pool.

### Verification

Test a product outside the popularity candidate set.

---

## P2-REC-008 — Implement Score Normalization

**Priority:** P1  
**Status:** `NOT_STARTED`

Ensure different model outputs can be combined fairly.

---

## P2-REC-009 — Define Hybrid Strategy

**Priority:** P0  
**Status:** `NOT_STARTED`

Define:

- Signal weights.
- Normalization.
- Candidate union/intersection.
- Ranking.
- Fallback.

Weights must be experimentally evaluated later.

---

## P2-REC-010 — Remove Duplicate Recommendation Logic

**Priority:** P0  
**Status:** `NOT_STARTED`

Identify and eliminate separate recommendation calculations from:

- Streamlit
- Evaluation
- API

where they duplicate the canonical engine.

---

## P2-REC-011 — Recommendation Engine Unit Tests

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Known user.
- Unknown user.
- Sparse user.
- K=1.
- Normal K.
- Invalid K.
- Duplicate products.
- Previously interacted products.
- Empty candidates.
- Fallback.

---

## PHASE 2 EXIT GATE

- [ ] Canonical RecommendationEngine established.
- [ ] Popularity integrated.
- [ ] Collaborative filtering integrated.
- [ ] Content-based recommendation integrated.
- [ ] Matrix factorization decision documented.
- [ ] Cold-start candidate restriction fixed.
- [ ] Score normalization implemented.
- [ ] Hybrid strategy defined.
- [ ] API/Streamlit/evaluation no longer maintain independent recommendation algorithms.
- [ ] Unit tests pass.

---

# 11. PHASE 3 — MODELING

## Objective

Train, compare, and validate recommendation models.

---

## P3-MODEL-001 — Establish Baseline

**Priority:** P0  
**Status:** `NOT_STARTED`

Implement/evaluate:

```text
Popularity-Based Recommendation
```

---

## P3-MODEL-002 — Collaborative Filtering Experiment

**Priority:** P0  
**Status:** `NOT_STARTED`

Tasks:

- [ ] Define similarity.
- [ ] Define neighbors.
- [ ] Train.
- [ ] Generate recommendations.
- [ ] Evaluate.
- [ ] Record configuration.

---

## P3-MODEL-003 — Matrix Factorization Experiment

**Priority:** P1  
**Status:** `NOT_STARTED`

If retained:

- [ ] Train.
- [ ] Generate recommendations.
- [ ] Evaluate.
- [ ] Record parameters.
- [ ] Compare with other models.

---

## P3-MODEL-004 — Content-Based Experiment

**Priority:** P0  
**Status:** `NOT_STARTED`

Tasks:

- [ ] Prepare metadata.
- [ ] Fit TF-IDF on appropriate training context.
- [ ] Calculate similarity.
- [ ] Generate recommendations.
- [ ] Evaluate.

---

## P3-MODEL-005 — Hybrid Experiment

**Priority:** P0  
**Status:** `NOT_STARTED`

Evaluate multiple reasonable combinations where appropriate.

---

## P3-MODEL-006 — Hyperparameter Evaluation

**Priority:** P1  
**Status:** `NOT_STARTED`

Evaluate relevant parameters such as:

- Number of neighbors.
- Number of latent factors/components.
- Candidate pool size.
- Hybrid weights.
- Minimum history threshold.

Do not perform uncontrolled parameter searching.

---

## P3-MODEL-007 — Model Artifact Management

**Priority:** P1  
**Status:** `NOT_STARTED`

Ensure trained artifacts are:

- Reproducible.
- Version-compatible.
- Clearly named.
- Loaded by the canonical engine.

---

## P3-MODEL-008 — Model Sanity Checks

**Priority:** P0  
**Status:** `NOT_STARTED`

Check:

- Recommendation count.
- Duplicate recommendations.
- Invalid IDs.
- NaN scores.
- Infinite scores.
- Empty outputs.
- Extreme score values.

---

## PHASE 3 EXIT GATE

- [ ] Baseline implemented.
- [ ] Personalized model implemented.
- [ ] Content model implemented.
- [ ] Matrix factorization evaluated.
- [ ] Hybrid model implemented.
- [ ] Configurations documented.
- [ ] Sanity tests pass.

---

# 12. PHASE 4 — COLD-START STRATEGY

## Objective

Provide technically defensible behavior for users/products with insufficient historical data.

---

## P4-COLD-001 — Define Cold-Start Taxonomy

**Priority:** P0  
**Status:** `NOT_STARTED`

Define:

- New user.
- Sparse user.
- New product.
- Sparse product.

---

## P4-COLD-002 — New User Fallback

**Priority:** P0  
**Status:** `NOT_STARTED`

Implement documented fallback.

Potential path:

```text
Unknown User
    ↓
Popularity
```

---

## P4-COLD-003 — Sparse User Strategy

**Priority:** P0  
**Status:** `NOT_STARTED`

Use content/popularity/personalization according to defined history threshold.

---

## P4-COLD-004 — New Product Candidate Support

**Priority:** P0  
**Status:** `NOT_STARTED`

Ensure a new product with valid metadata can enter the content-based candidate pool.

---

## P4-COLD-005 — Cold-Start Tests

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Completely new user.
- User with one interaction.
- User with sparse history.
- New product.
- Product with metadata but no interaction.
- Empty candidate pool.

---

## P4-COLD-006 — Cold-Start Evaluation

**Priority:** P1  
**Status:** `NOT_STARTED`

Where the evaluation data supports it, separately analyze recommendation behavior for cold-start groups.

---

## PHASE 4 EXIT GATE

- [ ] New-user fallback works.
- [ ] Sparse-user behavior works.
- [ ] New-product behavior works.
- [ ] Candidate generation does not block new products.
- [ ] Cold-start tests pass.
- [ ] Cold-start limitations are documented.

---

# 13. PHASE 5 — EVALUATION

## Objective

Replace the current non-trustworthy evaluation with a valid, reproducible evaluation pipeline.

---

## P5-EVAL-001 — Audit Existing Evaluation Code

**Priority:** P0  
**Status:** `NOT_STARTED`

Inspect:

`src/evaluation/evaluate_recommendations.py`

Tasks:

- [ ] Inspect metric functions.
- [ ] Inspect split logic.
- [ ] Inspect recommendation generation.
- [ ] Inspect candidate handling.
- [ ] Inspect aggregation.
- [ ] Inspect sampling.
- [ ] Inspect leakage risks.

---

## P5-EVAL-002 — Preserve Metric Functions

**Priority:** P0  
**Status:** `NOT_STARTED`

Preserve and validate:

- Precision@K
- Recall@K
- NDCG@K

---

## P5-EVAL-003 — Validate Metric Functions

**Priority:** P0  
**Status:** `NOT_STARTED`

Create controlled test cases where expected results are known.

---

## P5-EVAL-004 — Define Relevance

**Priority:** P0  
**Status:** `NOT_STARTED`

Define exactly what makes an item relevant for evaluation.

---

## P5-EVAL-005 — Resolve Validation Strategy

**Priority:** P0  
**Status:** `NOT_STARTED`

If legitimate timestamps exist:

```text
Historical Data
      ↓
Chronological Ordering
      ↓
Training Period
      ↓
Validation Period
      ↓
Optional Test Period
```

If timestamps do not legitimately exist:

- [ ] Document limitation.
- [ ] Do not fake chronology.
- [ ] Apply the most defensible alternative permitted by the project specification.
- [ ] Clearly label the alternative.

---

## P5-EVAL-006 — Prevent Evaluation Leakage

**Priority:** P0  
**Status:** `NOT_STARTED`

Audit:

- Popularity.
- TF-IDF.
- Collaborative filtering.
- Matrix factorization.
- Candidate generation.
- Feature engineering.

---

## P5-EVAL-007 — Evaluate Popularity

**Priority:** P0  
**Status:** `NOT_STARTED`

Produce verified:

- Precision@K.
- Recall@K.
- NDCG@K.

---

## P5-EVAL-008 — Evaluate Collaborative Filtering

**Priority:** P0  
**Status:** `NOT_STARTED`

Use the same evaluation protocol.

---

## P5-EVAL-009 — Evaluate Matrix Factorization

**Priority:** P1  
**Status:** `NOT_STARTED`

Only if retained as a candidate model.

---

## P5-EVAL-010 — Evaluate Content-Based Model

**Priority:** P0  
**Status:** `NOT_STARTED`

Use the same protocol.

---

## P5-EVAL-011 — Evaluate Hybrid Engine

**Priority:** P0  
**Status:** `NOT_STARTED`

The final RecommendationEngine must be evaluated directly.

---

## P5-EVAL-012 — Remove Placeholder Results

**Priority:** P0  
**Status:** `NOT_STARTED`

No final evaluation report may contain placeholder values.

---

## P5-EVAL-013 — Full Evaluation Population

**Priority:** P0  
**Status:** `NOT_STARTED`

Avoid arbitrary evaluation truncation unless computationally justified.

---

## P5-EVAL-014 — Reproduce Evaluation

**Priority:** P0  
**Status:** `NOT_STARTED`

Run evaluation twice under identical configuration and verify consistency.

---

## P5-EVAL-015 — Generate Final Evaluation Artifacts

**Priority:** P1  
**Status:** `NOT_STARTED`

Potential artifacts:

```text
outputs/
└── reports/
    ├── evaluation_report.*
    ├── model_comparison.*
    └── segment_evaluation.*
```

Exact structure should follow the approved architecture.

---

## PHASE 5 EXIT GATE

- [ ] Metric functions verified.
- [ ] Relevance definition finalized.
- [ ] Validation strategy finalized.
- [ ] Leakage audit passes.
- [ ] Baseline evaluated.
- [ ] Personalized model evaluated.
- [ ] Content model evaluated.
- [ ] Hybrid evaluated.
- [ ] Matrix factorization evaluated if retained.
- [ ] No placeholder results.
- [ ] Evaluation reproducible.
- [ ] Evaluation report generated.

---

# 14. PHASE 6 — USER SEGMENT ANALYSIS

## Objective

Replace the current collapsed user segmentation with meaningful recommendation-quality analysis.

---

## P6-SEG-001 — Audit Existing Segmentation

**Priority:** P1  
**Status:** `NOT_STARTED`

Inspect:

`src/utils/user_segmentation.py`

---

## P6-SEG-002 — Analyze Activity Distribution

**Priority:** P1  
**Status:** `NOT_STARTED`

Determine:

- Interaction distribution.
- Unique users.
- Activity percentiles.
- Sparse-user population.
- Highly active population.

---

## P6-SEG-003 — Define Segmentation Method

**Priority:** P1  
**Status:** `NOT_STARTED`

Possible approaches:

- Quantile-based segmentation.
- Data-driven thresholds.
- History-length segmentation.

Final method must be justified.

---

## P6-SEG-004 — Generate User Segments

**Priority:** P1  
**Status:** `NOT_STARTED`

Produce meaningful segments.

---

## P6-SEG-005 — Validate Segment Distribution

**Priority:** P1  
**Status:** `NOT_STARTED`

Check that the segments are not accidentally collapsed.

---

## P6-SEG-006 — Evaluate Metrics by Segment

**Priority:** P1  
**Status:** `NOT_STARTED`

Calculate:

- Precision@K.
- Recall@K.
- NDCG@K.

for eligible segments.

---

## P6-SEG-007 — Segment Error Analysis

**Priority:** P1  
**Status:** `NOT_STARTED`

Investigate:

- Sparse-user performance.
- High-activity performance.
- Cold-start performance.
- Popularity bias.

---

## P6-SEG-008 — Generate Segment Report

**Priority:** P1  
**Status:** `NOT_STARTED`

Produce a reproducible report.

---

## PHASE 6 EXIT GATE

- [ ] Segmentation is meaningful.
- [ ] Segment sizes are reported.
- [ ] Segment recommendation metrics are calculated.
- [ ] Segment limitations are documented.
- [ ] Segment report is reproducible.

---

# 15. PHASE 7 — FASTAPI + STREAMLIT INTEGRATION

## Objective

Integrate the canonical Recommendation Engine into the existing application layers.

---

## P7-API-001 — Audit FastAPI

**Priority:** P1  
**Status:** `NOT_STARTED`

Inspect:

`api/recommendation_api.py`

---

## P7-API-002 — Integrate Canonical Engine

**Priority:** P0  
**Status:** `NOT_STARTED`

FastAPI must call the canonical RecommendationEngine.

---

## P7-API-003 — Validate `/health`

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify health endpoint.

---

## P7-API-004 — Validate Recommendation Endpoint

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Known user.
- Unknown user.
- Valid K.
- Invalid K.
- Empty result.
- Server errors.

---

## P7-API-005 — Validate Response Schema

**Priority:** P1  
**Status:** `NOT_STARTED`

Ensure consistent JSON response.

---

## P7-API-006 — API Documentation

**Priority:** P1  
**Status:** `NOT_STARTED`

Update:

`docs/api.md`

with final API contract.

---

## P7-APP-001 — Audit Streamlit

**Priority:** P1  
**Status:** `NOT_STARTED`

Inspect:

`app/streamlit_app.py`

---

## P7-APP-002 — Remove Duplicate Recommendation Logic

**Priority:** P0  
**Status:** `NOT_STARTED`

Replace independent Streamlit recommendation calculations with calls to the canonical engine.

---

## P7-APP-003 — Preserve Useful UI

**Priority:** P1  
**Status:** `NOT_STARTED`

Preserve existing useful:

- User selection.
- Recommendation controls.
- Dataset analytics.
- Popular products.
- Segment analysis.

---

## P7-APP-004 — Streamlit Error Handling

**Priority:** P1  
**Status:** `NOT_STARTED`

Handle:

- Unknown users.
- Missing model.
- Empty recommendation result.
- Data loading failure.

---

## P7-APP-005 — Streamlit Manual QA

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify UI manually.

---

## P7-INTEGRATION-001 — API/Streamlit Consistency

**Priority:** P0  
**Status:** `NOT_STARTED`

Given the same user and configuration, API and Streamlit should use the same canonical engine and produce consistent recommendation logic.

---

## PHASE 7 EXIT GATE

- [ ] FastAPI uses canonical engine.
- [ ] API endpoints work.
- [ ] API validation works.
- [ ] Streamlit uses canonical engine.
- [ ] Streamlit UI works.
- [ ] No duplicated recommendation logic.
- [ ] API documentation updated.
- [ ] Integration tests pass.

---

# 16. PHASE 8 — TESTING + QA

## Objective

Verify the entire project systematically.

---

## P8-QA-001 — Repair Dependency Configuration

**Priority:** P0  
**Status:** `NOT_STARTED`

Verify:

- Python dependencies.
- Test framework dependency.
- Version compatibility.
- No unnecessary packages.

---

## P8-QA-002 — Unit Test Data Utilities

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Loading.
- Saving.
- Validation.
- Preprocessing.

---

## P8-QA-003 — Unit Test Models

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Popularity model.
- Collaborative filtering.
- Content model.
- Matrix factorization if retained.

---

## P8-QA-004 — Unit Test Recommendation Engine

**Priority:** P0  
**Status:** `NOT_STARTED`

Test all documented behaviors.

---

## P8-QA-005 — Unit Test Metrics

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Precision@K.
- Recall@K.
- NDCG@K.

---

## P8-QA-006 — API Tests

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Health.
- Recommendation endpoint.
- Validation.
- Error handling.

---

## P8-QA-007 — Integration Tests

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

```text
Data
 ↓
Models
 ↓
RecommendationEngine
 ↓
API
```

---

## P8-QA-008 — Streamlit Verification

**Priority:** P1  
**Status:** `NOT_STARTED`

Perform manual UI QA.

---

## P8-QA-009 — Edge-Case Testing

**Priority:** P0  
**Status:** `NOT_STARTED`

Test:

- Unknown user.
- New product.
- Sparse user.
- Empty data.
- Invalid K.
- Duplicate data.
- Missing metadata.
- No candidates.

---

## P8-QA-010 — Full Test Suite

**Priority:** P0  
**Status:** `NOT_STARTED`

Run complete test suite.

Record:

- Tests collected.
- Tests passed.
- Tests failed.
- Tests skipped.
- Runtime.

---

## P8-QA-011 — Regression Test

**Priority:** P0  
**Status:** `NOT_STARTED`

Verify that repairs did not break preserved components.

---

## P8-QA-012 — Reproducibility Test

**Priority:** P0  
**Status:** `NOT_STARTED`

Perform clean/repeated execution where practical.

---

## PHASE 8 EXIT GATE

- [ ] Dependencies valid.
- [ ] Unit tests pass.
- [ ] Metric tests pass.
- [ ] Recommendation tests pass.
- [ ] API tests pass.
- [ ] Integration tests pass.
- [ ] Edge cases pass.
- [ ] Full suite passes.
- [ ] Regression checks pass.
- [ ] Reproducibility check passes.

---

# 17. PHASE 9 — DOCUMENTATION + GITHUB

## Objective

Bring all project documentation into synchronization with the actual final implementation.

---

## P9-DOC-001 — Update README

**Priority:** P1  
**Status:** `NOT_STARTED`

README must contain:

- Project overview.
- Problem statement.
- Features.
- Dataset.
- Methodology.
- Architecture.
- Models.
- Evaluation.
- Results.
- Setup.
- Usage.
- API.
- Streamlit.
- Limitations.
- Future scope.

---

## P9-DOC-002 — Update Methodology

**Priority:** P1  
**Status:** `NOT_STARTED`

Update:

`docs/methodology.md`

Ensure it matches actual implementation.

---

## P9-DOC-003 — Update Architecture Documentation

**Priority:** P1  
**Status:** `NOT_STARTED`

Update:

`docs/project_architecture.md`

---

## P9-DOC-004 — Update API Documentation

**Priority:** P1  
**Status:** `NOT_STARTED`

Update:

`docs/api.md`

---

## P9-DOC-005 — Generate Final Evaluation Report

**Priority:** P0  
**Status:** `NOT_STARTED`

The report must contain actual verified results.

---

## P9-DOC-006 — Generate Data Analysis Report

**Priority:** P1  
**Status:** `NOT_STARTED`

Include:

- Dataset size.
- Schema.
- Missingness.
- Interaction distribution.
- User distribution.
- Product distribution.
- Relevant EDA findings.

---

## P9-DOC-007 — Generate Model Comparison Report

**Priority:** P0  
**Status:** `NOT_STARTED`

Compare retained models using verified evaluation results.

---

## P9-DOC-008 — Generate Error Analysis Report

**Priority:** P1  
**Status:** `NOT_STARTED`

Document:

- Failure patterns.
- Cold-start issues.
- Sparse-user behavior.
- Segment differences.
- Popularity bias.

---

## P9-GIT-001 — Repository Audit

**Priority:** P1  
**Status:** `NOT_STARTED`

Check:

- Source files.
- Data files.
- Documentation.
- Tests.
- Configuration.
- Generated artifacts.
- Secrets.
- Unnecessary files.

---

## P9-GIT-002 — Dependency Audit

**Priority:** P1  
**Status:** `NOT_STARTED`

Ensure dependencies are:

- Required.
- Correct.
- Version-compatible.
- Documented.

---

## P9-GIT-003 — Git History Cleanup

**Priority:** P2  
**Status:** `NOT_STARTED`

Ensure commits are understandable and meaningful.

---

## P9-GIT-004 — GitHub Verification

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify repository:

- Opens successfully.
- README renders correctly.
- Project structure is understandable.
- Setup instructions work.
- No secrets exist.
- No broken links exist.

---

## PHASE 9 EXIT GATE

- [ ] README complete.
- [ ] Methodology accurate.
- [ ] Architecture accurate.
- [ ] API documentation accurate.
- [ ] Evaluation report complete.
- [ ] Error analysis complete.
- [ ] Repository clean.
- [ ] Dependencies correct.
- [ ] GitHub verified.

---

# 18. PHASE 10 — FINAL CAPSTONE QA

## Objective

Perform a complete final audit before declaring Project 3 complete.

---

## P10-FINAL-001 — Requirement Traceability Audit

**Priority:** P0  
**Status:** `NOT_STARTED`

Verify every P0/P1 requirement.

---

## P10-FINAL-002 — Data Audit

**Priority:** P0  
**Status:** `NOT_STARTED`

Verify:

- Source.
- Schema.
- Provenance.
- Interaction semantics.
- Timestamp status.
- Leakage.

---

## P10-FINAL-003 — ML Audit

**Priority:** P0  
**Status:** `NOT_STARTED`

Verify:

- Baseline.
- Collaborative filtering.
- Matrix factorization if retained.
- Content model.
- Hybrid model.
- Cold-start.

---

## P10-FINAL-004 — Evaluation Audit

**Priority:** P0  
**Status:** `NOT_STARTED`

Verify:

- Precision@K.
- Recall@K.
- NDCG@K.
- Validation methodology.
- Leakage prevention.
- Actual model evaluation.
- Reproducibility.

---

## P10-FINAL-005 — API Audit

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify all endpoints.

---

## P10-FINAL-006 — Streamlit Audit

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify:

- Startup.
- UI.
- Recommendation flow.
- Analytics.
- Error handling.

---

## P10-FINAL-007 — Testing Audit

**Priority:** P0  
**Status:** `NOT_STARTED`

Verify complete test suite.

---

## P10-FINAL-008 — Documentation Audit

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify that documentation does not claim functionality that does not exist.

---

## P10-FINAL-009 — Reproducibility Audit

**Priority:** P0  
**Status:** `NOT_STARTED`

Attempt to reproduce:

1. Environment setup.
2. Data preparation.
3. Model training.
4. Evaluation.
5. Application startup.

---

## P10-FINAL-010 — Final GitHub Audit

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify repository is presentation-ready.

---

## P10-FINAL-011 — Final Interview Readiness Audit

**Priority:** P1  
**Status:** `NOT_STARTED`

Verify that the project owner can explain:

- Dataset.
- Interaction representation.
- Popularity baseline.
- Collaborative filtering.
- Matrix factorization.
- Content-based filtering.
- Hybrid recommendation.
- Cold-start.
- Precision@K.
- Recall@K.
- NDCG@K.
- Temporal validation.
- Leakage prevention.
- Segmentation.
- API architecture.
- System limitations.

---

# 19. FINAL PROJECT CHECKLIST

## Documentation

- [x] `PRD.md`
- [x] `PROJECT_SPECIFICATIONS.md`
- [x] `DATASET_AND_DATA_STRATEGY.md`
- [x] `ML_METHODOLOGY.md`
- [x] `EXPERIMENT_PLAN.md`
- [x] `EVALUATION_AND_ERROR_ANALYSIS.md`
- [x] `SYSTEM_ARCHITECTURE.md`
- [ ] `TASK_TRACKER.md`
- [ ] `RULES.md`
- [ ] `DOCUMENTATION_AND_REPORTING.md`
- [ ] `README.md`

---

## Data

- [ ] Legitimate dataset source verified.
- [ ] Required raw data restored.
- [ ] Required processed data generated.
- [ ] Dataset schema verified.
- [ ] Interaction semantics documented.
- [ ] Product metadata verified.
- [ ] Timestamp source investigated.
- [ ] Timestamp strategy resolved.
- [ ] Data leakage audit passed.

---

## Recommendation Models

- [ ] Popularity baseline.
- [ ] Collaborative filtering.
- [ ] Matrix factorization evaluation.
- [ ] Content-based model.
- [ ] Hybrid model.
- [ ] Cold-start strategy.
- [ ] Canonical RecommendationEngine.

---

## Evaluation

- [ ] Precision@K.
- [ ] Recall@K.
- [ ] NDCG@K.
- [ ] Valid validation protocol.
- [ ] Temporal validation where legitimately possible.
- [ ] Leakage prevention.
- [ ] Model comparison.
- [ ] Segment evaluation.
- [ ] Error analysis.

---

## Application

- [ ] FastAPI.
- [ ] Health endpoint.
- [ ] Recommendation endpoint.
- [ ] API validation.
- [ ] API error handling.
- [ ] Streamlit.
- [ ] Streamlit recommendation flow.
- [ ] Streamlit analytics.
- [ ] API/Streamlit canonical engine consistency.

---

## Testing

- [ ] Data tests.
- [ ] Model tests.
- [ ] Recommendation tests.
- [ ] Metric tests.
- [ ] API tests.
- [ ] Integration tests.
- [ ] Edge-case tests.
- [ ] Regression tests.
- [ ] Full test suite.

---

## Reproducibility

- [ ] Dependencies.
- [ ] Configuration.
- [ ] Dataset acquisition.
- [ ] Data preprocessing.
- [ ] Model training.
- [ ] Evaluation.
- [ ] API startup.
- [ ] Streamlit startup.

---

## GitHub

- [ ] README.
- [ ] Documentation.
- [ ] No secrets.
- [ ] No unnecessary generated files.
- [ ] No broken links.
- [ ] Clean project structure.
- [ ] Meaningful commits.
- [ ] Repository verified.

---

# 20. CRITICAL BLOCKERS REGISTER

| Blocker ID | Issue | Priority | Status | Resolution |
|---|---|---:|---|---|
| B-001 | Missing core dataset files | P0 | `OPEN` | Restore legitimate data |
| B-002 | Missing timestamp | P0 | `OPEN` | Investigate legitimate source |
| B-003 | Interaction-type mismatch | P0 | `OPEN` | Define legitimate interaction representation |
| B-004 | Evaluation not trustworthy | P0 | `OPEN` | Rebuild evaluation |
| B-005 | Fragmented recommendation logic | P0 | `OPEN` | Establish canonical engine |
| B-006 | Cold-start candidate restriction | P0 | `OPEN` | Fix candidate generation |
| B-007 | User segment collapse | P1 | `OPEN` | Redesign segmentation |
| B-008 | Evaluation leakage risk | P0 | `OPEN` | Audit and isolate training/evaluation |
| B-009 | Test environment incomplete | P0 | `OPEN` | Repair dependencies/data |
| B-010 | Documentation inconsistencies | P1 | `OPEN` | Synchronize docs after implementation |

---

# 21. TECHNICAL DEBT REGISTER

## TD-001 — Fragmented Recommendation Logic

**Impact:** High

The same conceptual recommendation functionality exists in multiple implementations.

### Resolution

Centralize recommendation generation.

---

## TD-002 — Hardcoded Hybrid Weights

**Impact:** Medium

Existing weights may not be empirically justified.

### Resolution

Make configurable and evaluate experimentally.

---

## TD-003 — Candidate Pool Restriction

**Impact:** High

Current popularity-based restriction can prevent cold-start products from being considered.

### Resolution

Redesign candidate generation.

---

## TD-004 — Random Evaluation Split

**Impact:** Critical

Does not satisfy temporal validation.

### Resolution

Legitimate temporal source investigation and evaluation redesign.

---

## TD-005 — Evaluation Heuristic Divergence

**Impact:** Critical

Evaluation may not represent the actual recommendation engine.

### Resolution

Evaluate canonical engine directly.

---

## TD-006 — User Segment Collapse

**Impact:** High

Existing thresholds create nearly unusable segment distribution.

### Resolution

Data-driven segmentation.

---

## TD-007 — Missing Processed Artifacts

**Impact:** Critical

Downstream pipeline cannot run.

### Resolution

Reproducible data generation.

---

## TD-008 — Dependency Configuration

**Impact:** Medium

Test environment currently has dependency issues.

### Resolution

Audit and repair dependency declarations.

---

# 22. DECISION LOG

Important technical decisions shall be recorded here.

| Decision ID | Decision | Rationale | Date | Status |
|---|---|---|---|---|
| D-001 | Preserve RecommendationEngine | Existing implementation is a useful foundation | TBD | Approved |
| D-002 | Preserve FastAPI | Existing architecture is usable | TBD | Approved |
| D-003 | Preserve Streamlit structure | Existing UI provides useful functionality | TBD | Approved |
| D-004 | Preserve ranking metric functions | Existing metric implementations are useful foundations | TBD | Approved |
| D-005 | No fabricated behavioral events | Maintains data integrity | TBD | Approved |
| D-006 | No fabricated timestamps | Prevents invalid temporal evaluation | TBD | Approved |
| D-007 | No unnecessary frontend frameworks | Project stack is already appropriate | TBD | Approved |
| D-008 | Establish one canonical recommendation engine | Prevents API/UI/evaluation divergence | TBD | Approved |

Additional decisions shall be appended rather than overwriting previous decisions.

---

# 23. EXPERIMENT RESULT TRACKING

Final verified experiment results shall be recorded here after execution.

| Experiment | Model | Validation | K | Precision@K | Recall@K | NDCG@K | Status |
|---|---|---|---:|---:|---:|---:|---|
| EXP-001 | Popularity | TBD | TBD | TBD | TBD | TBD | `PENDING` |
| EXP-002 | Collaborative Filtering | TBD | TBD | TBD | TBD | TBD | `PENDING` |
| EXP-003 | Matrix Factorization | TBD | TBD | TBD | TBD | TBD | `PENDING` |
| EXP-004 | Content-Based | TBD | TBD | TBD | TBD | TBD | `PENDING` |
| EXP-005 | Hybrid | TBD | TBD | TBD | TBD | TBD | `PENDING` |

### Important

`TBD` values are permitted in the **planning tracker only**.

They must not appear in the final evaluation report after the corresponding experiment has been executed.

---

# 24. SEGMENT RESULT TRACKING

Final verified segment results shall be recorded after Phase 6.

| Segment | Users | Precision@K | Recall@K | NDCG@K | Notes | Status |
|---|---:|---:|---:|---:|---|---|
| Segment A | TBD | TBD | TBD | TBD | TBD | `PENDING` |
| Segment B | TBD | TBD | TBD | TBD | TBD | `PENDING` |
| Segment C | TBD | TBD | TBD | TBD | TBD | `PENDING` |

Segment names must be replaced with the actual validated segmentation strategy.

---

# 25. REPRODUCIBILITY CHECKLIST

Before final completion:

## Environment

- [ ] Python version documented.
- [ ] Dependencies installed.
- [ ] Dependency versions verified.
- [ ] Environment setup documented.

## Data

- [ ] Source documented.
- [ ] Acquisition reproducible.
- [ ] Processing reproducible.

## Models

- [ ] Configuration documented.
- [ ] Random seeds controlled where applicable.
- [ ] Training reproducible.

## Evaluation

- [ ] Evaluation command documented.
- [ ] Validation methodology documented.
- [ ] Results reproducible.

## Application

- [ ] API startup documented.
- [ ] Streamlit startup documented.
- [ ] Example requests documented.

---

# 26. FINAL QA EVIDENCE REGISTER

Every critical completion claim should have evidence.

| Evidence ID | Area | Evidence | Location | Status |
|---|---|---|---|---|
| EV-001 | Data | Dataset validation output | TBD | `PENDING` |
| EV-002 | Models | Training output | TBD | `PENDING` |
| EV-003 | Evaluation | Final metrics | TBD | `PENDING` |
| EV-004 | Temporal Validation | Split evidence | TBD | `PENDING` |
| EV-005 | Recommendation Engine | Integration test | TBD | `PENDING` |
| EV-006 | API | API test output | TBD | `PENDING` |
| EV-007 | Streamlit | Manual QA evidence | TBD | `PENDING` |
| EV-008 | Tests | Full test-suite output | TBD | `PENDING` |
| EV-009 | Reproducibility | Re-run evidence | TBD | `PENDING` |
| EV-010 | GitHub | Final repository audit | TBD | `PENDING` |

---

# 27. CHANGE CONTROL

Any major change to the project shall be recorded before or immediately after implementation.

Examples:

- Changing dataset.
- Changing interaction definition.
- Changing evaluation methodology.
- Adding/removing model.
- Changing RecommendationEngine architecture.
- Changing API contract.
- Changing Streamlit behavior.
- Adding dependency.
- Removing dependency.
- Deleting project files.
- Changing validation strategy.

Each change should record:

```text
Change ID
Date
Description
Reason
Affected Documents
Affected Code
Risk
Decision
Verification
```

---

# 28. AI CODING TOOL SAFETY CHECKLIST

Before allowing Google AI Studio or another coding agent to modify the repository, verify that the prompt explicitly requires:

- [ ] Read all control documents first.
- [ ] Read existing repository before editing.
- [ ] Preserve existing valid implementation.
- [ ] Do not delete files without explicit permission.
- [ ] Do not add unnecessary technologies.
- [ ] Do not migrate to React/Vite/TypeScript/Tailwind.
- [ ] Do not fabricate data.
- [ ] Do not fabricate timestamps.
- [ ] Do not fabricate metrics.
- [ ] Do not rewrite working components unnecessarily.
- [ ] Run tests after changes.
- [ ] Report changed files.
- [ ] Report deleted files.
- [ ] Report added files.
- [ ] Report test results.
- [ ] Stop if a requirement cannot be fulfilled legitimately.

---

# 29. MASTER IMPLEMENTATION ORDER

The implementation should follow this sequence unless a documented dependency requires otherwise:

```text
1. Read all control documents
        ↓
2. Audit current repository
        ↓
3. Resolve dataset/provenance
        ↓
4. Resolve timestamp question
        ↓
5. Restore data foundation
        ↓
6. Validate data
        ↓
7. Repair data utilities
        ↓
8. Validate popularity model
        ↓
9. Validate collaborative filtering
        ↓
10. Validate matrix factorization
        ↓
11. Validate content model
        ↓
12. Fix candidate generation
        ↓
13. Build canonical RecommendationEngine
        ↓
14. Implement cold-start strategy
        ↓
15. Build valid evaluation pipeline
        ↓
16. Evaluate all retained models
        ↓
17. Perform error analysis
        ↓
18. Build meaningful user segmentation
        ↓
19. Perform segment evaluation
        ↓
20. Integrate FastAPI
        ↓
21. Integrate Streamlit
        ↓
22. Run complete tests
        ↓
23. Verify reproducibility
        ↓
24. Update documentation
        ↓
25. Final GitHub audit
        ↓
26. Final capstone QA
```

---

# 30. PHASE COMPLETION SUMMARY

| Phase | Required Exit Condition | Status |
|---|---|---|
| Phase 0 | All control documents complete | `IN_PROGRESS` |
| Phase 1 | Data foundation valid and reproducible | `NOT_STARTED` |
| Phase 2 | Canonical RecommendationEngine established | `NOT_STARTED` |
| Phase 3 | Models implemented and sanity-checked | `NOT_STARTED` |
| Phase 4 | Cold-start strategy verified | `NOT_STARTED` |
| Phase 5 | Evaluation valid and reproducible | `NOT_STARTED` |
| Phase 6 | Segment analysis meaningful | `NOT_STARTED` |
| Phase 7 | API + Streamlit integrated | `NOT_STARTED` |
| Phase 8 | Full QA suite passes | `NOT_STARTED` |
| Phase 9 | Documentation/GitHub complete | `NOT_STARTED` |
| Phase 10 | Final capstone audit passes | `NOT_STARTED` |

---

# 31. FINAL P0 REQUIREMENTS

The following requirements are considered absolute blockers for project completion:

- [ ] Legitimate dataset source.
- [ ] Valid data foundation.
- [ ] Correct interaction representation.
- [ ] No fabricated behavioral events.
- [ ] Timestamp situation honestly resolved.
- [ ] No fabricated temporal validation.
- [ ] Popularity baseline.
- [ ] Personalized recommendation model.
- [ ] Content-based recommendation where applicable.
- [ ] Cold-start handling.
- [ ] Canonical RecommendationEngine.
- [ ] Valid Precision@K.
- [ ] Valid Recall@K.
- [ ] Valid NDCG@K.
- [ ] Valid evaluation methodology.
- [ ] Leakage prevention.
- [ ] Actual-model evaluation.
- [ ] API integration.
- [ ] Full testing.
- [ ] Reproducibility.
- [ ] Accurate final documentation.

---

# 32. FINAL P1 REQUIREMENTS

The following should be complete before final submission:

- [ ] Matrix-factorization comparison where applicable.
- [ ] Meaningful user segmentation.
- [ ] Segment-level evaluation.
- [ ] Error analysis.
- [ ] Streamlit integration.
- [ ] API documentation.
- [ ] Methodology documentation.
- [ ] Architecture documentation.
- [ ] Professional README.
- [ ] GitHub repository audit.
- [ ] Interview-readiness verification.

---

# 33. PROJECT COMPLETION RULE

The project shall not be marked:

```text
COMPLETE
```

until:

```text
All P0 requirements
        +
Critical P1 requirements
        +
Final QA
        +
Documentation audit
        +
Reproducibility verification
```

have passed.

---

# 34. FINAL PROJECT STATE

The final desired state is:

```text
                    PROJECT 3
                        │
                        ▼
              ┌──────────────────┐
              │ Legitimate Data  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Valid Interaction│
              │ Representation   │
              └────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      Popularity       CF          Content
          │            │            │
          │            ▼            │
          │           MF            │
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Canonical        │
              │ Recommendation   │
              │ Engine           │
              └────────┬─────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       FastAPI API          Streamlit
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Valid Evaluation │
              │ Precision@K      │
              │ Recall@K         │
              │ NDCG@K           │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Segment Analysis │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Error Analysis   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Testing + QA     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Reproducibility  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Documentation    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Final Capstone   │
              │ Ready            │
              └──────────────────┘
```

---

# 35. FINAL TRACKER PRINCIPLE

This tracker must remain synchronized with the actual repository.

When a task changes state:

1. Update its status.
2. Record relevant evidence.
3. Record blockers if any.
4. Update dependent tasks where necessary.
5. Do not mark a task `VERIFIED` without verification evidence.
6. Do not hide failed tasks by deleting them.
7. Do not mark a requirement complete merely because an AI coding tool claims completion.

The tracker represents the **actual state of Project 3**, not the intended state.

---

# 36. FINAL DECLARATION

Project 3 shall be considered successfully completed only when the repository demonstrates:

> **A legitimate data foundation, a coherent and unified recommendation architecture, validated recommendation models, defensible cold-start behavior, trustworthy ranking evaluation, meaningful user-segment analysis, integrated FastAPI and Streamlit applications, passing tests, reproducible execution, accurate documentation, and a professionally maintained GitHub repository.**

The objective is not merely to finish the code.

The objective is to produce a recommendation system that can withstand:

- Internship evaluation
- Code review
- ML methodology review
- Technical demonstration
- GitHub inspection
- Resume/portfolio presentation
- Technical interview questioning

without relying on fabricated data, fabricated results, unsupported claims, or unnecessary technology.

---

**END OF TASK_TRACKER.md**
