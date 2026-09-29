# SYSTEM_ARCHITECTURE.md

# System Architecture
## Personalized Product Recommendation Model

---

## Document Control

| Field | Value |
|---|---|
| Project | Personalized Product Recommendation Model |
| Project Number | Project 3 |
| Document | System Architecture |
| Version | 1.0 |
| Status | Approved Architecture Baseline |
| Architecture Type | Modular ML + API + Application Architecture |
| Primary Language | Python |
| ML Framework | Scikit-learn / SciPy |
| API Framework | FastAPI |
| Application Framework | Streamlit |
| Version Control | Git / GitHub |
| Primary Recommendation Component | `RecommendationEngine` |
| Parent Documents | `PRD.md`, `PROJECT_SPECIFICATIONS.md` |
| Supporting Documents | `DATASET_AND_DATA_STRATEGY.md`, `ML_METHODOLOGY.md`, `EXPERIMENT_PLAN.md`, `EVALUATION_AND_ERROR_ANALYSIS.md` |
| Architecture Objective | Establish one coherent, reproducible recommendation system while preserving valid existing repository components |

---

# 1. PURPOSE

This document defines the complete technical architecture of the Personalized Product Recommendation Model.

It specifies:

- System boundaries
- Architectural principles
- Repository structure
- Component responsibilities
- Data flow
- Model flow
- Recommendation flow
- Training architecture
- Evaluation architecture
- API architecture
- Streamlit architecture
- Cold-start architecture
- Configuration architecture
- Testing architecture
- Artifact management
- Dependency relationships
- Runtime behavior
- Error handling
- Reproducibility
- Deployment-oriented structure
- Architectural constraints
- Preservation of existing components
- Target-state architecture
- Migration from the current audited state to the final system

This document is an architectural blueprint.

It does not itself constitute evidence that every component described below is already implemented.

The architecture represents the **approved target state** toward which the existing repository will be incrementally repaired and integrated.

---

# 2. ARCHITECTURAL OBJECTIVE

The system shall transform legitimate source data into ranked personalized product recommendations through a coherent pipeline:

```text
Data Source
    ↓
Data Acquisition / Restoration
    ↓
Data Validation
    ↓
Preprocessing
    ↓
Interaction Representation
    ↓
Model Training
    ├── Popularity Baseline
    ├── Collaborative Filtering
    ├── Matrix Factorization
    └── Content-Based Model
            ↓
      Candidate Generation
            ↓
      Candidate Filtering
            ↓
      Score Generation
            ↓
      Score Normalization
            ↓
      Hybrid Ranking
            ↓
      Cold-Start / Fallback Logic
            ↓
      Canonical RecommendationEngine
            ↓
       ┌────┴────┐
       ↓         ↓
    FastAPI   Streamlit
       │         │
       └────┬────┘
            ↓
       End User / Client
````

Evaluation runs alongside the modeling/recommendation lifecycle:

```text
Training Data
      ↓
Models
      ↓
Recommendation Engine
      ↓
Evaluation Pipeline
      ↓
Precision@K
Recall@K
NDCG@K
      ↓
Segment Analysis
      ↓
Error Analysis
      ↓
Verified Results
```

---

# 3. ARCHITECTURAL PHILOSOPHY

The architecture follows the following principles.

## 3.1 Correctness Before Complexity

The architecture must favor a simple and correct design over unnecessary technical complexity.

---

## 3.2 Preserve Valid Existing Work

The current repository already contains useful components.

The following are architectural assets and should be preserved wherever technically valid:

* `RecommendationEngine`
* FastAPI structure
* Streamlit structure
* Popularity model
* Collaborative filtering implementation
* Content-based implementation
* Metric implementations
* `data_utils.py`
* Existing Python module organization

The goal is:

> **Repair + integrate + validate, not blindly rebuild.**

---

## 3.3 One Canonical Recommendation Pipeline

The most important architectural rule is:

> **There must be one canonical recommendation pipeline.**

FastAPI, Streamlit, and evaluation must not each implement their own recommendation formula.

The architecture shall therefore follow:

```text
                    ┌───────────────────┐
                    │ Recommendation    │
                    │ Engine             │
                    └─────────┬─────────┘
                              │
                ┌─────────────┼─────────────┐
                ↓             ↓             ↓
              API         Streamlit     Evaluation
```

---

## 3.4 Separation of Concerns

Each architectural layer should have one primary responsibility.

```text
Data Layer
    ↓
Model Layer
    ↓
Recommendation Layer
    ↓
Evaluation Layer
    ↓
Application Layer
```

No layer should silently take over responsibilities belonging to another layer.

---

## 3.5 No Fabricated Data

The architecture must never require fabricated:

* Views
* Clicks
* Carts
* Purchases
* Timestamps
* User behavior

If derived representations are required, they must be explicitly identified as derived.

---

## 3.6 No Fabricated Evaluation

The architecture must never generate:

* Artificial performance numbers
* Placeholder final metrics
* Synthetic temporal validation presented as real
* Unsupported model rankings

---

## 3.7 Reproducibility

The architecture must make it possible to reproduce:

```text
Data
    ↓
Preprocessing
    ↓
Training
    ↓
Evaluation
    ↓
