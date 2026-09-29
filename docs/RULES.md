# RULES.md

# Project Rules & Non-Negotiable Engineering Standards
## Personalized Product Recommendation Model

---

## Document Control

| Field | Value |
|---|---|
| Project | Personalized Product Recommendation Model |
| Project Number | Project 3 |
| Document | `RULES.md` |
| Version | 1.0 |
| Status | Approved — Mandatory |
| Rule Type | Engineering + ML + Data + QA + Documentation |
| Primary Language | Python |
| ML Stack | Scikit-learn / SciPy |
| API | FastAPI |
| Application | Streamlit |
| Version Control | Git / GitHub |
| Parent Documents | `PRD.md`, `PROJECT_SPECIFICATIONS.md` |
| Purpose | Define non-negotiable rules governing all Project 3 implementation work |

---

# 1. PURPOSE

This document defines the **mandatory rules, constraints, safeguards, engineering standards, machine-learning integrity requirements, data rules, evaluation rules, documentation rules, and implementation controls** for Project 3.

The purpose of this document is to ensure that every implementation change made to the repository remains:

- Correct
- Reproducible
- Defensible
- Requirement-compliant
- Data-integrity preserving
- Evaluation-safe
- Architecturally consistent
- Maintainable
- Professionally documented

These rules apply to:

- Human development
- Google AI Studio modifications
- AI-generated code
- Refactoring
- Bug fixes
- Model development
- Data processing
- Evaluation
- API development
- Streamlit development
- Testing
- Documentation
- Git/GitHub operations

---

# 2. RULE AUTHORITY

These rules operate within the following project hierarchy:

```text
Official Internship Requirements
            ↓
        PRD.md
            ↓
PROJECT_SPECIFICATIONS.md
            ↓
       RULES.md
            ↓
Specialized Technical Documents
            ↓
Implementation
```

Where a conflict exists:

1. Official internship requirements take precedence.
2. `PRD.md` defines approved product direction.
3. `PROJECT_SPECIFICATIONS.md` defines technical requirements.
4. `RULES.md` defines mandatory implementation behavior.
5. Specialized documents provide domain-specific details.
6. Existing code is preserved unless modification is justified.

No implementation should silently override a higher-level requirement.

---

# 3. CORE PROJECT PRINCIPLES

The following principles are absolute unless an explicit higher-priority requirement requires otherwise.

---

## RULE-CORE-001 — Correctness Over Complexity

A simpler correct implementation is always preferable to a more complex implementation that is difficult to validate.

```text
Correct + Simple
        >
Complex + Unverified
```

Do not introduce complexity merely to make the project appear more advanced.

---

## RULE-CORE-002 — Evidence Over Assumption

Do not assume that a feature works because:

- A file exists.
- A function exists.
- The application launches.
- An AI model generated the code.
- A README says it works.
- A previous experiment worked.

Implementation must be verified through execution, testing, inspection, or reproducible evidence.

---

## RULE-CORE-003 — Preserve Existing Valid Work

Existing technically valid components must be preserved wherever possible.

Important existing components include:

- `RecommendationEngine`
- FastAPI structure
- Streamlit structure
- Precision@K
- Recall@K
- NDCG@K
- Popularity model
- `data_utils.py`
- Existing Python/scikit-learn/SciPy architecture

Do not rewrite functioning components merely for stylistic reasons.

---

## RULE-CORE-004 — Repair Before Rebuild

When an existing component is defective:

```text
Inspect
  ↓
Understand
  ↓
Repair
  ↓
Test
  ↓
Verify
```

Do not immediately replace it with an entirely new implementation.

---

## RULE-CORE-005 — One Canonical Recommendation Pipeline

There must be one authoritative recommendation pipeline.

The following must not silently implement different recommendation algorithms:

- API
- Streamlit
- Evaluation
- Recommendation Engine

They should use the same canonical recommendation logic wherever applicable.

---

## RULE-CORE-006 — No Hidden Behavior

Important recommendation behavior must not be hidden inside:

- UI code
- API routes
- notebooks
- temporary scripts
- duplicated helper functions

Core recommendation logic belongs in the recommendation/model layer.

---

# 4. REPOSITORY INTEGRITY RULES

---

## RULE-REPO-001 — Do Not Delete Existing Files Without Authorization

No existing project file may be deleted merely because:

- It appears unused.
- It is not currently imported.
- An AI coding tool considers it unnecessary.
- A cleaner architecture is possible.
- Another framework has been introduced.

Deletion requires:

1. Identification.
2. Dependency/use analysis.
3. Technical justification.
4. Confirmation that no requirement depends on it.
5. Explicit approval.

---

## RULE-REPO-002 — No Unrequested Technology Migration

The project must not be migrated to a different technology stack without explicit approval.

The approved primary stack is:

```text
Python
Scikit-learn
SciPy
FastAPI
Streamlit
Git
GitHub
```

---

## RULE-REPO-003 — No Frontend Framework Creep

Do not add:

- React
- TypeScript
- Vite
- Tailwind CSS
- Next.js
- Vue
- Angular
- Other frontend frameworks

unless a higher-level requirement explicitly requires them.

The existing Streamlit architecture is sufficient for the application layer.

---

## RULE-REPO-004 — No Unnecessary Dependencies

Before adding a dependency, verify:

1. Existing project functionality cannot reasonably accomplish the requirement.
2. The dependency provides clear technical value.
3. It is compatible with the project stack.
4. It does not introduce unnecessary complexity.
5. It is documented.

Do not add packages simply because they are popular.

---

## RULE-REPO-005 — Preserve Directory Architecture

Do not restructure the repository merely for visual cleanliness.

Any directory restructuring must be:

- Requirement-driven
- Documented
- Tested
- Consistent with `SYSTEM_ARCHITECTURE.md`

---

## RULE-REPO-006 — No Unexplained Generated Files

Do not commit:

- Temporary files
- Debug outputs
- Local caches
- Editor artifacts
- Unnecessary generated files
- Experimental leftovers

