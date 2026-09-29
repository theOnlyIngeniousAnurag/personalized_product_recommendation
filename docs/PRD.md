# PRD.md

# Product Requirements Document
## Personalized Product Recommendation Model

---

## Document Control

| Field | Value |
|---|---|
| Project | Personalized Product Recommendation Model |
| Project Number | Project 3 |
| Project Type | Machine Learning Internship Capstone |
| Document | Product Requirements Document |
| Document Version | 1.0 |
| Document Status | Approved Planning Baseline |
| Primary Language | Python |
| Primary ML Ecosystem | Scikit-learn / SciPy |
| Application Layer | FastAPI + Streamlit |
| Version Control | Git / GitHub |
| Repository | `personalized_product_recommendation` |
| Source of Requirements | Official Internship Project Specification |
| Existing Implementation Source | Existing GitHub Repository |
| Current Development Mode | Audit → Repair → Integrate → Validate → Finalize |
| Primary Objective | Build a correct, reproducible, evaluated personalized product recommendation system |

---

# 1. PURPOSE OF THIS DOCUMENT

This Product Requirements Document defines the intended product, functionality, scope, quality standards, user-facing behavior, machine-learning objectives, system outcomes, constraints, and completion criteria for:

> **Personalized Product Recommendation Model**

This project is the third Machine Learning Internship Capstone Project.

The project is not being treated as a simple internship assignment.

The target is a technically defensible machine-learning recommendation system that can be:

- Submitted for internship evaluation
- Presented as a capstone project
- Published on GitHub
- Included in a resume
- Discussed on LinkedIn
- Demonstrated in a portfolio
- Explained during technical interviews
- Defended from a machine-learning and software-engineering perspective

This PRD therefore defines both:

1. The **minimum requirements derived from the official internship specification**, and
2. The **engineering and ML quality expectations required to make the project genuinely defensible**.

---

# 2. IMPORTANT DOCUMENTATION PRINCIPLE

This PRD defines the **target product requirements**.

It does NOT claim that all requirements are currently implemented.

The current repository has already been audited separately.

The audit established that the repository contains a substantial existing implementation, including:

- Recommendation Engine
- Collaborative Filtering
- Matrix Factorization prototype
- Content-Based recommendation
- Popularity recommendation
- FastAPI application
- Streamlit application
- Recommendation metrics
- User segmentation
- Testing infrastructure
- Configuration utilities

However, the audit also identified significant problems involving:

- Missing core datasets
- Dataset/requirement mismatch
- Lack of legitimate timestamps
- Non-time-based validation
- Fragmented recommendation pipelines
- Incomplete evaluation
- Cold-start candidate filtering
- Collapsed user segmentation
- Dependency defects
- Documentation inconsistencies

Therefore, throughout all Project 3 documentation, we must distinguish between:

```text
REQUIRED
    ↓
TARGET / PLANNED
    ↓
IMPLEMENTED
    ↓
VERIFIED

A feature must not be described as implemented or verified until actual repository evidence and testing establish that status.

3. PRODUCT NAME
Personalized Product Recommendation Model

Short name:

PPRM

The system is a machine-learning recommendation platform designed to generate ranked product recommendations for users based on historical interaction behavior and product information.

4. OFFICIAL PROJECT DESCRIPTION

The official internship project describes the objective as recommending products to users based on:

Past interactions
Purchases
Product similarity

The prescribed approach includes:

Preparing user-item interaction data.
Creating a popularity-based baseline.
Building collaborative filtering or matrix-factorization recommendations.
Adding item metadata for a content-based fallback.
Evaluating recommendations using:
Precision@K
Recall@K
NDCG@K
Using a time-based validation split.
Creating a simple recommendation API.
Analyzing recommendations for different user segments.

The recommended implementation ecosystem is:

Python
Git/GitHub
Streamlit and/or API layer where useful.

These requirements constitute the minimum product scope.

5. PRODUCT VISION

The project aims to transform a raw product-interaction dataset into a complete recommendation workflow:

Data Source
    ↓
Data Acquisition / Restoration
    ↓
Data Validation
    ↓
Data Preparation
    ↓
User-Item Interaction Representation
    ↓
Popularity Baseline
    ↓
Personalized Recommendation Model
    ↓
Content-Based Recommendation / Fallback
    ↓
Candidate Generation
    ↓
Ranking
    ↓
Recommendation Evaluation
    ↓
User Segment Analysis
    ↓
Recommendation API
    ↓
Streamlit Application
    ↓
Testing + QA
    ↓
Reproducible Capstone System


The final product should demonstrate that recommendation systems require more than simply training a model.

It should demonstrate the complete lifecycle:

Data → Modeling → Recommendation → Evaluation → Serving → Analysis → Validation

6. PROBLEM STATEMENT

Product catalogs can contain thousands or millions of items.

Showing the same products to every user does not account for differences in:

User interests
Previous interactions
Purchase preferences
Product similarity
Activity levels
Historical behavior

A personalized recommendation system attempts to reduce this problem by using historical user-item behavior and item information to identify products that are likely to be relevant to individual users.

The project therefore aims to construct a recommendation system that can:

Represent user-item interactions.
Establish a simple popularity baseline.
Learn personalized relationships between users and products.
Incorporate product similarity.
Handle users/products with limited historical information.
Generate ranked recommendations.
Measure recommendation quality using ranking metrics.
Analyze performance across meaningful user segments.
Serve recommendations through a practical API/application layer.
7. CORE PRODUCT OBJECTIVE

The primary objective is:

Build a reproducible and technically correct personalized product recommendation system that combines user-item behavior, collaborative recommendation, product similarity, and appropriate fallback strategies, and evaluates recommendation quality using valid ranking metrics and a legitimate temporal validation methodology.

The system must prioritize:

Correctness
    >
Requirement Compliance
    >
Evaluation Validity
    >
Reproducibility
    >
Engineering Quality
    >
Documentation
    >
Optional Enhancements
8. PRODUCT GOALS
8.1 Primary Goals

The system shall aim to:

Establish a reproducible data pipeline.
Construct a valid user-item interaction representation.
Preserve the semantics of the actual source data.
Avoid fabricated behavioral events.
Establish a popularity-based recommendation baseline.
Implement personalized recommendation using collaborative filtering and/or matrix factorization.
Implement content-based recommendation using available product metadata.
Provide appropriate cold-start/fallback behavior.
Produce ranked Top-K recommendations.
Evaluate recommendations using:
Precision@K
Recall@K
NDCG@K
Use a legitimate time-based validation strategy whenever a valid timestamp-bearing data source is available.
Analyze recommendation behavior across meaningful user segments.
Provide a working recommendation API.
Integrate the same canonical recommendation logic into the application layer.
Provide a usable Streamlit demonstration where appropriate.
Provide automated and manual QA.
Make the project reproducible.
Maintain professional GitHub documentation.
9. SECONDARY GOALS

Where supported by the available data and without introducing unnecessary complexity, the system should also:

Handle sparse user-item interactions.
Handle users with limited history.
Handle new users.
Handle products with limited interaction history.
Handle new products when sufficient product metadata exists.
Avoid recommending already-interacted products where appropriate.
Provide recommendation reasons where technically defensible.
Maintain deterministic behavior where applicable.
Keep recommendation logic modular.
Allow different recommendation models to be evaluated independently.
Provide model comparison evidence.
Provide segment-level evaluation.
Provide reproducible experiment configuration.
10. NON-GOALS

The following are explicitly outside the mandatory scope unless later justified and approved.

10.1 Unnecessary Technology Expansion

The project shall not introduce:

React
TypeScript
Vite
Tailwind CSS
Next.js
Angular
Vue
Node.js frontend architecture
Unnecessary JavaScript frameworks
Unnecessary AI frameworks

The project is already based on the intended Python ecosystem.

10.2 Unnecessary ML Complexity

The project shall not introduce:

Deep neural recommender systems
Transformers
Large Language Models
Generative AI
Reinforcement learning
Complex neural ranking architectures

unless there is a clear technical requirement and explicit approval.

10.3 Unnecessary Infrastructure

The project does not require:

Kafka
Kubernetes
Microservices
Distributed model training
Large-scale cloud infrastructure
Real-time streaming infrastructure
Complex database clusters

The project should remain appropriately scoped to the internship dataset and objectives.

11. TARGET USERS
11.1 End User

A conceptual customer/user who receives personalized product recommendations.

Example:

User
 ↓
Historical Interaction Profile
 ↓
Recommendation Engine
 ↓
Ranked Product Recommendations
11.2 API Consumer

A client or application requesting recommendations for a user.

Example:

GET /recommend/{user_id}?n=10

The exact final API contract will be defined in:

APPLICATION_SPECIFICATIONS.md

11.3 ML Engineer / Developer

Responsible for:

Data preparation
Model training
Recommendation generation
Evaluation
Experimentation
Testing
Maintenance
11.4 Internship Evaluator

A reviewer should be able to determine:

What problem is being solved.
What data is being used.
How interactions are represented.
What models were implemented.
How recommendations are generated.
How recommendations were evaluated.
Whether the evaluation methodology is valid.
What limitations remain.
11.5 Technical Interviewer

The project should provide sufficient technical depth to discuss:

Recommendation-system fundamentals
Collaborative filtering
Matrix factorization
Content-based filtering
Hybrid recommendation
Cold-start problems
Ranking metrics
Temporal validation
Data leakage
Candidate generation
User segmentation
API integration
Reproducibility
12. PRODUCT PRINCIPLES
Principle 1 — Correctness Over Complexity

A simple, correct solution is preferable to a sophisticated but invalid solution.

Principle 2 — Evidence Over Assumption

Implementation claims must be supported by actual repository evidence.

Principle 3 — No Fabricated Data

The system must never fabricate:

Views
Clicks
Carts
Purchases
Timestamps
User behavior
Product metadata

and present them as genuine source observations.

If derived features or proxy interactions are used, their derivation must be explicitly documented.

Principle 4 — No Fabricated Results

The project must never fabricate:

Precision
Recall
NDCG
RMSE
Model performance
User-segment results
Experiments
Dataset statistics
API performance
Screenshots
User studies
Principle 5 — Honest Limitations

If an official requirement cannot be satisfied because the available source data lacks a required field, the limitation must be explicitly documented.

A methodological limitation is preferable to fabricated compliance.

Principle 6 — Preserve Valid Existing Work

Existing technically valid components should be preserved and improved rather than unnecessarily rewritten.

Principle 7 — One Canonical Recommendation Engine

The final system must avoid multiple conflicting recommendation implementations.

The canonical recommendation logic should be centralized and consumed by:

API
Streamlit
Evaluation
Testing

where applicable.

Principle 8 — Evaluation Must Reflect the Actual System

The system evaluated in experiments must be the same recommendation system that is ultimately served, unless an experiment explicitly identifies a separate baseline/model.

Principle 9 — Reproducibility

Important results should be reproducible from the repository and documented environment.

13. CURRENT REPOSITORY BASELINE

The repository audit established that the existing project already contains substantial components.

These components should be preserved unless subsequent technical analysis demonstrates a concrete reason otherwise.

13.1 Components to Preserve
Recommendation Engine

src/recommendation/recommendation_engine.py

Contains:

User-based collaborative filtering
Content-based scoring
Popularity scoring
Score normalization
Weighted hybrid recommendation logic

This is the preferred foundation for the final canonical recommendation engine.

FastAPI Application

api/recommendation_api.py

Provides:

Root endpoint
Recommendation endpoint
Health endpoint
Request validation
JSON serialization
Error handling

The API architecture should be preserved.

Streamlit Application

app/streamlit_app.py

Contains a substantial UI/dashboard structure including:

User selection/input
Recommendation count
Dataset metrics
Rating analysis
User segments
Popular products
Recommendation display

The UI structure should be preserved while its recommendation logic is unified with the canonical Recommendation Engine.

Evaluation Metric Functions

src/evaluation/evaluate_recommendations.py

Contains implementations of:

Precision@K
Recall@K
NDCG@K

These functions should be preserved and independently validated.

Popularity Model

src/models/popularity_model.py

Contains the existing popularity-based recommendation formulation.

This will serve as the baseline model.

Data Utilities

src/utils/data_utils.py

Contains reusable data loading/saving/validation helpers.

These should be preserved.

Technology Stack

The following stack is explicitly retained:

Python
Scikit-learn
SciPy
FastAPI
Streamlit
Git
GitHub

No unnecessary technology migration is permitted.

14. CURRENT KNOWN PRODUCT GAPS

The repository audit identified the following major gaps.

GAP-01 — Missing Core Data

The following critical data files are currently absent:

data/raw/train.csv
data/raw/test.csv
data/processed/interactions.csv
data/processed/products.csv

The absence of these files prevents multiple project components from executing.

GAP-02 — Interaction-Type Mismatch

The official requirement references:

Views
Clicks
Carts
Purchases

The audited dataset currently contains explicit ratings and related fields instead.

The current repository therefore does not contain genuine event-type information corresponding to all four interaction types.

The final system must not fabricate those events.

A legitimate data strategy must be established before implementation.

GAP-03 — Missing Legitimate Timestamp

The audited source dataset does not contain a timestamp field.

Therefore the existing random split cannot satisfy the official temporal-validation requirement.

The project must investigate whether a legitimate timestamp-bearing source/version corresponding to the dataset can be obtained.

Artificial timestamps must not be introduced and presented as real temporal observations.

GAP-04 — Fragmented Recommendation Architecture

The existing implementation contains different recommendation pipelines:

Recommendation Engine
50% Collaborative
30% Content
20% Popularity
Streamlit
70% Content
30% Popularity
Evaluation

Uses a separate heuristic rather than the canonical engine.

The final product must establish a single canonical recommendation pipeline.

GAP-05 — Cold-Start Candidate Restriction

The existing Recommendation Engine restricts candidates to a popularity-derived pool.

This prevents genuinely new products outside the popularity pool from being surfaced through the content-based mechanism.

The final system must correct this behavior.

GAP-06 — Evaluation Not Trustworthy

The current evaluation has multiple problems:

Random rather than temporal split.
Evaluates an ad-hoc heuristic.
Does not evaluate the canonical engine.
Report contains placeholder metrics.
User evaluation is truncated.
Potential information leakage exists in TF-IDF fitting.

These issues must be resolved before final performance claims are made.

GAP-07 — User Segment Collapse

Current thresholds produce approximately:

High Activity    1999
Medium Activity     1
Low Activity        0

This does not provide meaningful segment analysis.

The final segmentation strategy must be data-driven and should support recommendation-quality analysis.

GAP-08 — Testing Infrastructure

Existing tests cannot currently execute because of:

Missing pytest installation/dependency declaration
Missing required data files

The final project must restore and expand testing.

15. TARGET PRODUCT ARCHITECTURE

The target product should conceptually follow:

                    ┌─────────────────────────┐
                    │      Data Source        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Data Acquisition /      │
                    │ Restoration             │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Data Validation &       │
                    │ Preprocessing           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ User-Item Interaction   │
                    │ Representation          │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
      Popularity           Collaborative       Content-Based
       Baseline              Filtering            Model
             │                   │                   │
             │                   ▼                   │
             │             Matrix Factorization     │
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Canonical              │
                    │ Recommendation Engine  │
                    └────────────┬────────────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
                     ▼                       ▼
              Recommendation          Evaluation
                  API                      │
                     │                     ▼
                     │              Precision@K
                     │              Recall@K
                     │              NDCG@K
                     │                     │
                     │                     ▼
                     │              Segment Analysis
                     │
                     ▼
                Streamlit
                Application

This architecture is conceptual.

The final implementation architecture will be defined in:

SYSTEM_ARCHITECTURE.md

16. RECOMMENDATION MODEL STRATEGY

The final product should contain multiple recommendation approaches for meaningful comparison.

16.1 Model A — Popularity Baseline

Purpose:

Provide a simple non-personalized reference point.

Possible inputs include:

Interaction count
Rating
Other valid popularity signals

The exact formulation will be defined after data strategy review.

16.2 Model B — Collaborative Filtering

Purpose:

Capture relationships between users and products through historical interaction patterns.

The existing user-based k-NN implementation should be evaluated and improved where appropriate.

16.3 Model C — Matrix Factorization

The repository contains a TruncatedSVD implementation.

Its mathematical and practical suitability must be evaluated carefully before being promoted to a final model.

The current implementation must not automatically be treated as production-ready.

If retained, it must be:

Correctly integrated
Properly evaluated
Tested
Compared against alternatives
Documented
16.4 Model D — Content-Based Recommendation

The existing implementation uses product-name text and TF-IDF/cosine similarity.

This should be retained where appropriate but evaluated for:

Metadata sufficiency
Candidate generation
Cold-start capability
Leakage
Relevance
16.5 Model E — Hybrid Recommendation

The final system may combine multiple recommendation signals.

The exact weighting strategy must be experimentally justified.

Weights must not be presented as optimal without evidence.

17. COLD-START STRATEGY

The system must explicitly distinguish between:

New User

No or insufficient historical interaction data.

Possible fallback:

New User
   ↓
Popularity / contextual fallback
Existing User With Sparse History

Possible strategy:

Limited History
   ↓
Content + Popularity
   ↓
Collaborative when sufficient data exists
New Product

If product metadata exists:

New Product
   ↓
Metadata Representation
   ↓
Content Similarity
   ↓
Candidate Generation

The system must ensure that candidate filtering does not remove new products before the content model can evaluate them.

18. DATA INTEGRITY REQUIREMENT

The product must preserve the meaning of the source data.

If the source contains:

rating
votes
helpful_votes

the system must not document these as:

purchase
click
cart
view

unless an external authoritative source provides genuine event information.

Derived interaction representations must be clearly labeled as derived.

19. TEMPORAL VALIDATION REQUIREMENT

The official requirement specifies time-based validation.

The final project must therefore investigate:

The provenance of the current dataset.
Whether an original or corresponding timestamp-bearing dataset/version exists.
Whether timestamps can legitimately be restored from the authoritative source.
Whether the timestamp semantics are appropriate for chronological validation.
Whether the restored source is compatible with the project dataset.
Whether the resulting temporal split avoids leakage.

The project must not:

Invent timestamps.
Randomly assign timestamps.
Shuffle timestamps.
Present synthetic chronology as real user chronology.

If a legitimate timestamp-bearing source cannot be obtained, the limitation must be explicitly documented and discussed rather than hidden.

20. EVALUATION PRODUCT REQUIREMENT

The final recommendation system must be evaluated using ranking metrics.

Required metrics:

Precision@K
Recall@K
NDCG@K

Evaluation must:

Use a valid validation strategy.
Avoid data leakage.
Evaluate actual recommendation models.
Define relevance explicitly.
Define candidate sets.
Define K.
Aggregate results appropriately.
Report results reproducibly.

The final evaluation should include, where supported:

Popularity
Collaborative Filtering
Matrix Factorization
Content-Based
Hybrid

The exact model comparison set will depend on final implementation.

21. USER SEGMENTATION PRODUCT REQUIREMENT

The final system must analyze recommendation behavior across meaningful user segments.

Segmentation should be based on the actual data distribution.

Possible dimensions may include:

Interaction frequency
Purchase/engagement behavior where genuinely available
User history length
Other defensible behavioral attributes

The system must not force arbitrary thresholds that result in meaningless segments.

The final analysis should ideally report:

Segment
    ↓
Number of Users
    ↓
Recommendation Metrics
    ↓
Precision@K
    ↓
Recall@K
    ↓
NDCG@K

This will allow analysis of whether recommendation quality changes across user populations.

22. API PRODUCT REQUIREMENTS

The final API should provide a simple way to request recommendations.

At minimum:

GET /recommend/{user_id}?n=10

Expected behavior:

Validate user ID.
Validate recommendation count.
Load/use the canonical recommendation engine.
Generate recommendations.
Return ranked products.
Handle unknown users.
Handle invalid requests.
Return valid JSON.
Provide meaningful HTTP errors.

The existing FastAPI structure should be preserved.

23. STREAMLIT PRODUCT REQUIREMENTS

The Streamlit application should serve as the demonstration layer.

The existing UI structure should be preserved where practical.

The final application should allow:

User selection/input
Recommendation count selection
Recommendation generation
Recommendation display
Basic analytics
Segment analysis
Popular product analysis

Most importantly:

Streamlit must use the same canonical recommendation logic as the API.

It must not maintain a second independent recommendation algorithm.

24. FUNCTIONAL REQUIREMENTS
FR-001 — Data Acquisition

The system shall provide a reproducible mechanism for obtaining/restoring the required dataset.

FR-002 — Data Validation

The system shall validate dataset structure and quality before downstream modeling.

FR-003 — User-Item Construction

The system shall construct a valid user-item interaction representation from the available source data.

FR-004 — Baseline Recommendation

The system shall provide a popularity-based baseline.

FR-005 — Personalized Recommendation

The system shall provide collaborative filtering and/or matrix-factorization recommendation.

FR-006 — Content Recommendation

The system shall use available product metadata for content-based recommendation where appropriate.

FR-007 — Cold-Start Handling

The system shall provide defensible fallback behavior for users/products with insufficient interaction history.

FR-008 — Candidate Generation

The system shall generate recommendation candidates without incorrectly excluding valid cold-start candidates.

FR-009 — Ranking

The system shall rank candidates and return Top-K recommendations.

FR-010 — Recommendation API

The system shall expose recommendation functionality through FastAPI.

FR-011 — Streamlit Application

The system shall provide a Streamlit demonstration where appropriate.

FR-012 — Precision@K

The system shall calculate Precision@K.

FR-013 — Recall@K

The system shall calculate Recall@K.

FR-014 — NDCG@K

The system shall calculate NDCG@K.

FR-015 — Temporal Validation

The system shall use a legitimate time-based validation methodology when a valid timestamp-bearing source is available.

FR-016 — User Segment Analysis

The system shall analyze recommendation performance across meaningful user segments.

FR-017 — Reproducibility

The system shall provide sufficient configuration, dependency, data, and execution documentation to reproduce results.

FR-018 — Testing

The system shall provide automated tests for important data, model, recommendation, API, and evaluation components.

25. NON-FUNCTIONAL REQUIREMENTS
NFR-001 — Correctness

ML and software components must behave according to their documented specifications.

NFR-002 — Reproducibility

Training and evaluation should be repeatable under the documented environment.

NFR-003 — Maintainability

Code should remain modular and understandable.

NFR-004 — Reliability

The system should gracefully handle reasonable invalid and edge-case inputs.

NFR-005 — Explainability

Major recommendation decisions should be explainable at the methodology level.

NFR-006 — Technology Compliance

The project must remain within the approved Python-based stack.

NFR-007 — Documentation Accuracy

Documentation must reflect the actual implementation.

NFR-008 — Evaluation Integrity

Performance claims must originate from verified experiments.

26. EDGE CASE REQUIREMENTS

The system should explicitly handle:

Unknown User
user_id not found
    ↓
Fallback recommendation
Known User With No Eligible Candidates
All candidate products already interacted with
    ↓
Fallback strategy
New Product

Product with metadata but insufficient interaction history should remain eligible for content-based candidate generation where applicable.

Empty Dataset

The application must fail gracefully rather than produce misleading recommendations.

Invalid User ID

The API/UI should return a clear validation error.

Invalid K

The system should reject:

K ≤ 0
Excessively large K
Non-numeric K

according to the final API specification.

27. SECURITY REQUIREMENTS

The system must not expose:

API keys
Passwords
Tokens
Credentials
Secrets

The repository should remain free from hardcoded secrets.

The API should not expose unnecessary internal information through errors.

28. PERFORMANCE REQUIREMENTS

The project is an internship-scale ML system.

Performance goals should therefore be proportional to:

Dataset size
Available compute
Model complexity

The system does not require production-scale distributed infrastructure.

Where practical, recommendation generation should avoid unnecessarily retraining models for every request.

29. REPRODUCIBILITY REQUIREMENTS

A reviewer should be able to understand:

Where the data came from
        ↓
How data was processed
        ↓
How interactions were constructed
        ↓
How models were trained
        ↓
How recommendations were generated
        ↓
How evaluation was performed
        ↓
How results were produced

The repository should provide:

Dependency specification
Configuration
Random seeds where applicable
Data acquisition instructions
Training instructions
Evaluation instructions
Application execution instructions
30. PRODUCT OUTPUTS

The final product should produce:

30.1 Data Outputs
Valid processed interaction dataset
Product metadata table
User summary/segment data
30.2 Model Outputs
Popularity baseline
Collaborative filtering model
Matrix factorization model where retained
Content-based model
Canonical hybrid recommendation engine
30.3 Evaluation Outputs
Precision@K
Recall@K
NDCG@K
Model comparison
Segment-level evaluation
Error analysis
30.4 Application Outputs
FastAPI recommendation service
Streamlit demonstration
30.5 Documentation Outputs
Methodology
Architecture
Experiments
Evaluation
Limitations
Setup
Usage
Final README
31. SUCCESS CRITERIA

Project 3 should not be considered complete merely because the application launches.

Completion requires:

Data
 Required data is available or reproducibly obtainable.
 Data schema is documented.
 Data quality checks pass.
 Interaction representation is valid.
 No fabricated behavioral events are presented as real.
 Temporal data source is legitimate if used.
Modeling
 Popularity baseline works.
 Personalized model works.
 Content-based recommendation works where supported.
 Cold-start strategy works.
 Recommendation engine is centralized.
 Model components are appropriately integrated.
Evaluation
 Precision@K works.
 Recall@K works.
 NDCG@K works.
 Evaluation uses the actual recommendation models.
 Evaluation does not leak future information.
 Temporal validation is legitimate where required.
 Metrics are populated with verified values.
 Model comparison is documented.
User Segments
 Segments are statistically meaningful.
 Segment sizes are reported.
 Recommendation metrics are calculated per segment.
 Segment-level findings are documented.
API
 FastAPI starts successfully.
 /health works.
 Recommendation endpoint works.
 Invalid requests are handled.
 Unknown users are handled.
 API uses canonical RecommendationEngine.
Streamlit
 Application starts.
 User selection works.
 Recommendations are generated.
 Recommendations come from canonical RecommendationEngine.
 Analytics work.
 Segment analysis is displayed where appropriate.
QA
 Unit tests pass.
 Integration tests pass.
 Data validation passes.
 Evaluation tests pass.
 API tests pass.
 Edge cases are tested.
 End-to-end workflow is verified.
32. DEFINITION OF DONE

Project 3 is considered complete only when:

Data
  ↓
Valid

Models
  ↓
Correct

Recommendation Engine
  ↓
Unified

Evaluation
  ↓
Valid

Temporal Validation
  ↓
Legitimate / Explicitly Documented Limitation

Cold Start
  ↓
Functional

User Segmentation
  ↓
Meaningful

API
  ↓
Working

Streamlit
  ↓
Integrated

Tests
  ↓
Passing

Documentation
  ↓
Accurate

GitHub
  ↓
Professional

Final QA
  ↓
Passed
33. ACCEPTANCE CRITERIA
AC-001 — Data Pipeline

Given a valid project environment and documented dataset source,

the system should be able to:

Acquire/restore the required data.
Validate the data.
Process the data.
Produce required intermediate datasets.
AC-002 — Popularity Baseline

Given valid processed data,

the system should produce a ranked popularity-based recommendation list.

AC-003 — Personalized Recommendation

Given a known user with sufficient history,

the system should produce personalized recommendations.

AC-004 — Cold-Start User

Given an unknown/new user,

the system should return an appropriate fallback recommendation.

AC-005 — Cold-Start Product

Given a new product with valid metadata,

the content-based pipeline should be capable of considering it as a recommendation candidate where the methodology supports this.

AC-006 — Ranking Metrics

Given predictions and held-out relevant items,

the evaluation system should correctly calculate:

Precision@K
Recall@K
NDCG@K
AC-007 — Evaluation Integrity

The evaluation pipeline must:

Use the documented split.
Avoid leakage.
Evaluate the actual models.
Produce reproducible results.
AC-008 — API

Given a valid user ID,

the API should return:

User identifier
Number of recommendations
Ranked recommendation records
AC-009 — Streamlit

Given a valid user,

the Streamlit application should display recommendations generated by the canonical engine.

AC-010 — Segment Analysis

The system should provide recommendation-quality metrics for defined user segments where sufficient data exists.

34. QUALITY BAR

The project should meet the following quality hierarchy:

Level 1 — Functional

The system runs.

Level 2 — Correct

The system implements the required algorithms correctly.

Level 3 — Validated

The system is evaluated using a valid methodology.

Level 4 — Reproducible

Another developer can reproduce the results.

Level 5 — Integrated

API, Streamlit, evaluation, and model logic use a coherent architecture.

Level 6 — Capstone Quality

The system is professionally documented and technically defensible.

The final target is:

Level 6 — Capstone Quality

35. KNOWN CURRENT LIMITATIONS

The following are currently known from the repository audit and must not be hidden:

Core raw and processed datasets are missing.
Current dataset lacks timestamps.
Current dataset does not contain genuine views/clicks/carts/purchases.
Current evaluation uses random splitting.
Current evaluation does not evaluate the canonical engine.
Evaluation report contains placeholders.
Streamlit recommendation logic differs from RecommendationEngine.
Matrix Factorization is currently disconnected.
Content-based cold-start behavior is blocked by candidate filtering.
User segmentation is highly imbalanced.
Segment analysis does not currently evaluate recommendation quality.
Dependency configuration contains a pytest typo.
Some documentation contains inconsistencies.

These limitations are current-state findings, not final product requirements.

36. DATA SOURCE INTEGRITY POLICY

The project shall distinguish between:

Source Data

Data directly obtained from the legitimate dataset source.

Derived Data

Data calculated from source data.

Proxy Features

Features derived to represent a concept that is not directly present.

Synthetic Data

Artificially generated data.

Synthetic data must never be represented as real behavioral observations.

If synthetic data is used for testing only, it must be clearly labeled:

Synthetic test data — not used as evidence of real user behavior.

37. TEMPORAL DATA INTEGRITY POLICY

Temporal information is especially important because the official project requires time-based validation.

Therefore:

Allowed
Original source timestamps.
Timestamps from an authoritative corresponding dataset version.
Legitimately documented temporal metadata.
Not Allowed
Randomly generated timestamps.
Sequential timestamps invented solely for evaluation.
Reordering observations and treating order as real time.
Assigning timestamps based on row order.
Presenting synthetic chronology as historical behavior.
38. MODEL COMPARISON PRINCIPLE

Models must be compared using the same evaluation framework wherever appropriate.

Potential comparison:

Popularity Baseline
        ↓
Collaborative Filtering
        ↓
Matrix Factorization
        ↓
Content-Based
        ↓
Hybrid

The comparison must report actual measured results.

No model may be declared superior without evidence.

39. ERROR ANALYSIS PRINCIPLE

Evaluation must not stop at aggregate metrics.

Where practical, the final system should investigate:

Poor recommendations
Users with sparse history
Users with extensive history
Cold-start cases
Popularity bias
Long-tail coverage
Segment differences
Candidate-generation failures
Ranking errors

The goal is to understand:

Why did the recommendation system succeed or fail?

40. PORTFOLIO REQUIREMENTS

The final project should be presentable as a professional ML portfolio project.

The repository should communicate:

Problem

What recommendation problem is being solved?

Data

What data is used?

Methodology

How are recommendations generated?

Evaluation

How is recommendation quality measured?

Results

What did the experiments actually show?

Engineering

How is the system structured?

Application

How can recommendations be requested?

Limitations

What cannot the system currently do?

Future Scope

What could be improved?

41. INTERVIEW-READINESS REQUIREMENT

The final implementation should allow the developer to explain:

Recommendation Systems
What is collaborative filtering?
What is content-based filtering?
What is matrix factorization?
What is a hybrid recommender?
What is the cold-start problem?
Evaluation
What is Precision@K?
What is Recall@K?
What is NDCG@K?
Why is accuracy inappropriate as the primary ranking metric?
Why is temporal validation important?
Data
How were interactions constructed?
What limitations exist in the dataset?
How was leakage prevented?
Engineering
Why is RecommendationEngine centralized?
How does FastAPI interact with the engine?
How does Streamlit interact with the engine?
How is the system reproduced?
Results
Which model performed how?
Why?
Where did it fail?
What limitations remain?

No answer should depend on fabricated results.

42. FUTURE SCOPE

Potential future enhancements include:

More sophisticated hybrid ranking.
Better cold-start modeling.
Additional product metadata.
Context-aware recommendation.
Learning-to-rank models.
Online evaluation.
Real-time feedback loops.
More advanced implicit-feedback algorithms.
Production-scale serving.
Model monitoring.
Recommendation diversity optimization.

These are future possibilities and are not mandatory Project 3 requirements.

43. PROJECT GOVERNANCE

The following documents govern the implementation:

PRD.md
    ↓
PROJECT_SPECIFICATIONS.md
    ↓
DATASET_AND_DATA_STRATEGY.md
    ↓
ML_METHODOLOGY.md
    ↓
EXPERIMENT_PLAN.md
    ↓
EVALUATION_AND_ERROR_ANALYSIS.md
    ↓
SYSTEM_ARCHITECTURE.md
    ↓
TASK_TRACKER.md
    ↓
RULES.md
    ↓
DOCUMENTATION_AND_REPORTING.md

The official internship specification remains the highest-level external requirement source.

The repository audit defines the current implementation baseline.

44. CHANGE MANAGEMENT

Any significant change to the project must consider:

Official internship requirements.
Current repository architecture.
Data availability.
ML correctness.
Evaluation validity.
Reproducibility.
Engineering complexity.
Deadline impact.

Major changes should not be introduced simply because another technology or algorithm appears newer.

45. TRACEABILITY TO OFFICIAL REQUIREMENTS
Requirement	PRD Requirement
User-item interaction data	FR-003
Views/clicks/carts/purchases requirement	Sections 4, 18, 36
Popularity baseline	FR-004
Collaborative filtering / matrix factorization	FR-005
Item metadata	FR-006
Content-based fallback	FR-006 / FR-007
Precision@K	FR-012
Recall@K	FR-013
NDCG@K	FR-014
Time-based validation	FR-015
Recommendation API	FR-010
User segment analysis	FR-016
Python	Section 13
Git/GitHub	Section 13
Streamlit/API	FR-010 / FR-011
46. RELATED CONTROL DOCUMENTS

The following documents will provide deeper technical specifications:

PROJECT_SPECIFICATIONS.md

Defines detailed functional and technical requirements, acceptance criteria, requirement IDs, dependencies, and verification methods.

DATASET_AND_DATA_STRATEGY.md

Defines:

Dataset provenance
Dataset acquisition
Schema
Data restoration
Missing data
Interaction representation
Timestamp investigation
Data quality
Leakage prevention
Reproducibility
ML_METHODOLOGY.md

Defines:

Popularity baseline
Collaborative filtering
Matrix factorization
Content-based filtering
Hybrid recommendation
Candidate generation
Ranking
Cold-start methodology
EXPERIMENT_PLAN.md

Defines:

Experiments
Baselines
Model comparisons
Hyperparameters
Ablation studies
Reproducibility
Expected outputs
EVALUATION_AND_ERROR_ANALYSIS.md

Defines:

Precision@K
Recall@K
NDCG@K
Temporal validation
Segment evaluation
Leakage controls
Error analysis
SYSTEM_ARCHITECTURE.md

Defines:

Components
Data flow
Module responsibilities
API architecture
Streamlit architecture
Recommendation engine architecture
TASK_TRACKER.md

Defines the actual implementation tasks and their status.

RULES.md

Defines non-negotiable project rules.

DOCUMENTATION_AND_REPORTING.md

Defines how results, experiments, methodology, screenshots, reports, and final documentation are maintained.

47. FINAL PRODUCT STATEMENT

The final product shall be:

A reproducible, technically correct, professionally documented personalized product recommendation system that learns from legitimate user-item interaction data, establishes a popularity baseline, provides personalized recommendations using collaborative filtering and/or matrix factorization, uses product metadata for content-based recommendation and cold-start support where applicable, evaluates ranking quality using Precision@K, Recall@K, and NDCG@K under a legitimate validation methodology, analyzes recommendation performance across meaningful user segments, and exposes the final recommendation engine through a simple FastAPI and Streamlit interface.

The system must preserve the integrity of the underlying data and must never fabricate behavioral events, timestamps, metrics, experiments, or performance claims.

The project must be something that can be:

Demonstrated
Reproduced
Tested
Explained
Defended
Evaluated
Published professionally
48. FINAL STANDARD

The ultimate standard for Project 3 is not:

"The application runs."

It is:

"The recommendation system is technically correct, the data methodology is defensible, the evaluation is trustworthy, the architecture is coherent, the results are reproducible, the limitations are honestly documented, and the developer can explain and defend every major technical decision."

Therefore:

Correctness
    >
Complexity

Evidence
    >
Assumption

Real Data
    >
Fabricated Compliance

Valid Evaluation
    >
Impressive-Looking Metrics

Unified Architecture
    >
Duplicated Implementations

Reproducibility
    >
One-Time Execution

Understanding
    >
Library Usage

Capstone Quality
    >
Assignment Completion

END OF PRD.md


### Why this version is the right foundation

The major improvement is that this PRD now explicitly incorporates the **actual audit reality** rather than pretending Project 3 is starting from a clean slate. For example, the audit found that the existing Recommendation Engine, FastAPI architecture, Streamlit structure, metric functions, popularity model, and utilities are worth preserving. :contentReference[oaicite:1]{index=1}

It also locks in the two methodological decisions we discussed:

- **No fake views/clicks/carts/purchases** — the audited dataset currently contains explicit ratings instead. :contentReference[oaicite:2]{index=2}
- **No fake timestamps** — the audited source lacks timestamps, and the existing random 80/20 split therefore does not satisfy the temporal requirement. :contentReference[oaicite:3]{index=3}

And the PRD deliberately leaves the **legitimate timestamp recovery method** for `DATASET_AND_DATA_STRATEGY.md`, where we can properly investigate the dataset provenance and determine whether an authoritative timestamp-bearing source/version can be obtained rather than making a methodological shortcut.

Most importantly, this gives us a clean hierarchy:

**PRD = WHAT we're building**  
**PROJECT_SPECIFICATIONS = EXACTLY what must be satisfied**  
**DATASET_AND_DATA_STRATEGY = WHAT data we can legitimately use**  
**ML_METHODOLOGY = HOW the recommender works**  
**EXPERIMENT_PLAN = WHAT we test**  
**EVALUATION = HOW we prove it works**

That separation will make the subsequent Google AI Studio prompts much safer and much more precise.