Results
```

from documented configuration and commands.

---

# 4. SYSTEM BOUNDARY

The system boundary includes:

```text
┌──────────────────────────────────────────────────────┐
│ Personalized Product Recommendation System          │
│                                                      │
│  Data                                                │
│  Preprocessing                                       │
│  Models                                              │
│  Recommendation Engine                               │
│  Evaluation                                         │
│  API                                                 │
│  Streamlit                                           │
│  Tests                                               │
│  Configuration                                       │
└──────────────────────────────────────────────────────┘
```

External systems may include:

* Dataset source
* GitHub
* User/client applications
* Browser
* Runtime environment

The system does not require:

* Microservices
* Kubernetes
* Kafka
* Distributed training
* Cloud-native orchestration
* React
* Vite
* TypeScript
* Tailwind CSS

unless a future requirement explicitly introduces them.

---

# 5. HIGH-LEVEL ARCHITECTURE

```text
                              ┌─────────────────────┐
                              │  Legitimate Dataset │
                              │       Source        │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ Data Acquisition /  │
                              │ Restoration         │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ Data Validation     │
                              │ & Quality Checks    │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ Preprocessing &      │
                              │ Normalization       │
                              └──────────┬──────────┘
                                         │
                                         ▼
                         ┌──────────────────────────────┐
                         │ User-Item Interaction Layer  │
                         └──────────────┬───────────────┘
                                        │
                ┌───────────────────────┼───────────────────────┐
                │                       │                       │
                ▼                       ▼                       ▼
       ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
       │ Popularity     │      │ Collaborative  │      │ Content-Based  │
       │ Baseline       │      │ Filtering      │      │ Model          │
       └───────┬────────┘      └───────┬────────┘      └───────┬────────┘
               │                       │                       │
               │                       ▼                       │
               │               ┌────────────────┐              │
               │               │ Matrix         │              │
               │               │ Factorization  │              │
               │               └───────┬────────┘              │
               │                       │                       │
               └───────────────────────┼───────────────────────┘
                                       │
                                       ▼
                           ┌────────────────────────┐
                           │ Candidate Generation   │
                           └────────────┬───────────┘
                                        │
                                        ▼
                           ┌────────────────────────┐
                           │ Candidate Filtering    │
                           └────────────┬───────────┘
                                        │
                                        ▼
                           ┌────────────────────────┐
                           │ Score Generation       │
                           └────────────┬───────────┘
                                        │
                                        ▼
                           ┌────────────────────────┐
                           │ Score Normalization    │
                           └────────────┬───────────┘
                                        │
                                        ▼
                           ┌────────────────────────┐
                           │ Hybrid Ranking         │
                           └────────────┬───────────┘
                                        │
                                        ▼
                           ┌────────────────────────┐
                           │ Cold-Start / Fallback   │
                           │ Resolution              │
                           └────────────┬───────────┘
                                        │
                                        ▼
                           ┌────────────────────────┐
                           │ RecommendationEngine    │
                           │       (Canonical)       │
                           └────────────┬───────────┘
                                        │
                          ┌─────────────┴─────────────┐
                          │                           │
                          ▼                           ▼
                ┌──────────────────┐       ┌──────────────────┐
                │ FastAPI          │       │ Streamlit        │
                │ Recommendation   │       │ Application       │
                │ Service          │       │                  │
                └────────┬─────────┘       └────────┬─────────┘
                         │                          │
                         └────────────┬─────────────┘
                                      ▼
                                  End User
```

---

# 6. ARCHITECTURAL LAYERS

The system is divided into the following logical layers.

| Layer                          | Primary Responsibility                           |
| ------------------------------ | ------------------------------------------------ |
| Data Layer                     | Acquisition, storage, validation, preprocessing  |
| Feature / Representation Layer | User-item and product representations            |
| Model Layer                    | Train recommendation models                      |
| Recommendation Layer           | Candidate generation, scoring, ranking, fallback |
| Evaluation Layer               | Metrics, validation, comparison, error analysis  |
| Service Layer                  | FastAPI endpoints                                |
| Application Layer              | Streamlit UI                                     |
| Configuration Layer            | Centralized configuration                        |
| Testing Layer                  | Unit, integration, API, evaluation tests         |
| Documentation Layer            | Architecture, methodology, results               |
| Repository Layer               | Git/GitHub management                            |

---

# 7. DATA LAYER

## 7.1 Responsibility

The Data Layer is responsible for:

* Obtaining the legitimate dataset.
* Restoring missing source files.
* Validating schema.
* Cleaning data.
* Handling missing values.
* Constructing interaction representations.
* Producing processed artifacts.

---

## 7.2 Data Flow

```text
External Dataset
      ↓
Raw Data
      ↓
Schema Validation
      ↓
Data Quality Checks
      ↓
Cleaning
      ↓
Interaction Construction
      ↓
Processed Data
```

---

## 7.3 Raw Data

Raw data should remain as close as practical to the original source.

Example conceptual structure:

```text
data/
└── raw/
    ├── source_data.csv
    ├── train.csv
    └── test.csv
```

The exact final filenames depend on the recovered dataset strategy.

---

## 7.4 Processed Data

Processed artifacts may include:

```text
data/
└── processed/
    ├── interactions.csv
    ├── products.csv
    ├── users.csv
    ├── popular_products.csv
    └── user_segment_summary.csv
```

These filenames reflect the existing project structure where applicable.

They must not be created merely to satisfy a filename expectation.

Each artifact must have a documented purpose and reproducible generation process.

---

# 8. DATA VALIDATION ARCHITECTURE

Before modeling, the data shall pass through validation.

```text
Raw Data
   │
   ▼
Schema Validation
   │
   ├── Required Columns?
   ├── Correct Data Types?
   ├── Valid IDs?
   ├── Missing Values?
   ├── Duplicate Records?
   ├── Valid Interaction Values?
   └── Timestamp Validity?
   │
   ▼
Validated Data
```

If validation fails:

```text
Validation Failure
       ↓
Stop Downstream Processing
       ↓
Report Error
```

The system must not silently continue using invalid data.

---

# 9. TIMESTAMP ARCHITECTURE

The project has a specific architectural requirement around temporal validation.

The currently audited dataset lacks timestamps.

Therefore the architecture must support two controlled states.

## State A — Legitimate Timestamp Available

```text
Source
  ↓
Timestamp Validation
  ↓
Chronological Ordering
  ↓
Temporal Train/Validation Split
  ↓
Leakage-Controlled Training
  ↓
Evaluation
```

---

## State B — No Legitimate Timestamp Available

```text
Source
  ↓
No Timestamp
  ↓
Document Limitation
  ↓
Do NOT fabricate chronology
  ↓
Use only a defensible alternative
  ↓
Clearly report limitation
```

The architecture must never silently convert State B into State A.

---

# 10. INTERACTION REPRESENTATION LAYER

The Interaction Representation Layer converts source records into a form usable by recommendation algorithms.

Conceptually:

```text
User
   │
   ├── Interaction ──> Product
   │
   └── Interaction Value
```

Example abstract representation:

```text
user_id
item_id
interaction_value
timestamp (if legitimate)
```

The architecture must preserve the semantics of the actual source data.

---

# 11. MODEL LAYER

The Model Layer contains independent recommendation components.

```text
                    Model Layer
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
  Popularity      Collaborative      Content-Based
    Model            Model              Model
                         │
                         ▼
                 Matrix Factorization
```

Each model must have:

* Defined inputs
* Defined outputs
* Training method
* Configuration
* Evaluation method
* Error behavior

---

# 12. POPULARITY MODEL

## 12.1 Purpose

The popularity model provides:

* Baseline recommendations
* New-user fallback
* General fallback
* Comparison reference

---

## 12.2 Architecture

```text
Training Interactions
        ↓
Popularity Aggregation
        ↓
Product Ranking
        ↓