unless explicitly required by the project.

---

## RULE-REPO-007 — No Silent File Replacement

Existing files must not be overwritten wholesale when a targeted modification is sufficient.

Prefer:

```text
Minimal targeted modification
```

over:

```text
Complete uncontrolled rewrite
```

---

# 5. GOOGLE AI STUDIO RULES

These rules are particularly important because Google AI Studio will be used for implementation.

---

## RULE-AI-001 — Read Before Modifying

Before modifying the repository, AI Studio must inspect:

- Existing directory structure
- Relevant source files
- Configuration
- Tests
- Documentation
- Existing recommendation logic

---

## RULE-AI-002 — No Unauthorized Deletion

Google AI Studio must not delete existing files without explicit instruction.

This applies even if the AI determines that a file is:

- Redundant
- Obsolete
- Unused
- Poorly designed
- Replaced by another file

---

## RULE-AI-003 — No Unauthorized File Addition

AI Studio must not add unrelated files, frameworks, or architecture merely because they are common in generated applications.

New files must have a documented project purpose.

---

## RULE-AI-004 — Preserve Existing Technology Stack

AI Studio must not automatically introduce:

- React
- Vite
- TypeScript
- Tailwind
- Node.js frontend architecture

The repository is a Python ML project.

---

## RULE-AI-005 — No Autonomous Architecture Rewrite

AI Studio must not independently redesign the entire project.

Changes must follow:

- `PRD.md`
- `PROJECT_SPECIFICATIONS.md`
- `SYSTEM_ARCHITECTURE.md`
- `RULES.md`

---

## RULE-AI-006 — No Fabricated Completion

AI Studio must never state:

> "Implemented successfully"

unless the implementation has actually been executed or verified.

---

## RULE-AI-007 — No Fabricated Test Results

AI Studio must never claim:

```text
All tests passed
```

unless the test suite was actually executed.

---

## RULE-AI-008 — No Fabricated Metrics

AI Studio must never generate plausible-looking recommendation metrics without actual evaluation.

---

## RULE-AI-009 — No Fabricated Data

AI Studio must never create fake production data and present it as source data.

---

## RULE-AI-010 — Explain Significant Changes

For major modifications, the implementation process should identify:

- What changed
- Why it changed
- Which requirement it satisfies
- What files were affected
- How it was verified

---

# 6. DATA INTEGRITY RULES

---

## RULE-DATA-001 — Source Data Must Be Legitimate

Only legitimate and documented data sources may be used for final results.

---

## RULE-DATA-002 — Never Fabricate User Behavior

Do not fabricate:

- Views
- Clicks
- Cart additions
- Purchases
- Ratings
- User interactions

and present them as genuine observations.

---

## RULE-DATA-003 — Derived Data Must Be Labeled

If a source field is transformed into a derived representation, document:

- Original field
- Transformation
- Reason
- Resulting semantics

Example:

```text
Source:
rating

Derived:
binary interaction indicator

Documentation:
Derived interaction representation from explicit rating data.
```

Do not rename the derived feature to falsely imply that it represents a purchase.

---

## RULE-DATA-004 — Synthetic Data Is Testing-Only Unless Explicitly Approved

Synthetic data may be used for:

- Unit tests
- Controlled metric validation
- Edge-case testing
- Demonstration of algorithm behavior

It must never silently become evidence for final project performance.

Synthetic datasets must be clearly labeled.

---

## RULE-DATA-005 — Never Fabricate Timestamps

Timestamps must never be:

- Randomly generated
- Assigned based on row order
- Fabricated from IDs
- Fabricated from file order
- Invented to satisfy temporal validation

---

## RULE-DATA-006 — Legitimate Timestamp Recovery

If a timestamp-bearing version/source corresponding to the project dataset can legitimately be obtained, it may be used after verification.

The following must be documented:

- Source
- Provenance
- Schema compatibility
- Timestamp semantics
- Mapping to project records
- Validation procedure

---

## RULE-DATA-007 — Missing Data Must Be Reported

If a required data field is unavailable, do not silently substitute fabricated information.

Instead:

```text
Missing
   ↓
Investigate
   ↓
Recover legitimately if possible
   ↓
Otherwise document limitation
```

---

## RULE-DATA-008 — Data Schema Must Be Verified

Before modeling, verify:

- Required columns
- Data types
- Identifier uniqueness/validity
- Missingness
- Value ranges
- Duplicate behavior

---

## RULE-DATA-009 — Preserve Source Semantics

Do not rename or reinterpret fields in a way that changes their meaning.

---

## RULE-DATA-010 — No Manual Undocumented Data Modification

Manual changes to datasets must not be used for final experiments unless:

- The modification is necessary.
- It is documented.
- It is reproducible.
- It is applied through a controlled process.

---

# 7. DATA LEAKAGE RULES

---

## RULE-LEAK-001 — Future Data Must Never Enter Training

Evaluation-period information must not influence model training.

---

## RULE-LEAK-002 — No Evaluation-Derived Features

Features must not be constructed using future evaluation outcomes.

---

## RULE-LEAK-003 — Popularity Must Respect the Evaluation Boundary

Popularity statistics used in temporal evaluation must be calculated using only information permitted by the training period.

---

## RULE-LEAK-004 — Content Model Leakage Prevention

TF-IDF/vectorization and similar transformations must be fitted according to the evaluation protocol.

Do not use information from a future evaluation context in a way that leaks the target.

---

## RULE-LEAK-005 — Collaborative Model Isolation

Collaborative filtering models must be trained only using permitted training interactions.

---

## RULE-LEAK-006 — Evaluation Must Be Independent

The evaluation dataset must remain unseen by model-fitting procedures.

---

# 8. INTERACTION MODEL RULES

---

## RULE-INT-001 — Explicitly Define Interaction Semantics

The project must clearly define what an interaction means.

---

## RULE-INT-002 — No False Event Mapping

