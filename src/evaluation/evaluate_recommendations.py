import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. LOAD DATA
# ============================================================

data = pd.read_csv(
    "data/processed/interactions.csv"
)

products = pd.read_csv(
    "data/processed/products.csv"
)

print("=" * 60)
print("RECOMMENDATION SYSTEM EVALUATION")
print("=" * 60)

print(f"Total interactions: {len(data)}")


# ============================================================
# 2. CREATE USER-LEVEL HOLDOUT
# ============================================================

print("\nCreating user-level validation split...")

train_data = []
validation_data = []

for user_id, user_data in data.groupby("user_id"):

    # Users need at least 2 interactions
    if len(user_data) >= 2:

        train_part, validation_part = train_test_split(
            user_data,
            test_size=0.20,
            random_state=42
        )

        train_data.append(train_part)
        validation_data.append(validation_part)


train_data = pd.concat(train_data)
validation_data = pd.concat(validation_data)


print(f"Training interactions   : {len(train_data)}")
print(f"Validation interactions : {len(validation_data)}")


# ============================================================
# 3. DEFINE RELEVANT ITEMS
# ============================================================

# Ratings >= 4 are treated as relevant.
relevant_items = (
    validation_data[
        validation_data["rating"] >= 4
    ]
    .groupby("user_id")["product_id"]
    .apply(set)
    .to_dict()
)


# ============================================================
# 4. POPULARITY MODEL
# ============================================================

print("\nBuilding popularity recommendations...")

popular_products = (
    train_data
    .groupby("product_id")
    .agg(
        average_rating=("rating", "mean"),
        interaction_count=("rating", "count")
    )
    .reset_index()
)

popular_products["score"] = (
    popular_products["average_rating"]
    * popular_products["interaction_count"]
)

popular_products = popular_products.sort_values(
    "score",
    ascending=False
)


popular_list = (
    popular_products["product_id"]
    .head(100)
    .tolist()
)


# ============================================================
# 5. CONTENT-BASED MODEL
# ============================================================

print("Building content-based model...")

products["product_name"] = (
    products["product_name"]
    .fillna("Unknown Product")
)

products["product_text"] = (
    products["product_name"]
    .astype(str)
    .str.lower()
)

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=30000
)

tfidf_matrix = vectorizer.fit_transform(
    products["product_text"]
)

product_index = {
    product_id: index
    for index, product_id
    in enumerate(products["product_id"])
}


# ============================================================
# 6. RECOMMENDATION FUNCTION
# ============================================================

def recommend_for_user(
    user_id,
    user_history,
    k=10
):

    history = user_history[
        user_history["user_id"] == user_id
    ]

    seen = set(
        history["product_id"]
    )

    candidate_scores = {}

    # Use highest-rated products as seeds
    seeds = (
        history
        .sort_values("rating", ascending=False)
        .head(3)
    )

    for product_id in seeds["product_id"]:

        if product_id not in product_index:
            continue

        index = product_index[product_id]

        similarities = cosine_similarity(
            tfidf_matrix[index],
            tfidf_matrix
        ).flatten()

        top_indices = np.argpartition(
            similarities,
            -30
        )[-30:]

        for candidate_index in top_indices:

            candidate_id = products.iloc[
                candidate_index
            ]["product_id"]

            if candidate_id in seen:
                continue

            score = similarities[
                candidate_index
            ]

            if (
                candidate_id not in candidate_scores
                or score > candidate_scores[candidate_id]
            ):
                candidate_scores[candidate_id] = score

    # Add popularity candidates
    for rank, product_id in enumerate(
        popular_list
    ):

        if product_id not in seen:

            popularity_score = (
                1 - rank / len(popular_list)
            )

            if product_id not in candidate_scores:

                candidate_scores[
                    product_id
                ] = 0.2 * popularity_score

    recommendations = sorted(
        candidate_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        product_id
        for product_id, score
        in recommendations[:k]
    ]


# ============================================================
# 7. EVALUATION METRICS
# ============================================================

def precision_at_k(
    recommended,
    relevant,
    k
):

    recommended = recommended[:k]

    if len(recommended) == 0:
        return 0.0

    hits = len(
        set(recommended) & relevant
    )

    return hits / k


def recall_at_k(
    recommended,
    relevant,
    k
):

    recommended = recommended[:k]

    if len(relevant) == 0:
        return 0.0

    hits = len(
        set(recommended) & relevant
    )

    return hits / len(relevant)


def ndcg_at_k(
    recommended,
    relevant,
    k
):

    recommended = recommended[:k]

    dcg = 0.0

    for rank, product_id in enumerate(
        recommended,
        start=1
    ):

        if product_id in relevant:

            dcg += 1 / np.log2(
                rank + 1
            )

    ideal_hits = min(
        len(relevant),
        k
    )

    if ideal_hits == 0:
        return 0.0

    idcg = sum(
        1 / np.log2(rank + 1)
        for rank in range(
            1,
            ideal_hits + 1
        )
    )

    return dcg / idcg


# ============================================================
# 8. EVALUATE USERS
# ============================================================

print("\nEvaluating recommendations...")

precision_scores = []
recall_scores = []
ndcg_scores = []

evaluated_users = 0

for user_id, relevant in relevant_items.items():

    recommendations = recommend_for_user(
        user_id,
        train_data,
        k=10
    )

    precision_scores.append(
        precision_at_k(
            recommendations,
            relevant,
            10
        )
    )

    recall_scores.append(
        recall_at_k(
            recommendations,
            relevant,
            10
        )
    )

    ndcg_scores.append(
        ndcg_at_k(
            recommendations,
            relevant,
            10
        )
    )

    evaluated_users += 1

    # Limit evaluation to keep runtime manageable
    if evaluated_users >= 1000:
        break


# ============================================================
# 9. FINAL RESULTS
# ============================================================

precision = np.mean(
    precision_scores
)

recall = np.mean(
    recall_scores
)

ndcg = np.mean(
    ndcg_scores
)


print("\n" + "=" * 60)
print("EVALUATION RESULTS")
print("=" * 60)

print(f"Users evaluated : {evaluated_users}")
print(f"Precision@10    : {precision:.4f}")
print(f"Recall@10       : {recall:.4f}")
print(f"NDCG@10         : {ndcg:.4f}")

print("=" * 60)
print("EVALUATION COMPLETED")
print("=" * 60)