Popularity Candidate List
```

---

## 12.3 Data Isolation

For temporal evaluation, popularity statistics must be calculated only from permitted training information.

It must not include future validation interactions.

---

# 13. COLLABORATIVE FILTERING MODEL

## 13.1 Purpose

Collaborative filtering uses similarities or shared interaction patterns between users/items.

---

## 13.2 Architecture

```text
User-Item Matrix
      ↓
Similarity Computation
      ↓
Neighbor Selection
      ↓
Candidate Scoring
      ↓
Ranked Recommendations
```

---

## 13.3 Existing Implementation

The existing collaborative filtering component should be preserved and evaluated.

Its final integration must occur through the canonical Recommendation Engine.

---

# 14. MATRIX FACTORIZATION MODEL

## 14.1 Purpose

Matrix factorization provides a latent representation of users/items.

Conceptually:

```text
User-Item Matrix
       ↓
Factorization
       ↓
User Latent Factors
       +
Item Latent Factors
       ↓
Predicted Affinity
       ↓
Ranked Recommendations
```

---

## 14.2 Architectural Role

Matrix factorization is a candidate personalized model.

It must not automatically become the final model simply because it exists in the repository.

It must first be:

* Validated
* Integrated
* Evaluated
* Compared

---

# 15. CONTENT-BASED MODEL

## 15.1 Purpose

The content-based component recommends products based on product metadata similarity.

---

## 15.2 Existing Approach

The audited project contains a TF-IDF/cosine-similarity implementation based on available product text.

The architecture should preserve this where appropriate.

---

## 15.3 Architecture

```text
Product Metadata
      ↓
Text Preprocessing
      ↓
TF-IDF Representation
      ↓
Product Feature Matrix
      ↓
Cosine Similarity
      ↓
Similar Product Candidates
```

---

# 16. COLD-START ARCHITECTURE

Cold-start handling is a first-class architectural concern.

---

## 16.1 New User

```text
User Request
     ↓
User Exists?
     │
   NO
     ↓
Popularity / Approved Fallback
     ↓
Recommendations
```

---

## 16.2 Sparse User

```text
User Request
     ↓
Sufficient History?
     │
   NO
     ↓
Content / Popularity Fallback
     ↓
Recommendations
```

---

## 16.3 Established User

```text
User Request
     ↓
Sufficient History
     ↓
Personalized Model
     ↓
Content Augmentation
     ↓
Hybrid Ranking
```

---

## 16.4 New Product

A new product should not be automatically excluded merely because it has little or no interaction history.

Where metadata exists:

```text
New Product
     ↓
Product Metadata
     ↓
Content Representation
     ↓
Similarity / Candidate Generation
     ↓
Recommendation Candidate
```

---

# 17. CANDIDATE GENERATION ARCHITECTURE

Candidate generation and ranking shall be separate concepts.

```text
Potential Product Universe
          ↓
Candidate Generation
          ↓
Candidate Pool
          ↓
Filtering
          ↓
Scoring
          ↓
Ranking
          ↓
Top-K
```

Candidate generation may receive candidates from:

* Popularity
* Collaborative filtering
* Matrix factorization
* Content similarity
* Other approved recommendation components

---

# 18. CANDIDATE FILTERING

Candidate filtering may remove products that are not eligible for recommendation.

Examples:

* Already interacted products
* Invalid products
* Missing product records
* Explicitly excluded items

However:

> Candidate filtering must not unintentionally destroy cold-start coverage.

---

# 19. SCORE GENERATION

Each model may generate its own score.

Conceptually:

```text
Item A
 ├── Collaborative Score
 ├── Content Score
 └── Popularity Score
```

These scores may have different ranges.

Therefore they must not be combined blindly.

---

# 20. SCORE NORMALIZATION

Where multiple model outputs are combined:

```text
Raw Model Scores
       ↓
Score Normalization
       ↓
Comparable Score Scales
       ↓
Hybrid Combination
```

The normalization method must be documented.

---

# 21. HYBRID RECOMMENDATION ARCHITECTURE

The final Recommendation Engine may combine:

```text
Collaborative Signal
        +
Content Signal
        +
Popularity Signal
        ↓
Normalized Signals
        ↓
Weighted Combination
        ↓
Final Ranking
```

Example conceptual representation:

```text
Final Score =
    w_cf × CF Score
  + w_cb × Content Score
  + w_pop × Popularity Score
```

The actual weights are not fixed by this architecture.

They must be determined and documented through the methodology/experiment process.

---

# 22. CANONICAL RECOMMENDATION ENGINE

The `RecommendationEngine` is the central architectural component.

It should coordinate:

* User lookup
* User history
* Candidate generation
* Collaborative scoring
* Content scoring
* Popularity scoring
* Score normalization
* Filtering
* Ranking
* Fallback handling
* Top-K selection

---

## 22.1 Canonical Flow

```text
Request
  ↓
Validate User
  ↓
Load User Context
  ↓
Determine User State
  │
  ├── Unknown
  │      ↓
  │   Fallback
  │
  ├── Sparse
  │      ↓
  │   Limited Personalization
  │
  └── Established
         ↓
      Personalized Pipeline
         ↓
Candidate Generation
  ↓
Candidate Filtering
  ↓
Model Scoring
  ↓
Score Normalization
  ↓
Hybrid Ranking
  ↓
Top-K
  ↓
Recommendation Response
```

---

# 23. USER STATE CLASSIFICATION

The Recommendation Engine should classify users into operational states.

Possible states:

```text
UNKNOWN
SPARSE_HISTORY
ESTABLISHED
```

These are operational states, not necessarily the same as analytical user segments.

---

## 23.1 UNKNOWN

No valid interaction history exists.

Use:

```text
Popularity / Approved fallback
```

---

## 23.2 SPARSE_HISTORY

Some history exists, but insufficient evidence exists for robust collaborative personalization.

Use:

```text
Content + limited personalization + popularity
```

as supported by the final methodology.

---

## 23.3 ESTABLISHED

Sufficient interaction history exists.

Use:

```text
Personalized model
+
Content
+
Popularity
```

where supported.

---

# 24. RECOMMENDATION RESPONSE ARCHITECTURE

The Recommendation Engine should return a structured internal result.

Conceptual structure:

```text
RecommendationResult
│
├── user_id
├── requested_k
├── recommendations
│   ├── item_id
│   ├── rank
│   ├── score
│   └── optional metadata
│
├── strategy_used
├── fallback_used
└── metadata
```

The exact schema will be finalized in:

`APPLICATION_SPECIFICATIONS.md`

---

# 25. EVALUATION ARCHITECTURE

Evaluation must consume the canonical recommendation pipeline.

The desired architecture is:

```text
Evaluation Dataset
      ↓
Eligible Users
      ↓
For Each User
      ↓
Canonical RecommendationEngine
      ↓