Do not claim:

```text
rating = purchase
```

or:

```text
rating = click
```

unless an authoritative project-specific methodology explicitly establishes that mapping.

---

## RULE-INT-003 — Interaction Weighting Must Be Justified

If different interaction signals are combined, their weights must be documented and reproducible.

---

## RULE-INT-004 — Duplicate Interactions Must Be Handled Deliberately

Do not silently drop or aggregate duplicate user-item records.

The aggregation policy must be documented.

---

# 9. MODELING RULES

---

## RULE-ML-001 — Baseline Is Mandatory

A popularity baseline must exist before claiming that a personalized model provides improvement.

---

## RULE-ML-002 — Baseline Must Be Honest

The popularity baseline must be evaluated using the same appropriate evaluation framework as other models.

---

## RULE-ML-003 — Model Complexity Must Be Justified

Do not add sophisticated models solely to make the project look advanced.

---

## RULE-ML-004 — Existing Models Must Be Audited Before Replacement

The existing:

- Collaborative Filtering
- Matrix Factorization
- Content-Based model
- Popularity model

must be evaluated before deciding whether to replace them.

---

## RULE-ML-005 — Model Configuration Must Be Reproducible

Important model parameters must be:

- Explicit
- Documented
- Reproducible

---

## RULE-ML-006 — No Unsupported Claims of Superiority

Never state:

> "Model X is the best."

unless supported by documented experimental evidence.

Even then, describe the measured result within the specific evaluation context.

---

## RULE-ML-007 — No Metric Manipulation

Do not:

- Select favorable subsets without justification.
- Change K repeatedly until results look good.
- Remove difficult users solely to improve metrics.
- Report only successful experiments.
- Alter relevance thresholds after seeing results without documenting the change.

---

# 10. POPULARITY MODEL RULES

---

## RULE-POP-001 — Popularity Must Be Explicitly Defined

Document what "popular" means.

---

## RULE-POP-002 — Popularity Must Respect Evaluation Boundaries

Do not calculate popularity using future information during temporal evaluation.

---

## RULE-POP-003 — Popularity Is a Baseline

Popularity should not automatically be presented as personalized recommendation.

---

## RULE-POP-004 — Popularity Fallback Must Be Documented

If popularity is used for cold-start users, that behavior must be explicitly documented.

---

# 11. COLLABORATIVE FILTERING RULES

---

## RULE-CF-001 — Preserve Valid Existing Implementation

The existing collaborative filtering implementation should be preserved if technically valid.

---

## RULE-CF-002 — Similarity Must Be Documented

Document:

- Similarity measure
- Neighbor selection
- Minimum history
- Candidate generation

---

## RULE-CF-003 — Unknown Users Must Have Defined Behavior

Collaborative filtering must not crash when a user is unknown.

---

## RULE-CF-004 — Sparse Users Must Have Defined Behavior

Users with insufficient interaction history must have a documented fallback.

---

## RULE-CF-005 — No Hidden Candidate Filtering

Candidate restrictions must be visible and justified.

---

# 12. MATRIX FACTORIZATION RULES

---

## RULE-MF-001 — Existing Prototype Must Be Validated

The existing matrix-factorization implementation must not automatically be treated as production-ready.

---

## RULE-MF-002 — Matrix Semantics Must Be Correct

The project must document:

- Rows
- Columns
- Values
- Missing values
- Transformation

---

## RULE-MF-003 — Model Must Be Evaluated Before Promotion

A matrix-factorization model must demonstrate valid behavior under the project evaluation framework before being used as a final model.

---

# 13. CONTENT-BASED MODEL RULES

---

## RULE-CB-001 — Use Real Product Metadata

Content-based recommendation must use legitimate product metadata.

---

## RULE-CB-002 — Metadata Must Be Documented

Document:

- Fields used
- Preprocessing
- Vectorization
- Similarity metric

---

## RULE-CB-003 — Avoid Candidate-Pool Cold-Start Failure

Do not restrict the content model to a popularity pool in a way that prevents new products from being considered.

---

## RULE-CB-004 — Content Model Must Respect Evaluation Boundaries

Feature construction must not leak evaluation information.

---

# 14. COLD-START RULES

---

## RULE-COLD-001 — Define Cold Start Explicitly

The project must distinguish:

- New user
- Sparse user
- New product
- Sparse product

---

## RULE-COLD-002 — New User Must Not Crash

Unknown users must receive a defined fallback where possible.

---

## RULE-COLD-003 — New Product Must Not Be Silently Excluded

If valid product metadata exists, new products should remain eligible for content-based recommendation.

---

## RULE-COLD-004 — Fallback Hierarchy Must Be Deterministic

The fallback order must be documented.

Example:

```text
Personalized model
      ↓
Content-based fallback
      ↓
Popularity fallback
```

The exact final hierarchy shall be defined in `ML_METHODOLOGY.md`.

---

# 15. RECOMMENDATION ENGINE RULES

---

## RULE-REC-001 — RecommendationEngine Is Canonical

The existing `RecommendationEngine` is the designated foundation for the final recommendation system.

---

## RULE-REC-002 — No Duplicate Recommendation Algorithms

Do not independently implement recommendation logic in:

- Streamlit
- FastAPI
- Evaluation scripts

when the canonical engine can be used.

---

## RULE-REC-003 — Separate Candidate Generation and Ranking

Where practical, recommendation architecture should distinguish:

```text
Candidate Generation
        ↓
Candidate Filtering
        ↓
Feature/Score Generation
        ↓
Score Combination
        ↓
Ranking
        ↓
Top-K
```

---

## RULE-REC-004 — No Duplicate Products

Final recommendation lists must not contain duplicate products.

---

## RULE-REC-005 — Previously Interacted Items

Where appropriate to the evaluation/product definition, previously consumed/interacted products should be filtered.

The exact policy must be documented.

---

## RULE-REC-006 — Score Normalization

When combining heterogeneous model scores, normalize them appropriately before weighted combination.

