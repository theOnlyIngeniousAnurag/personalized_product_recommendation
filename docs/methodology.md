# Recommendation System Methodology

## 1. Introduction

The Personalized Product Recommendation System is designed to recommend products to users based on their previous interactions with products and information available about those products.

The methodology combines multiple recommendation approaches so that the system can provide recommendations using different sources of information.

The main approaches implemented are:

* Popularity-based recommendation
* Collaborative filtering
* Matrix factorization
* Content-based recommendation
* Hybrid recommendation

The system also includes offline evaluation using Precision@10, Recall@10, and NDCG@10.

---

## 2. Dataset

The project uses the FIT5212 S1 2025 Recommender System Challenge dataset.

The available training data contains user-product interactions with explicit ratings from 1 to 5.

The main fields used by the project include:

* `user_id`
* `product_id`
* `product_name`
* `rating`
* `votes`
* `helpful_votes`

The training dataset contains 745,889 interaction records, while the test dataset contains 223,553 records.

---

## 3. Data Preprocessing

The raw interaction data is processed before being used by the recommendation models.

The preprocessing procedure includes:

1. Loading the training dataset.
2. Selecting the required columns.
3. Removing duplicate user-product interactions.
4. Removing missing user, product, and rating values.
5. Filling missing textual and voting information where appropriate.
6. Converting user and product identifiers into consistent string representations.
7. Converting ratings into numeric values.
8. Keeping valid ratings between 1 and 5.
9. Saving the processed interaction data.

The resulting processed dataset is stored in:

`data/processed/interactions.csv`

---

## 4. User and Product Entities

Separate user and product information is generated from the processed interaction data.

For users, the system calculates information such as:

* number of interactions
* number of unique products
* average rating
* total votes

For products, the system calculates:

* number of interactions
* number of unique users
* average rating
* total votes

These statistics are used by the recommendation and analysis components.

---

## 5. Popularity-Based Recommendation

The popularity-based model provides a baseline recommendation method.

Products with a minimum number of interactions are considered.

The popularity score is calculated using:

`Popularity Score = Average Rating × Interaction Count`

Products are then ranked according to this score.

This approach is useful as a baseline because it does not require personalized user information.

It can also be used as a fallback for users for whom insufficient interaction history is available.

---

## 6. Collaborative Filtering

The collaborative filtering component uses user-product interaction information.

A sparse user-item matrix is constructed where:

* rows represent users
* columns represent products
* matrix values represent ratings

User similarity is calculated using cosine similarity.

Users with similar interaction patterns can therefore be identified.

Products interacted with by similar users can then be considered as candidate recommendations.

---

## 7. Matrix Factorization

Matrix factorization is implemented using Truncated Singular Value Decomposition (SVD).

The user-item interaction matrix is transformed into a lower-dimensional latent representation.

The method produces:

* user latent factors
* product latent factors

These latent representations are used to estimate relationships between users and products.

The use of a lower-dimensional representation also provides a way to work with the sparse interaction matrix more efficiently.

---

## 8. Content-Based Recommendation

The content-based component uses product names as product metadata.

Product names are transformed into numerical representations using Term Frequency-Inverse Document Frequency (TF-IDF).

The TF-IDF representation allows the system to identify products with similar textual characteristics.

Cosine similarity is then used to calculate similarity between product representations.

Products similar to those previously rated highly by the user can therefore be considered for recommendation.

---

## 9. Hybrid Recommendation

The hybrid recommendation approach combines multiple recommendation signals.

The implemented hybrid model combines:

* collaborative recommendation score
* content similarity score
* popularity score

The final score is calculated using weighted components:

`Hybrid Score = 0.50 × Collaborative Score
              \+ 0.30 × Content Score
              \+ 0.20 × Popularity Score`

The resulting candidates are ranked according to the hybrid score.

This approach allows the recommendation system to use both user behaviour and product information.

---

## 10. Recommendation Process

For an existing user, the recommendation process consists of the following steps:

1. Identify the user's historical interactions.
2. Identify highly rated products from the user's history.
3. Generate candidate products.
4. Calculate collaborative recommendation scores.
5. Calculate content-based similarity scores.
6. Calculate popularity scores.
7. Normalize the recommendation signals where required.
8. Combine the signals using the hybrid scoring formula.
9. Remove products already interacted with by the user.
10. Rank the remaining products.
11. Return the requested number of recommendations.

For a new user with no interaction history, the system uses a popularity-based fallback.

---

## 11. Evaluation Methodology

The recommendation system is evaluated using top-K recommendation metrics.

The main evaluation metrics are:

### Precision@10

Measures the proportion of recommended products that are relevant.

`Precision@K = Relevant Recommended Items / K`

### Recall@10

Measures the proportion of relevant products that are successfully recommended.

`Recall@K = Relevant Recommended Items / Total Relevant Items`

### NDCG@10

Measures both recommendation relevance and ranking position.

`NDCG@K = DCG@K / IDCG@K`

Ratings of 4 or 5 are treated as relevant interactions during top-K evaluation.

---

## 12. Validation Strategy

The dataset does not contain a timestamp field.

Therefore, a true chronological time-based split cannot be performed using the available data without introducing information that is not present in the original dataset.

Instead, the recommendation evaluation uses a user-level holdout strategy.

Part of the user's interactions is used for generating recommendations, while held-out interactions are used to evaluate whether relevant products are retrieved.

---

## 13. User Segment Analysis

Users are divided into activity-based segments according to their number of interactions.

The implemented segments are:

* Low Activity: fewer than 3 interactions
* Medium Activity: 3 to 10 interactions
* High Activity: more than 10 interactions

The segments are analyzed using user activity and rating statistics.

This analysis helps examine how recommendation behaviour varies across users with different levels of interaction history.

---

## 14. Application Layer

The project provides a Streamlit interface for interacting with the recommendation system.

The application allows users to:

* enter a user ID
* select the number of recommendations
* view recommended products
* view user history statistics
* inspect rating distributions
* analyze user activity segments
* view popular products
* visualize recommendation scores

---

## 15. API Layer

A FastAPI-based API is also included.

The API provides programmatic access to the recommendation system.

The main endpoint is:

`GET /recommend/{user_id}`

The API can therefore be used by other applications or interfaces to request product recommendations.

FastAPI automatically provides interactive API documentation through Swagger UI at `/docs` and an OpenAPI schema at `/openapi.json`. [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/first-steps/)

---

## 16. Limitations

The methodology has several limitations.

First, the dataset does not contain timestamps, so chronological evaluation cannot be performed.

Second, the available interactions are primarily explicit ratings rather than separate event types such as views, clicks, carts, and purchases.

Third, product metadata is limited in the available dataset. Therefore, the content-based component primarily uses product names.

Finally, offline recommendation metrics may not completely represent user behaviour in a real-world production environment.

---

## 17. Overall Methodology

The complete methodology can be summarized as:

`Raw Dataset`
→ `Data Preprocessing`
→ `User/Product Construction`
→ `Recommendation Models`
→ `Hybrid Recommendation`
→ `Offline Evaluation`
→ `Streamlit Application / FastAPI`
→ `Personalized Product Recommendations`