Top-K Recommendations
      ↓
Compare Against Held-Out Relevant Items
      ↓
Precision@K
Recall@K
NDCG@K
      ↓
Aggregate Metrics
      ↓
Model / Segment Analysis
```

---

# 26. EVALUATION MODEL ISOLATION

Evaluation must support controlled comparison.

Conceptually:

```text
Training Data
     │
     ├── Popularity Model
     ├── CF Model
     ├── MF Model
     ├── Content Model
     └── Hybrid Engine
              │
              ▼
       Common Evaluation
              │
              ▼
       Common Metrics
```

This prevents differences in evaluation methodology from contaminating model comparisons.

---

# 27. TEMPORAL EVALUATION ARCHITECTURE

Where legitimate timestamps exist:

```text
All Interactions
       ↓
Sort by Timestamp
       ↓
Temporal Cutoff
       ├───────────────┐
       ↓               ↓
Training Period    Validation Period
       │               │
       ↓               ↓
Model Training     Ground Truth
       │               │
       └───────┬───────┘
               ↓
        Recommendation
               ↓
       Ranking Metrics
```

---

# 28. EVALUATION LEAKAGE BOUNDARY

The following boundary must be maintained:

```text
             TRAINING WORLD
┌────────────────────────────────────┐
│ Training interactions              │
│ Training popularity                │
│ Training collaborative model       │
│ Training content representation    │
└──────────────────┬─────────────────┘
                   │
                   │ NO FUTURE DATA
                   ▼
             EVALUATION WORLD
┌────────────────────────────────────┐
│ Held-out interactions              │
│ Ground-truth relevance             │
│ Final metric calculation           │
└────────────────────────────────────┘
```

No evaluation-period information should cross into the training boundary.

---

# 29. SEGMENT ANALYSIS ARCHITECTURE

User segmentation is separate from recommendation generation but connected to evaluation.

```text
User Interaction History
        ↓
Feature Extraction
        ↓
User Segmentation
        ↓
Segment Assignment
        ↓
Evaluation Results
        ↓
Group By Segment
        ↓
Precision@K
Recall@K
NDCG@K
```

---

# 30. SEGMENTATION VS USER STATE

The architecture must distinguish:

### Operational User State

Used by RecommendationEngine.

```text
UNKNOWN
SPARSE
ESTABLISHED
```

### Analytical User Segment

Used for evaluation and analysis.

Example:

```text
Low Activity
Medium Activity
High Activity
```

These concepts must not be conflated.

A user may be:

```text
Operational State:
ESTABLISHED

Analytical Segment:
High Activity
```

---

# 31. API ARCHITECTURE

FastAPI acts as the service layer.

```text
Client
  ↓
HTTP Request
  ↓
FastAPI Router
  ↓
Request Validation
  ↓
Recommendation Service
  ↓
RecommendationEngine
  ↓
Recommendation Result
  ↓
Response Serialization
  ↓
JSON Response
```

---

# 32. API COMPONENTS

The API architecture should conceptually contain:

```text
api/
├── recommendation_api.py
└── ...
```

The existing API file should be preserved where practical.

Responsibilities should include:

* Route definitions
* Input validation
* Calling service/recommendation layer
* Response formatting
* Error handling

The API should not contain model-training logic.

---

# 33. API DEPENDENCY RULE

The API must depend on the Recommendation Layer.

It must not depend directly on:

* Raw CSV manipulation
* Model-training scripts
* Evaluation scripts

for normal recommendation requests.

Desired dependency:

```text
FastAPI
   ↓
Recommendation Service / Engine
   ↓
Loaded Model Artifacts
```

Not:

```text
FastAPI
   ↓
Train Model
   ↓
Read Raw Dataset
   ↓
Calculate Recommendations
```

on every request.

---

# 34. API HEALTH ARCHITECTURE

The health endpoint should provide a lightweight service status check.

Conceptually:

```text
GET /health
      ↓
Service Running?
      ↓
Model/Dependency State
      ↓
JSON Status
```

It should not perform expensive model training.

---

# 35. STREAMLIT ARCHITECTURE

Streamlit serves as the user-facing demonstration layer.

```text
Browser
   ↓
Streamlit UI
   ↓
Input Controls
   ↓
Recommendation Service / Engine
   ↓
Recommendation Result
   ↓
UI Rendering
```

---

# 36. STREAMLIT RESPONSIBILITIES

Streamlit should be responsible for:

* User input
* Recommendation count
* Displaying recommendations
* Displaying analytics
* Displaying segment information
* Showing model/evaluation information where appropriate
* User-friendly error messages

It should not contain a second recommendation engine.

---

# 37. STREAMLIT DATA FLOW

```text
User
 ↓
Select User
 ↓
Select K
 ↓
Request Recommendation
 ↓
Canonical RecommendationEngine
 ↓
Recommendation Result
 ↓
Display Ranked Items
```

---

# 38. APPLICATION CONSISTENCY

API and Streamlit must produce consistent recommendation behavior for the same:

* User
* Model state
* Configuration
* K

subject to expected presentation differences.

This means:

```text
Same User
   +
Same Model State
   +
Same Configuration
   +
Same K
   ↓
Same Recommendation Logic
```

---

# 39. CONFIGURATION ARCHITECTURE

Configuration should be centralized.

Conceptual structure:

```text
config/
└── config.py
```

Potential configuration categories:

```text
Data paths
Model parameters
Recommendation weights
K defaults
Evaluation parameters
Random seeds
Application settings
```

---

# 40. CONFIGURATION RULES

Configuration must:

* Avoid unnecessary duplication.
* Avoid unexplained hardcoded values.
* Be easy to inspect.
* Be reproducible.
* Be separated from business logic where practical.

---

# 41. MODEL ARTIFACT ARCHITECTURE

Trained models and derived artifacts should be separated from source code.

Conceptually:

```text
models/
└── artifacts/
    ├── popularity/
    ├── collaborative/
    ├── matrix_factorization/
    └── content/
```

The exact artifact structure shall be determined by implementation.

Generated model artifacts should not be confused with source code.

---

# 42. MODEL LIFECYCLE

```text
Data
 ↓
Preprocessing
 ↓
Training
 ↓
Validation
 ↓
Evaluation
 ↓
Approved Model
 ↓
Persisted Artifact
 ↓
RecommendationEngine
 ↓
API / Streamlit
```

A model should not be served merely because training completed.

It should pass the required validation/evaluation gates.

---

# 43. TRAINING VS INFERENCE

The architecture must distinguish:

## Training

```text
Data
 ↓
Preprocessing
 ↓
Model Training
 ↓