---

## RULE-REC-007 — Hybrid Weights Must Be Configurable

Do not hardcode unexplained weights throughout the codebase.

---

## RULE-REC-008 — Hybrid Weights Must Not Be Called Optimal Without Evidence

A chosen weighting such as:

```text
50% collaborative
30% content
20% popularity
```

is a configuration, not automatically an optimized result.

---

## RULE-REC-009 — Recommendation Output Must Be Stable

For the same input and same model/data/configuration, the recommendation output should be deterministic where possible.

---

# 16. EVALUATION RULES

---

## RULE-EVAL-001 — Evaluate the Actual Recommendation System

The final evaluation must evaluate actual recommendation outputs from the model being claimed.

---

## RULE-EVAL-002 — No Toy Heuristic Substitution

A separate heuristic may be used as a baseline, but it must never be presented as evaluation of the final Recommendation Engine.

---

## RULE-EVAL-003 — Required Metrics

The project must evaluate:

- Precision@K
- Recall@K
- NDCG@K

---

## RULE-EVAL-004 — Metric Definitions Must Be Fixed

Before final evaluation, define:

- Relevant item
- K
- Evaluation users
- Candidate pool
- Filtering rules
- Aggregation method

---

## RULE-EVAL-005 — No Placeholder Metrics

Final reports must not contain:

- `TBD`
- `TODO`
- invented values
- example values
- estimated values presented as measured results

---

## RULE-EVAL-006 — No Fabricated Evaluation

Every reported number must come from an actual executed experiment.

---

## RULE-EVAL-007 — Same Evaluation Conditions

Models being compared should use equivalent evaluation conditions wherever appropriate.

---

## RULE-EVAL-008 — Full Eligible Population

Use the full eligible evaluation population unless a sampling strategy is justified and documented.

---

## RULE-EVAL-009 — Evaluation Code Must Be Tested

Metric implementations must be verified using controlled examples with known expected results.

---

# 17. TEMPORAL VALIDATION RULES

---

## RULE-TIME-001 — Time-Based Validation Is a Methodological Requirement

Where a legitimate timestamp-bearing source is available, temporal validation must be used as specified by the project.

---

## RULE-TIME-002 — No Fake Time

Never manufacture timestamps for final evaluation.

---

## RULE-TIME-003 — Chronological Order Must Be Real

Rows must be ordered according to legitimate timestamp information.

---

## RULE-TIME-004 — Training Must Precede Validation

Training observations must occur before validation observations according to the documented temporal boundary.

---

## RULE-TIME-005 — Future Information Is Forbidden

Future interactions must not influence historical recommendations.

---

## RULE-TIME-006 — Timestamp Source Must Be Documented

Document:

- Source
- Field
- Meaning
- Timezone if relevant
- Granularity
- Missingness
- Validity

---

## RULE-TIME-007 — Honest Limitation Reporting

If no legitimate timestamp-bearing source can be obtained, do not falsely claim compliance.

Document the limitation and the alternative methodology used.

---

# 18. USER SEGMENTATION RULES

---

## RULE-SEG-001 — Segments Must Be Meaningful

Do not create arbitrary segments solely because segmentation is required.

---

## RULE-SEG-002 — Segment Thresholds Must Be Justified

Thresholds must be supported by:

- Data distribution
- Statistical reasoning
- Domain rationale

---

## RULE-SEG-003 — Do Not Force Balanced Segments

Artificially equalizing segment sizes is not required unless justified.

---

## RULE-SEG-004 — Segment Analysis Must Measure Recommendations

User counts alone are insufficient.

Where data permits, analyze:

- Precision@K
- Recall@K
- NDCG@K

by segment.

---

## RULE-SEG-005 — Segment Definitions Must Remain Stable

Do not redefine segments after seeing results merely to improve conclusions.

Any methodology change must be documented.

---

# 19. API RULES

---

## RULE-API-001 — Preserve FastAPI Architecture

The existing FastAPI architecture should be retained.

---

## RULE-API-002 — API Must Use Canonical Engine

The API must call the canonical Recommendation Engine.

---

## RULE-API-003 — Validate Inputs

Validate:

- User ID
- K
- Request structure

---

## RULE-API-004 — Handle Errors Gracefully

API errors must be explicit and useful.

---

## RULE-API-005 — No Business Logic Duplication

Recommendation algorithms should not be duplicated inside API routes.

---

## RULE-API-006 — Stable Response Contract

API response structure must be documented and tested.

---

# 20. STREAMLIT RULES

---

## RULE-APP-001 — Preserve Existing Streamlit Structure

Do not replace the application with another frontend framework.

---

## RULE-APP-002 — Use Canonical Engine

Streamlit must use the same recommendation engine as the API.

---

## RULE-APP-003 — No Hidden Recommendation Formula

Do not implement an independent:

```text
70% content + 30% popularity
```

or any other separate recommendation formula inside Streamlit unless it is explicitly part of a named experiment/baseline.

---

## RULE-APP-004 — UI Must Reflect Actual Data

Do not display:

- Fake statistics
- Fake metrics
- Fake user counts
- Fake recommendations
- Fake model performance

---

## RULE-APP-005 — Application Errors Must Be Visible

The UI should communicate failures rather than silently displaying misleading content.

---

# 21. TESTING RULES

---

## RULE-TEST-001 — Tests Must Be Real

A test must execute code and verify behavior.

---

## RULE-TEST-002 — No Fake Passing Tests

Do not write tests that merely assert:

```python
assert True
```

without testing meaningful behavior.

---

## RULE-TEST-003 — Test Critical Functions

Tests should cover:

- Data validation
- Recommendation generation
- Ranking
- Metrics
- API
- Fallbacks

---

## RULE-TEST-004 — Test Edge Cases

At minimum consider:

- Unknown user
- Empty history
- Sparse user
- Empty candidate set
- Invalid K
- Duplicate candidates
- Missing metadata
- Empty dataset

---

## RULE-TEST-005 — Test Metrics Independently

Metric functions must be tested with known examples.

---

## RULE-TEST-006 — Integration Tests Must Use Canonical Components

Integration tests should verify actual component connections.

---

## RULE-TEST-007 — Test Results Must Be Executed

Do not report test counts from memory or expectation.

---

## RULE-TEST-008 — Failed Tests Must Not Be Hidden

A failing test must either:

1. Be fixed, or
2. Be explicitly documented as unresolved.

---

# 22. REPRODUCIBILITY RULES

---

## RULE-REP-001 — Reproducible Environment

Required dependencies and compatible Python version must be documented.

---

## RULE-REP-002 — Reproducible Data

Dataset acquisition/restoration must be reproducible.

---

## RULE-REP-003 — Reproducible Models

Model configuration must be documented.

---

## RULE-REP-004 — Reproducible Experiments

Important experiments must have:

- Configuration
- Input data
- Model
- Evaluation procedure
- Output

---

## RULE-REP-005 — Control Randomness

Random processes should use explicit seeds where practical.

---

## RULE-REP-006 — Results Must Be Traceable

A final metric should be traceable to:

```text
Dataset
  ↓
Preprocessing
  ↓
Split
  ↓
Model
  ↓
Configuration
  ↓
Recommendation
  ↓
Metric
```

---

# 23. CODE QUALITY RULES

---

## RULE-CODE-001 — Readable Python

Code must prioritize readability and maintainability.

---

## RULE-CODE-002 — Single Responsibility

Functions/classes should have focused responsibilities.

---

## RULE-CODE-003 — Avoid Unnecessary Duplication

Shared logic should be centralized.

---

## RULE-CODE-004 — Avoid Giant Functions

Do not create large functions containing unrelated responsibilities.

---

## RULE-CODE-005 — Meaningful Names

Use meaningful variable/function/class names.

Avoid unexplained names such as:

```text
x
tmp
foo
data2
model_final2
new_model_final
```

in important production code.

---

## RULE-CODE-006 — Type Hints Where Useful

Use type hints for important interfaces.

---

## RULE-CODE-007 — No Silent Exception Handling

Avoid:

```python
except Exception:
    pass
```

unless there is a documented reason.

---

## RULE-CODE-008 — Logging and Diagnostics

Important failures should provide useful diagnostic information.

---

# 24. CONFIGURATION RULES

---

## RULE-CONFIG-001 — Centralize Configuration

Important settings should be centralized.

Examples:

- Dataset paths
- Model parameters
- K
- Random seed
- Recommendation weights
- API configuration

---

## RULE-CONFIG-002 — Avoid Hardcoded Paths

Do not depend on one developer's local absolute paths.

---

## RULE-CONFIG-003 — No Environment-Specific Assumptions

The project should not require:

```text
C:\Users\SpecificUser\...
```

or equivalent machine-specific paths.

---

# 25. DEPENDENCY RULES

---

## RULE-DEP-001 — Correct Dependency Names

Every dependency must use its correct package name.

---

## RULE-DEP-002 — No Unused Dependencies

Avoid adding dependencies that are never used.

---

## RULE-DEP-003 — Dependency Changes Must Be Verified

After modifying dependencies:

1. Install environment.
2. Run tests.
3. Run relevant scripts.
4. Start application where applicable.

---

# 26. DOCUMENTATION RULES

---

## RULE-DOC-001 — Documentation Must Reflect Reality

Documentation must never claim functionality that does not exist.

---

## RULE-DOC-002 — Results Must Be Actual

Every reported metric must correspond to an actual experiment.

---

## RULE-DOC-003 — Limitations Must Be Honest

Do not hide:

- Missing timestamps
- Dataset limitations
- Model limitations
- Evaluation limitations
- Cold-start limitations
- Computational constraints

---

## RULE-DOC-004 — No Contradictory Documents

Control documents must remain consistent.

If a methodology changes, update all affected documents.

---

## RULE-DOC-005 — Terminology Must Remain Consistent

For example:

```text
User
Item
Interaction
Recommendation
Candidate
Ranking
Precision@K
Recall@K
NDCG@K
Cold Start
```

must be used consistently.

---

# 27. EXPERIMENT RULES

---

## RULE-EXP-001 — Every Experiment Has a Purpose

Do not run experiments merely to generate numbers.

---

## RULE-EXP-002 — Define Experiment Before Execution

Where practical, define:

- Objective
- Hypothesis
- Dataset
- Model
- Parameters
- Evaluation
- Expected interpretation

before running the experiment.

---

## RULE-EXP-003 — Preserve Negative Results

Failed or inferior experiments should not be deleted from project reasoning merely because they produced poor results.

---

## RULE-EXP-004 — Do Not Tune Against the Test Set

The final test/evaluation data must not become a tuning playground.

---

## RULE-EXP-005 — Document Significant Experiments

Important experiments should be recorded in the experiment documentation.

---

# 28. MODEL EVALUATION INTEGRITY RULES

---

## RULE-INTEGRITY-001 — No Cherry-Picking

Do not selectively report only favorable models or configurations.

---

## RULE-INTEGRITY-002 — Same Metric Definitions

Metrics must use consistent definitions across models.

---

## RULE-INTEGRITY-003 — Same Evaluation Population

Models should be compared over equivalent eligible populations.

---

## RULE-INTEGRITY-004 — Same K

When comparing models, use the same K unless there is a documented reason otherwise.

---

## RULE-INTEGRITY-005 — No Unsupported Causality

Do not claim:

> "Model X performs better because of algorithm Y"

unless the experiment supports that interpretation.

---

# 29. COLD-START INTEGRITY RULES

---

## RULE-COLD-INT-001 — No False Cold-Start Claims

Do not claim cold-start support merely because a fallback function exists.

The actual candidate-generation path must permit the cold-start case.

---

## RULE-COLD-INT-002 — Test New Products