Model Artifact
```

## Inference

```text
User Request
 ↓
Loaded Model
 ↓
Recommendation
```

Inference should not unnecessarily retrain the model.

---

# 44. OFFLINE TRAINING ARCHITECTURE

A conceptual offline training workflow:

```text
Raw Data
   ↓
Validation
   ↓
Preprocessing
   ↓
Training Split
   ↓
Model Training
   ↓
Model Validation
   ↓
Artifact Persistence
```

---

# 45. OFFLINE EVALUATION ARCHITECTURE

```text
Trained Model
      +
Held-Out Data
      ↓
Evaluation Runner
      ↓
Recommendations
      ↓
Ranking Metrics
      ↓
Reports
```

---

# 46. ONLINE / SERVING ARCHITECTURE

The project does not require a production-scale online infrastructure.

The intended serving architecture is:

```text
FastAPI / Streamlit
        ↓
Loaded Recommendation Components
        ↓
Canonical RecommendationEngine
        ↓
Ranked Recommendations
```

---

# 47. REPOSITORY ARCHITECTURE

The repository should maintain a structure conceptually similar to:

```text
personalized_product_recommendation/
│
├── app/
│   └── streamlit_app.py
│
├── api/
│   └── recommendation_api.py
│
├── config/
│   └── config.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── api.md
│   ├── methodology.md
│   └── project_architecture.md
│
├── models/
│   └── ...
│
├── outputs/
│   └── reports/
│
├── src/
│   ├── data/
│   ├── evaluation/
│   ├── models/
│   ├── recommendation/
│   └── utils/
│
├── tests/
│
├── PRD.md
├── PROJECT_SPECIFICATIONS.md
├── DATASET_AND_DATA_STRATEGY.md
├── ML_METHODOLOGY.md
├── EXPERIMENT_PLAN.md
├── EVALUATION_AND_ERROR_ANALYSIS.md
├── SYSTEM_ARCHITECTURE.md
├── TASK_TRACKER.md
├── RULES.md
├── DOCUMENTATION_AND_REPORTING.md
└── README.md
```

This is a target conceptual structure.

Existing files must not be deleted or moved merely to make the tree look cleaner.

Any structural change must be justified and controlled.

---

# 48. SOURCE CODE ORGANIZATION

The `src/` layer should remain responsible for reusable ML/system logic.

Conceptual organization:

```text
src/
│
├── data/
│   ├── data_preparation.py
│   └── eda.py
│
├── models/
│   ├── popularity_model.py
│   ├── collaborative_filter.py
│   └── matrix_factorization.py
│
├── recommendation/
│   └── recommendation_engine.py
│
├── evaluation/
│   └── evaluate_recommendations.py
│
└── utils/
    └── data_utils.py
```

Actual existing filenames should be preserved unless modification is required.

---

# 49. DATA SCRIPT RESPONSIBILITIES

Data scripts should perform:

* Acquisition
* Cleaning
* Transformation
* Validation
* Processing
* EDA

They should not implement recommendation-serving behavior.

---

# 50. MODEL SCRIPT RESPONSIBILITIES

Model modules should contain:

* Model classes/functions
* Training logic
* Prediction/scoring logic
* Model configuration handling

They should not contain Streamlit-specific UI code.

---

# 51. RECOMMENDATION MODULE RESPONSIBILITIES

The recommendation module should coordinate model outputs.

It should not duplicate data acquisition logic.

---

# 52. EVALUATION MODULE RESPONSIBILITIES

The evaluation module should:

* Generate recommendations using approved models
* Compare against held-out relevance
* Calculate metrics
* Aggregate results
* Produce evaluation artifacts

It should not contain an unrelated ad-hoc recommendation algorithm.

---

# 53. TEST ARCHITECTURE

Testing should exist at multiple levels.

```text
                  Tests
                    │
        ┌───────────┼────────────┐
        │           │            │
        ▼           ▼            ▼
      Unit     Integration      API
        │           │            │
        └───────────┼────────────┘
                    ▼
              End-to-End
```

---

# 54. UNIT TEST LAYER

Unit tests should validate isolated components.

Examples:

* Data validation
* Popularity calculation
* Collaborative filtering
* Matrix factorization utilities
* Content similarity
* Precision@K
* Recall@K
* NDCG@K
* Candidate filtering
* Score normalization

---

# 55. INTEGRATION TEST LAYER

Integration tests should validate:

```text
Data
 ↓
Model
 ↓
RecommendationEngine
```

and:

```text
RecommendationEngine
 ↓
API
```

---

# 56. END-TO-END TEST LAYER

The end-to-end test should verify the primary user journey:

```text
Data Available
    ↓
Models Available
    ↓
Engine Initialized
    ↓
User Request
    ↓
Recommendations Generated
    ↓
Valid Output Returned
```

---

# 57. ERROR HANDLING ARCHITECTURE

Errors should be handled at the appropriate layer.

```text
Data Error
    ↓
Data Layer

Model Error
    ↓
Model Layer

Recommendation Error
    ↓
Recommendation Layer

HTTP Error
    ↓
API Layer

UI Error
    ↓
Streamlit Layer
```

Errors should not be silently swallowed.

---

# 58. FAILURE MODES

The architecture should account for:

### Missing Data

```text
Missing Data
 ↓
Validation Failure
 ↓
Clear Error
```

### Missing Model

```text
Model Artifact Missing
 ↓
Initialization Failure
 ↓
Clear Error
```

### Unknown User

```text
Unknown User
 ↓
Fallback Strategy
```

### Invalid K

```text
Invalid K
 ↓
Validation Error
```

### No Candidates

```text
No Candidates
 ↓
Fallback
 ↓
If still unavailable → Controlled Empty/Error State
```

---

# 59. LOGGING ARCHITECTURE

The application should provide useful logging for:

* Startup
* Data loading
* Model loading
* Recommendation failures
* API errors
* Evaluation execution

Logs must not expose secrets.

---

# 60. OBSERVABILITY

For the scale of this project, observability can remain lightweight.

The system should make it possible to determine:

* Whether data loaded successfully.
* Whether models loaded successfully.
* Which recommendation strategy was used.
* Whether fallback was triggered.
* Whether an API request failed.
* Whether evaluation completed.

---

# 61. ARTIFACT FLOW

The project should conceptually produce:

```text
Raw Dataset
    ↓
Processed Dataset
    ↓
Model Artifacts
    ↓
Evaluation Results
    ↓
Reports
    ↓