Where metadata exists, test whether a new product can actually enter the recommendation candidate set.

---

## RULE-COLD-INT-003 — Test Unknown Users

Unknown users must be tested explicitly.

---

# 30. USER SEGMENTATION INTEGRITY RULES

---

## RULE-SEG-INT-001 — Segment Definitions Before Results

Do not create segment boundaries after seeing recommendation performance solely to produce a preferred narrative.

---

## RULE-SEG-INT-002 — Report Segment Sizes

Every segment analysis must report the number of eligible users.

---

## RULE-SEG-INT-003 — Small Segments Require Caution

Do not make strong conclusions from segments with extremely small sample sizes.

---

# 31. GIT RULES

---

## RULE-GIT-001 — Commit Coherent Changes

Each commit should represent a meaningful change.

---

## RULE-GIT-002 — No Secret Commits

Never commit secrets.

---

## RULE-GIT-003 — No Temporary Debug Code

Remove unnecessary debugging artifacts before final commits.

---

## RULE-GIT-004 — Preserve History

Do not rewrite Git history unnecessarily.

---

## RULE-GIT-005 — Verify Before Push

Before pushing significant changes:

```text
Code
 ↓
Tests
 ↓
Relevant execution
 ↓
Review
 ↓
Commit
 ↓
Push
```

---

# 32. CHANGE MANAGEMENT RULES

---

## RULE-CHANGE-001 — Understand Before Changing

Before modifying a core component, inspect its dependencies.

---

## RULE-CHANGE-002 — Small Changes First

Prefer incremental changes over massive rewrites.

---

## RULE-CHANGE-003 — Verify After Each Major Change

After significant implementation:

1. Run relevant tests.
2. Run affected pipeline.
3. Inspect outputs.
4. Review unintended changes.

---

## RULE-CHANGE-004 — Update Documentation After Methodology Changes

If methodology changes, update:

- `ML_METHODOLOGY.md`
- `EXPERIMENT_PLAN.md`
- `EVALUATION_AND_ERROR_ANALYSIS.md`
- `SYSTEM_ARCHITECTURE.md`
- Other affected documents

as appropriate.

---

# 33. NO-SILENT-SCOPE-EXPANSION RULE

---

## RULE-SCOPE-001 — Do Not Expand Scope Automatically

Do not add:

- New ML algorithms
- New applications
- New frameworks
- Cloud services
- Databases
- Authentication
- Real-time infrastructure

without a documented project need.

---

## RULE-SCOPE-002 — Optional Features Must Not Delay Core Requirements

Mandatory requirements always take precedence over optional enhancements.

---

# 34. NO-OVERENGINEERING RULE

---

## RULE-OVER-001 — Do Not Build Production Infrastructure for an Internship Dataset

The project does not require:

- Kubernetes
- Microservices
- Kafka
- Distributed training
- Complex cloud orchestration

unless explicitly justified.

---

## RULE-OVER-002 — Prefer Explainable ML

Use methods that can be explained clearly in an academic/interview context.

---

# 35. APPLICATION INTEGRITY RULES

---

## RULE-UI-001 — UI Must Reflect Actual Backend Behavior

The Streamlit interface must not claim to use a model that it does not actually use.

---

## RULE-UI-002 — Metrics Must Be Real

Dashboard metrics must originate from actual data.

---

## RULE-UI-003 — Recommendations Must Be Real

Displayed recommendations must come from the actual recommendation engine.

---

## RULE-UI-004 — Errors Must Not Become Fake Data

If the backend fails, the UI must not substitute fake recommendations.

---

# 36. API INTEGRITY RULES

---

## RULE-API-INT-001 — API Must Not Bypass Model Architecture

API endpoints should use established model/recommendation modules.

---

## RULE-API-INT-002 — No Hardcoded Recommendations

Do not hardcode recommendation lists to make the API appear functional.

---

## RULE-API-INT-003 — API Must Be Tested

Endpoint behavior must be verified through actual requests/tests.

---

# 37. REPORTING RULES

---

## RULE-REPORT-001 — Report Actual Results

Every final report must use measured results.

---

## RULE-REPORT-002 — Report Methodology With Results

Metrics without methodology are insufficient.

---

## RULE-REPORT-003 — Report Limitations

Results must be interpreted alongside relevant limitations.

---

## RULE-REPORT-004 — Do Not Overstate Findings

Avoid claims such as:

```text
perfect
best
state-of-the-art
production-ready
optimal
```

unless objectively and appropriately supported.

---

# 38. AI-GENERATED CODE RULES

---

## RULE-GENAI-001 — AI Code Must Be Reviewed

AI-generated code is not automatically considered correct.

---

## RULE-GENAI-002 — AI Code Must Be Tested

Generated code must undergo the same testing standards as manually written code.

---

## RULE-GENAI-003 — AI Must Not Invent Project Facts

AI tools must not invent:

- Dataset characteristics
- Results
- Requirements
- Files
- Model performance
- User behavior

---

## RULE-GENAI-004 — AI Must Respect Repository Context

AI coding tools must inspect the actual repository before proposing modifications.

---

## RULE-GENAI-005 — AI Must Not Override Control Documents

AI-generated implementation must follow:

- `PRD.md`
- `PROJECT_SPECIFICATIONS.md`
- `RULES.md`
- Specialized technical documents

---

# 39. FINAL RESULT INTEGRITY RULES

---

## RULE-FINAL-001 — No Fabricated Numbers

Never fabricate:

- Accuracy
- Precision
- Recall
- NDCG
- Coverage
- Runtime
- User counts
- Dataset counts

---

## RULE-FINAL-002 — No Fabricated Screenshots

Screenshots must represent actual application output.

---

## RULE-FINAL-003 — No Fabricated API Responses

Demonstration responses must come from actual execution unless explicitly labeled as examples.

---

## RULE-FINAL-004 — No Fabricated User Stories

User scenarios should not be presented as real user research unless actual user research occurred.

---

# 40. FINAL QA RULES