Application
```

---

# 62. REPORT ARCHITECTURE

Evaluation/report artifacts should distinguish:

### Raw Evidence

Actual experiment output.

### Derived Analysis

Interpretation of actual output.

### Documentation

Human-readable explanation.

The final report must not replace actual experiment results with manually written numbers.

---

# 63. REPRODUCIBILITY ARCHITECTURE

A clean environment should conceptually support:

```text
Clone Repository
       ↓
Install Dependencies
       ↓
Acquire Dataset
       ↓
Run Data Preparation
       ↓
Train Models
       ↓
Run Evaluation
       ↓
Launch API / Streamlit
```

The exact commands will be documented in `README.md`.

---

# 64. RANDOMNESS CONTROL

Where models use randomness:

```text
Configuration
     ↓
Random Seed
     ↓
Training
     ↓
Reproducible Artifact
```

Random seeds must be explicitly controlled where the underlying algorithm supports it.

---

# 65. DEPENDENCY ARCHITECTURE

Dependencies should be minimal and justified.

Core stack:

```text
Python
├── pandas
├── numpy
├── scipy
├── scikit-learn
├── fastapi
└── streamlit
```

Additional dependencies may be retained only when required by existing functionality or approved architecture.

---

# 66. NO UNNECESSARY FRONTEND ARCHITECTURE

The final architecture explicitly excludes:

```text
React
TypeScript
Vite
Tailwind CSS
Next.js
```

The project is not a frontend engineering project.

Streamlit is sufficient for the intended application demonstration.

---

# 67. DEPENDENCY DIRECTION

The architecture should follow this dependency direction:

```text
                 Configuration
                       │
                       ▼
Data ───────────────► Models
  │                     │
  │                     ▼
  └──────────────► Recommendation
                       │
                ┌──────┴──────┐
                ▼             ▼
             API          Streamlit
                │             │
                └──────┬──────┘
                       ▼
                    User
```

Evaluation may depend on models/recommendation components but should remain independent of the UI.

---

# 68. FORBIDDEN DEPENDENCY PATTERNS

Avoid:

```text
Streamlit
   ↓
Custom Recommendation Algorithm
```

when the canonical engine already exists.

Avoid:

```text
API
   ↓
Evaluation Script
```

for normal inference.

Avoid:

```text
RecommendationEngine
   ↓
Streamlit-specific code
```

The core recommendation layer must remain application-agnostic.

---

# 69. RECOMMENDATION REQUEST LIFECYCLE

A complete request should follow:

```text
1. Request received
        ↓
2. Validate user ID
        ↓
3. Validate K
        ↓
4. Resolve user state
        ↓
5. Retrieve user history
        ↓
6. Generate candidates
        ↓
7. Filter candidates
        ↓
8. Generate model scores
        ↓
9. Normalize scores
        ↓
10. Apply hybrid ranking
        ↓
11. Apply fallback if required
        ↓
12. Remove duplicates
        ↓
13. Select Top-K
        ↓
14. Format result
        ↓
15. Return response
```

---

# 70. MODEL INITIALIZATION LIFECYCLE

The model lifecycle should be:

```text
Application Startup
       ↓
Load Configuration
       ↓
Load Data / Artifacts
       ↓
Initialize Models
       ↓
Initialize RecommendationEngine
       ↓
Validate Dependencies
       ↓
Ready
```

If a critical dependency is unavailable:

```text
Initialization Failure
       ↓
Do Not Pretend Service Is Ready
       ↓
Clear Error / Health State
```

---

# 71. RECOMMENDATION ENGINE INITIALIZATION

The engine should receive the required components through a controlled initialization process.

Conceptually:

```text
RecommendationEngine(
    popularity_model,
    collaborative_model,
    content_model,
    matrix_factorization_model,
    configuration,
    metadata
)
```

The exact constructor/interface is implementation-dependent.

---

# 72. MODEL ARTIFACT CONSISTENCY

A RecommendationEngine must not combine incompatible artifacts.

For example:

```text
Training Dataset Version A
        +
Model trained on Version B
        +
Product metadata from Version C
```

should not silently be accepted.

Artifact/data compatibility should be documented.

---

# 73. DATASET VERSIONING

Where practical, identify:

* Dataset version
* Acquisition date
* Source URL/reference
* Row count
* Column count
* File checksum or equivalent fingerprint

This supports reproducibility.

---

# 74. MODEL VERSIONING

Model artifacts should be traceable to:

* Dataset version
* Configuration
* Training procedure
* Model type
* Experiment identifier

---

# 75. EXPERIMENT-TO-ARCHITECTURE TRACEABILITY

Every final model should have a traceable path:

```text
Experiment ID
      ↓
Configuration
      ↓
Dataset Version
      ↓
Model
      ↓
Evaluation
      ↓
Result
      ↓
RecommendationEngine Configuration
```

---

# 76. EVALUATION-TO-PRODUCTION CONSISTENCY

The architecture must prevent the following:

```text
Evaluation:
Model A

Production:
Model B

Documentation:
Claims Model A results
```

The final deployed/served recommendation configuration must be identifiable.

---

# 77. MODEL REGISTRY CONCEPT

A formal MLflow-style model registry is not required.

A lightweight artifact registry can be used.

Conceptually:

```text
models/
├── popularity/
├── collaborative/
├── matrix_factorization/
└── content/
```

with metadata documenting:

* Model version
* Dataset
* Configuration
* Experiment
* Evaluation result

---

# 78. DATA PIPELINE TO APPLICATION BOUNDARY

The application must consume processed/model artifacts rather than performing the entire data preparation pipeline during every request.

Desired:

```text
Offline:
Data → Models → Artifacts

Online:
Request → Artifacts → Recommendation
```

---

# 79. OFFLINE / ONLINE SEPARATION

## Offline

* Data processing
* Model training
* Evaluation
* Report generation

## Online / Interactive

* Recommendation request
* API response
* Streamlit interaction

This separation improves runtime efficiency and reproducibility.

---

# 80. ARCHITECTURAL PRESERVATION MATRIX

| Existing Component     | Target Action                 | Reason                          |
| ---------------------- | ----------------------------- | ------------------------------- |
| `RecommendationEngine` | Preserve + repair             | Canonical recommendation layer  |
| FastAPI                | Preserve + integrate          | Required service layer          |
| Streamlit              | Preserve + integrate          | Demonstration/application layer |
| Popularity model       | Preserve + validate           | Baseline + fallback             |
| CF model               | Preserve + validate           | Personalized model              |
| TF-IDF model           | Preserve + repair             | Content/cold-start capability   |
| Matrix factorization   | Evaluate + integrate if valid | Candidate personalized model    |
| Metric functions       | Preserve + test               | Required metrics                |
| `data_utils.py`        | Preserve                      | Reusable data utilities         |
| Existing tests         | Preserve + expand             | Regression protection           |
| Existing configuration | Preserve + repair             | Centralized settings            |

---

# 81. ARCHITECTURAL MODIFICATION POLICY

Before modifying an existing component:

1. Inspect it.
2. Determine its current behavior.
3. Identify the specific defect.
4. Determine whether the defect affects requirements.
5. Modify only what is necessary.
6. Run relevant tests.
7. Verify downstream behavior.

---

# 82. ARCHITECTURAL DELETION POLICY

No existing file should be deleted merely because:

* It appears unused.
* Another module appears newer.
* Google AI Studio suggests a different structure.
* A framework generated replacement files.
* The file appears redundant.

Deletion requires:

1. Identification.
2. Dependency check.
3. Confirmation that it is not required.
4. Documentation of the decision.
5. Controlled removal.

---

# 83. GOOGLE AI STUDIO IMPLEMENTATION CONSTRAINT

Google AI Studio may be used as the implementation assistant.

However, the architecture remains repository-controlled.

AI-assisted implementation must not:

* Replace the approved stack.
* Delete files without authorization.
* Introduce React/Vite/TypeScript/Tailwind.
* Create duplicate application architectures.
* Replace valid existing components unnecessarily.
* Modify unrelated files.

---

# 84. ARCHITECTURE CHANGE CONTROL

Any major architecture change must answer:

1. What requirement does this solve?
2. Why is the existing architecture insufficient?
3. What files/components are affected?
4. What dependencies change?
5. What tests must change?
6. Does it affect reproducibility?
7. Does it affect evaluation?
8. Does it affect the API/UI?
9. Does it introduce unnecessary complexity?

---

# 85. FINAL TARGET ARCHITECTURE

The final target architecture is:

```text
┌──────────────────────────────────────────────────────────────┐
│                    DATA FOUNDATION                           │
│                                                              │
│  Legitimate Source → Raw → Validation → Processing           │
│                                      ↓                       │
│                              User-Item / Product Data        │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                    MODEL LAYER                               │
│                                                              │
│  Popularity │ Collaborative │ Matrix Factorization │ Content │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│               RECOMMENDATION LAYER                           │
│                                                              │
│ Candidate Generation                                         │
│        ↓                                                     │
│ Candidate Filtering                                          │
│        ↓                                                     │
│ Model Scoring                                                │
│        ↓                                                     │
│ Score Normalization                                          │
│        ↓                                                     │
│ Hybrid Ranking                                               │
│        ↓                                                     │
│ Cold-Start / Fallback                                        │
│        ↓                                                     │
│ Canonical RecommendationEngine                               │
└───────────────────────────────┬──────────────────────────────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
┌────────────────────────┐        ┌────────────────────────────┐
│      FASTAPI           │        │       STREAMLIT             │
│                        │        │                            │
│ Request Validation     │        │ User Controls              │
│ Recommendation Route   │        │ Recommendation Display     │
│ Health Route           │        │ Analytics                  │
│ Error Handling         │        │ Segment Analysis           │
└────────────┬───────────┘        └──────────────┬─────────────┘
             │                                   │
             └─────────────────┬─────────────────┘
                               ▼
                             USER
```

---

# 86. FINAL EVALUATION ARCHITECTURE

Evaluation remains connected to the recommendation system but is logically separated from serving.

```text
                 Training Data
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
     Model Training          Validation Data
          │                         │
          ▼                         ▼
   Model Artifacts            Ground Truth
          │                         │
          └────────────┬────────────┘
                       ▼
             Canonical Recommendation
                    Engine
                       │
                       ▼
              Top-K Recommendations
                       │
                       ▼
             Ranking Evaluation
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 Precision@K       Recall@K       NDCG@K
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                Segment Analysis
                       │
                       ▼
                 Error Analysis
                       │
                       ▼
                Final Evaluation
```

---

# 87. FINAL APPLICATION ARCHITECTURE

```text
                         USER
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
            Streamlit             API Client
                │                     │
                ▼                     ▼
          Application Layer      FastAPI Layer
                │                     │
                └──────────┬──────────┘
                           ▼
                Recommendation Service
                           │
                           ▼
                RecommendationEngine
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       Collaborative    Content       Popularity
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                    Hybrid Ranking
                           │
                           ▼
                       Top-K
                           │
                           ▼
                    Application
```

---

# 88. FINAL DATA-TO-RECOMMENDATION FLOW

```text
SOURCE
  ↓
Acquire
  ↓
Validate
  ↓
Clean
  ↓
Transform
  ↓
Represent Interactions
  ↓
Train Models
  ↓
Persist Artifacts
  ↓
Initialize RecommendationEngine
  ↓
Receive User Request
  ↓
Determine User State
  ↓
Generate Candidates
  ↓
Filter Candidates
  ↓
Score Candidates
  ↓
Normalize Scores
  ↓
Combine Signals
  ↓
Apply Fallback if Required
  ↓
Rank
  ↓
Top-K
  ↓
Return Recommendation
```

---

# 89. FINAL ARCHITECTURAL QUALITY GATES

Before architecture is considered complete:

## Gate A — Data

* [ ] Legitimate source
* [ ] Valid schema
* [ ] Reproducible processing
* [ ] No fabricated behavior
* [ ] Timestamp strategy resolved honestly

## Gate B — Models

* [ ] Popularity model
* [ ] Collaborative model
* [ ] Content model
* [ ] Matrix factorization evaluated
* [ ] Model artifacts reproducible

## Gate C — Recommendation

* [ ] One canonical engine
* [ ] Candidate generation separated
* [ ] Filtering separated
* [ ] Ranking separated
* [ ] Cold-start handled
* [ ] Fallback handled

## Gate D — Evaluation

* [ ] Actual engine evaluated
* [ ] Precision@K
* [ ] Recall@K
* [ ] NDCG@K
* [ ] Leakage prevented
* [ ] Temporal methodology valid/documented

## Gate E — Applications

* [ ] FastAPI integrated
* [ ] Streamlit integrated
* [ ] No duplicate recommendation logic

## Gate F — QA

* [ ] Unit tests
* [ ] Integration tests
* [ ] API tests
* [ ] End-to-end tests

## Gate G — Documentation

* [ ] Architecture documented
* [ ] Methodology synchronized
* [ ] Evaluation synchronized
* [ ] README synchronized

---

# 90. ARCHITECTURAL ANTI-PATTERNS

The following patterns are prohibited.

## Anti-Pattern 1 — Multiple Recommendation Engines

```text
API → Engine A
Streamlit → Engine B
Evaluation → Engine C
```

### Correct

```text
API
  \