---

## RULE-QA-001 — Full System Verification

Before final submission, verify:

```text
Data
 ↓
Preprocessing
 ↓
Models
 ↓
Recommendation Engine
 ↓
Evaluation
 ↓
API
 ↓
Streamlit
 ↓
Tests
 ↓
Documentation
```

---

## RULE-QA-002 — No Unresolved P0 Issues

Project completion requires zero unresolved critical requirements.

---

## RULE-QA-003 — P1 Issues Must Be Resolved or Explicitly Documented

A P1 requirement may only remain incomplete if the limitation is explicitly documented and accepted.

---

## RULE-QA-004 — Clean Environment Verification

Where practical, verify setup from a clean environment.

---

## RULE-QA-005 — Re-run Final Evaluation

Final reported results should come from the final verified implementation.

---

# 41. FINAL SUBMISSION RULES

Before final submission:

- [ ] Repository is clean.
- [ ] Dependencies are correct.
- [ ] Data acquisition is documented.
- [ ] No secrets exist.
- [ ] No fabricated data exists.
- [ ] No fabricated metrics exist.
- [ ] Recommendation Engine is canonical.
- [ ] API uses canonical engine.
- [ ] Streamlit uses canonical engine.
- [ ] Evaluation uses actual models.
- [ ] Precision@K is verified.
- [ ] Recall@K is verified.
- [ ] NDCG@K is verified.
- [ ] Temporal validation is legitimate or limitation is documented.
- [ ] Cold-start behavior is tested.
- [ ] User segmentation is meaningful.
- [ ] Segment evaluation is complete where applicable.
- [ ] Tests pass.
- [ ] README is accurate.
- [ ] Documentation is synchronized.
- [ ] Git history is professional.
- [ ] Final results are reproducible.

---

# 42. ABSOLUTE PROHIBITIONS

The following actions are strictly prohibited without explicit higher-level authorization:

```text
❌ Delete project files arbitrarily
❌ Introduce React
❌ Introduce Vite
❌ Introduce TypeScript
❌ Introduce Tailwind CSS
❌ Replace Streamlit unnecessarily
❌ Fabricate views
❌ Fabricate clicks
❌ Fabricate carts
❌ Fabricate purchases
❌ Fabricate timestamps
❌ Fabricate ratings
❌ Fabricate metrics
❌ Fabricate experiments
❌ Fabricate test results
❌ Fabricate screenshots
❌ Claim temporal validation without legitimate temporal data
❌ Claim cold-start support without actual candidate coverage
❌ Evaluate a different model and call it the final model
❌ Maintain conflicting recommendation logic
❌ Leak evaluation data
❌ Cherry-pick favorable results
❌ Hide failures
❌ Hide limitations
❌ Add unnecessary frameworks
❌ Add unnecessary infrastructure
❌ Hardcode recommendations
❌ Hardcode fake dashboard statistics
❌ Commit secrets
❌ Claim completion without verification
```

---

# 43. REQUIRED BEHAVIOR WHEN A REQUIREMENT CANNOT BE COMPLETED

If a requirement cannot be implemented legitimately:

```text
Identify Blocker
      ↓
Investigate
      ↓
Attempt Legitimate Resolution
      ↓
Verify Possibility
      ↓
If Resolved → Implement
      ↓
If Not Resolved
      ↓
Document Limitation
      ↓
Do NOT Fabricate Compliance
```

The project must prefer an honest limitation over an invalid implementation.

---

# 44. REQUIRED BEHAVIOR WHEN AI STUDIO ENCOUNTERS CONFLICT

If Google AI Studio encounters a conflict between:

- Existing code
- Project documents
- Its generated implementation

it must not make an autonomous destructive decision.

The correct behavior is:

```text
Stop
 ↓
Inspect
 ↓
Identify Conflict
 ↓
Preserve Existing Work
 ↓
Follow Highest-Priority Requirement
 ↓
Make Minimal Necessary Change
 ↓
Verify
```

---

# 45. REQUIRED BEHAVIOR WHEN A FILE APPEARS UNNECESSARY

If a file appears unnecessary:

```text
DO NOT DELETE
```

Instead:

1. Determine whether it is imported.
2. Search for references.
3. Determine whether documentation depends on it.
4. Determine whether future project phases depend on it.
5. Determine whether tests depend on it.
6. Record findings.
7. Only then consider controlled removal.

---

# 46. REQUIRED BEHAVIOR WHEN DATA IS MISSING

If a required dataset/file is missing:

```text
Do not generate fake replacement data.
```

Instead:

1. Identify expected source.
2. Search project documentation.
3. Verify dataset provenance.
4. Recover from legitimate source.
5. Recreate through documented processing if appropriate.
6. Validate schema.
7. Verify downstream compatibility.

---

# 47. REQUIRED BEHAVIOR WHEN TIMESTAMPS ARE MISSING

If timestamps are missing:

```text
Do not invent them.
```

Instead:

1. Identify original dataset.
2. Investigate dataset provenance.
3. Determine whether a timestamp-bearing corresponding version exists.
4. Verify compatibility.
5. Recover legitimate timestamps if possible.
6. Redesign temporal evaluation around the legitimate field.
7. If unavailable, document the limitation honestly.

---

# 48. REQUIRED BEHAVIOR WHEN METRICS ARE POOR

Poor metrics are not a reason to fabricate better results.

Correct workflow:

```text
Poor Result
    ↓
Verify Evaluation
    ↓
Verify Data
    ↓
Verify Leakage
    ↓
Analyze Model
    ↓
Perform Legitimate Experiment
    ↓
Improve if justified
    ↓
Re-evaluate
```

A poor but valid result is preferable to a strong but fabricated result.

---

# 49. REQUIRED BEHAVIOR WHEN A MODEL PERFORMS WORSE

If a sophisticated model performs worse than a baseline:

Do not hide the result.

Document:

- Baseline
- Model
- Evaluation conditions
- Metrics
- Possible explanations
- Limitations