Streamlit → Canonical RecommendationEngine
  /
Evaluation
```

---

## Anti-Pattern 2 — Training During Every API Request

```text
Request
 ↓
Load Raw Data
 ↓
Train Model
 ↓
Recommend
```

### Correct

```text
Offline Training
 ↓
Model Artifact
 ↓
API
 ↓
Recommend
```

---

## Anti-Pattern 3 — Evaluation Heuristic Disconnected From Production

```text
Evaluation → Toy Heuristic

Production → RecommendationEngine
```

### Correct

```text
Evaluation → RecommendationEngine
Production  → RecommendationEngine
```

---

## Anti-Pattern 4 — Cold-Start Blocked by Candidate Pool

```text
All Products
 ↓
Top Popular Products Only
 ↓
Content Model
```

This prevents non-popular new products from being considered.

### Correct

```text
Product Universe
 ↓
Eligible Candidates
 ├── Popular
 ├── Personalized
 └── Metadata-Based
 ↓
Ranking
```

---

## Anti-Pattern 5 — Fake Temporal Validation

```text
No Timestamp
 ↓
Invent Timestamp
 ↓
Temporal Split
 ↓
Claim Time-Based Validation
```

This is prohibited.

---

# 91. ARCHITECTURAL DECISION RECORDS

Important architectural decisions should be documented when necessary.

Examples:

```text
ADR-001 — Preserve RecommendationEngine
ADR-002 — Preserve FastAPI
ADR-003 — Preserve Streamlit
ADR-004 — Centralize Recommendation Logic
ADR-005 — Do Not Fabricate Behavioral Events
ADR-006 — Do Not Fabricate Timestamps
ADR-007 — Separate Evaluation From UI
ADR-008 — Preserve Python-Based Stack
```

Formal ADR files are optional unless the project requires them.

---

# 92. ARCHITECTURAL DECISION: PRESERVE RECOMMENDATION ENGINE

### Decision

Preserve the existing `RecommendationEngine` as the foundation of the canonical recommendation layer.

### Reason

The repository already contains a hybrid recommendation implementation that combines multiple recommendation signals.

### Required Action

Repair and integrate it rather than creating an unrelated replacement.

---

# 93. ARCHITECTURAL DECISION: PRESERVE FASTAPI

### Decision

Preserve the existing FastAPI architecture.

### Reason

The official project requires a simple recommendation API and the existing structure already provides a suitable foundation.

### Required Action

Connect it to the canonical RecommendationEngine.

---

# 94. ARCHITECTURAL DECISION: PRESERVE STREAMLIT

### Decision

Preserve the existing Streamlit structure.

### Reason

The existing application provides a useful demonstration interface.

### Required Action

Remove/replace duplicate recommendation logic where necessary and connect the UI to the canonical engine.

---

# 95. ARCHITECTURAL DECISION: NO UNNECESSARY FRONTEND

### Decision

Do not introduce:

* React
* Vite
* TypeScript
* Tailwind CSS

### Reason

They are unnecessary for the approved Python/Streamlit architecture and would increase complexity without satisfying a required project objective.

---

# 96. ARCHITECTURAL DECISION: NO FABRICATED TEMPORAL DATA

### Decision

Do not invent timestamps.

### Reason

Temporal validation must represent genuine chronology.

### Required Action

Investigate legitimate timestamp-bearing source/version availability before deciding the final temporal evaluation strategy.

---

# 97. ARCHITECTURAL DECISION: NO FABRICATED EVENT TYPES

### Decision

Do not invent views/clicks/carts/purchases and present them as source data.

### Reason

The audited dataset does not establish these genuine behavioral events.

### Required Action

Use only legitimate source fields and clearly documented derived representations.

---

# 98. ARCHITECTURAL DECISION: ONE SOURCE OF TRUTH

The RecommendationEngine shall be the source of truth for recommendation behavior.

```text
RecommendationEngine
       │
       ├── API
       ├── Streamlit
       └── Evaluation
```

This is a mandatory architectural constraint.

---

# 99. FINAL ARCHITECTURE SUMMARY

The final system architecture can be summarized as:

```text
                    DATA
                     │
                     ▼
              VALIDATION
                     │
                     ▼
             PREPROCESSING
                     │
                     ▼
          USER-ITEM REPRESENTATION
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
  POPULARITY         CF         CONTENT
       │             │             │
       │             ▼             │
       │             MF            │
       │             │             │
       └─────────────┼─────────────┘
                     ▼
             CANDIDATE GENERATION
                     │
                     ▼
             CANDIDATE FILTERING
                     │
                     ▼
                SCORING
                     │
                     ▼
             SCORE NORMALIZATION
                     │
                     ▼
             HYBRID RANKING
                     │
                     ▼
            COLD-START FALLBACK
                     │
                     ▼
         CANONICAL RECOMMENDATION
                  ENGINE
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
       FASTAPI              STREAMLIT
          │                     │
          └──────────┬──────────┘
                     ▼
                    USER


Parallel Evaluation Path:

       TRAINING DATA
             │
             ▼
          MODELS
             │
             ▼
     RECOMMENDATION ENGINE
             │
             ▼
       HELD-OUT DATA
             │
             ▼
     PRECISION@K / RECALL@K
             │
             ▼
          NDCG@K
             │
             ▼
      SEGMENT ANALYSIS
             │
             ▼
       ERROR ANALYSIS
             │
             ▼
      VERIFIED RESULTS
```

---

# 100. FINAL ARCHITECTURAL PRINCIPLE

The final Project 3 architecture must follow one central rule:

> **Build one coherent recommendation system, not several disconnected demonstrations of recommendation techniques.**

The final architecture must therefore connect:

```text
Legitimate Data
      ↓
Valid Representation
      ↓
Multiple Recommendation Signals
      ↓
Canonical RecommendationEngine
      ↓
Valid Evaluation
      ↓
Meaningful Segment Analysis
      ↓
FastAPI
      ↓
Streamlit
      ↓
Testing
      ↓
Reproducibility
      ↓
Professional Documentation
```

The architecture is considered successful when:

* Existing valid work has been preserved.
* Existing architectural inconsistencies have been removed.
* Data flows through a reproducible pipeline.
* Models operate on valid data.
* Recommendation logic exists in one canonical location.
* Cold-start behavior is genuinely supported.
* Evaluation uses actual recommendation outputs.
* Temporal validation is legitimate or its limitation is explicitly documented.
* API and Streamlit use the same recommendation engine.
* Testing verifies critical behavior.
* The complete system can be reproduced and explained.

---

**END OF SYSTEM_ARCHITECTURE.md**

```
```