The result itself is valuable experimental evidence.

---

# 50. REQUIRED BEHAVIOR WHEN A MODEL PERFORMS BETTER

If a model performs better:

Verify:

1. Same evaluation population.
2. Same metric definitions.
3. No leakage.
4. Correct implementation.
5. Reproducibility.
6. Statistical/experimental context.

Only then report the improvement.

---

# 51. DOCUMENT SYNCHRONIZATION RULE

If implementation changes affect methodology, update relevant control documents.

Examples:

```text
Recommendation Architecture Change
        ↓
SYSTEM_ARCHITECTURE.md
ML_METHODOLOGY.md
PROJECT_SPECIFICATIONS.md
```

```text
Evaluation Method Change
        ↓
EXPERIMENT_PLAN.md
EVALUATION_AND_ERROR_ANALYSIS.md
PROJECT_SPECIFICATIONS.md
```

```text
Data Source Change
        ↓
DATASET_AND_DATA_STRATEGY.md
PROJECT_SPECIFICATIONS.md
ML_METHODOLOGY.md
```

---

# 52. CONTROL DOCUMENT CONSISTENCY RULE

The following documents must remain mutually consistent:

```text
PRD.md
PROJECT_SPECIFICATIONS.md
DATASET_AND_DATA_STRATEGY.md
ML_METHODOLOGY.md
EXPERIMENT_PLAN.md
EVALUATION_AND_ERROR_ANALYSIS.md
SYSTEM_ARCHITECTURE.md
TASK_TRACKER.md
RULES.md
DOCUMENTATION_AND_REPORTING.md
README.md
```

No document may silently describe an outdated architecture or methodology.

---

# 53. PROJECT PHASE CONTROL RULE

Implementation must proceed through controlled phases.

```text
Phase 0
Control Documents
       ↓
Phase 1
Data Foundation
       ↓
Phase 2
Canonical Recommendation Architecture
       ↓
Phase 3
Modeling
       ↓
Phase 4
Cold Start
       ↓
Phase 5
Evaluation
       ↓
Phase 6
Segment Analysis
       ↓
Phase 7
API + Streamlit
       ↓
Phase 8
Testing / QA
       ↓
Phase 9
Documentation / GitHub
       ↓
Phase 10
Final QA
```

Do not skip a phase merely because later components appear runnable.

---

# 54. PHASE EXIT RULE

A phase is complete only when:

1. Required implementation is complete.
2. Relevant tests pass.
3. Outputs are inspected.
4. Documentation is updated.
5. No critical unresolved dependency remains.

---

# 55. FINAL PROJECT INTEGRITY MODEL

The project must maintain the following chain:

```text
REAL DATA
   ↓
VALID PROCESSING
   ↓
VALID MODEL
   ↓
VALID RECOMMENDATION
   ↓
VALID EVALUATION
   ↓
REAL RESULT
   ↓
HONEST INTERPRETATION
   ↓
ACCURATE DOCUMENTATION
```

Breaking any link invalidates the corresponding downstream claim.

---

# 56. GOLDEN RULES

The following rules summarize the entire document.

## GOLDEN-RULE-001

> **Never fabricate data.**

---

## GOLDEN-RULE-002

> **Never fabricate timestamps.**

---

## GOLDEN-RULE-003

> **Never fabricate metrics or results.**

---

## GOLDEN-RULE-004

> **Never claim a feature works without verification.**

---

## GOLDEN-RULE-005

> **Never delete existing project files without explicit authorization and dependency analysis.**

---

## GOLDEN-RULE-006

> **Never introduce unnecessary technology.**

---

## GOLDEN-RULE-007

> **Preserve valid existing implementation before rebuilding.**

---

## GOLDEN-RULE-008

> **Maintain one canonical Recommendation Engine.**

---

## GOLDEN-RULE-009

> **Evaluate the actual system being claimed.**

---

## GOLDEN-RULE-010

> **Prevent data leakage.**

---

## GOLDEN-RULE-011

> **Treat cold-start behavior as an actual technical requirement, not a documentation claim.**

---

## GOLDEN-RULE-012

> **Make user segmentation meaningful and evaluate recommendation quality by segment.**

---

## GOLDEN-RULE-013

> **Document limitations honestly.**

---

## GOLDEN-RULE-014

> **Prefer reproducibility over convenience.**

---

## GOLDEN-RULE-015

> **Prefer correctness over complexity.**

---

# 57. FINAL DEFINITION OF RULE COMPLIANCE

The project is considered **RULE-COMPLIANT** only when:

```text
No unauthorized deletion
        +
No unnecessary stack expansion
        +
No fabricated data
        +
No fabricated timestamps
        +
No fabricated metrics
        +
No evaluation leakage
        +
Canonical recommendation architecture
        +
Valid cold-start handling
        +
Meaningful segmentation
        +
Verified evaluation
        +
Verified tests
        +
Accurate documentation
        +
Reproducible execution
```

---

# 58. FINAL RULE

The most important rule of Project 3 is:

> **Build only what can be legitimately supported by the data, requirements, architecture, experiments, and evidence.**

The objective is not to make Project 3 *look* complete.

The objective is to make Project 3 **actually complete**.

The final project must therefore favor:

```text
Truth
  >
Appearance

Evidence
  >
Assumption

Correctness
  >
Complexity

Real Data
  >
Fabricated Data

Valid Evaluation
  >
Convenient Evaluation

Reproducibility
  >
One-Time Success

Preservation
  >
Unnecessary Rewriting

Unified Architecture
  >
Duplicated Logic

Honest Limitations
  >
False Compliance
```

---

# 59. FINAL AUTHORIZATION

All future implementation work for Project 3 shall be performed under these rules.

Any implementation instruction that conflicts with these rules must be reviewed against the project requirement hierarchy before execution.

No AI coding assistant, including Google AI Studio, shall be permitted to silently override these rules.

---

**END OF RULES.md**
