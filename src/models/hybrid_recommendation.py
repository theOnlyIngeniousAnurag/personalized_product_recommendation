import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


# ============================================================
# 1. LOAD DATA
# ============================================================

interactions = pd.read_csv(
    "data/processed/interactions.csv"
)

products = pd.read_csv(
    "data/processed/products.csv"
)

popular_products = pd.read_csv(
    "data/processed/popular_products.csv"
)

print("=" * 60)
print("HYBRID RECOMMENDATION MODEL")
print("=" * 60)


# ============================================================
# 2. SELECT TARGET USER
# ============================================================

target_user = interactions["user_id"].iloc[0]

print(f"\nTarget User: {target_user}")


# ============================================================
# 3. USER-ITEM MATRIX
# ============================================================

user_ids = interactions["user_id"].unique()
product_ids = interactions["product_id"].unique()

user_to_index = {
    user_id: i
    for i, user_id in enumerate(user_ids)
}

product_to_index = {
    product_id: i
    for i, product_id in enumerate(product_ids)
}

rows = interactions["user_id"].map(user_to_index)
cols = interactions["product_id"].map(product_to_index)

ratings = interactions["rating"].astype(float)

user_item_matrix = csr_matrix(
    (ratings, (rows, cols)),
    shape=(len(user_ids), len(product_ids))
)


# ============================================================
# 4. COLLABORATIVE FILTERING
# ============================================================

print("\nGenerating collaborative recommendations...")

knn = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=6
)

knn.fit(user_item_matrix)

target_index = user_to_index[target_user]

distances, indices = knn.kneighbors(
    user_item_matrix[target_index],
    n_neighbors=6
)

similarities = 1 - distances.flatten()


# ============================================================
# 5. COLLABORATIVE SCORES
# ============================================================

collaborative_scores = {}

for similarity, similar_index in zip(
    similarities[1:],
    indices.flatten()[1:]
):

    similar_user = user_ids[similar_index]

    user_products = interactions[
        interactions["user_id"] == similar_user
    ]

    for _, row in user_products.iterrows():

        product_id = row["product_id"]

        if product_id not in collaborative_scores:
            collaborative_scores[product_id] = 0

        collaborative_scores[product_id] += (
            similarity * row["rating"]
        )


# ============================================================
# 6. USER HISTORY
# ============================================================

user_history = interactions[
    interactions["user_id"] == target_user
]

seen_products = set(
    user_history["product_id"]
)

print(
    f"Products already interacted with: "
    f"{len(seen_products)}"
)


# ============================================================
# 7. CONTENT-BASED MODEL
# ============================================================

print("\nGenerating content-based recommendations...")

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


# ============================================================
# 8. ONLY USE A FEW USER HISTORY PRODUCTS
# ============================================================

# Use the user's highest-rated products as the content seed.
seed_products = (
    user_history
    .sort_values("rating", ascending=False)
    .head(5)
)

content_scores = {}


for product_id in seed_products["product_id"]:

    matching = products.index[
        products["product_id"] == product_id
    ]

    if len(matching) == 0:
        continue

    product_index = matching[0]

    similarity = cosine_similarity(
        tfidf_matrix[product_index],
        tfidf_matrix
    ).flatten()

    # Only keep the best 50 candidates
    top_indices = np.argpartition(
        similarity,
        -50
    )[-50:]

    for index in top_indices:

        candidate_id = products.iloc[index]["product_id"]

        if candidate_id in seen_products:
            continue

        score = similarity[index]

        if candidate_id not in content_scores:
            content_scores[candidate_id] = score
        else:
            content_scores[candidate_id] = max(
                content_scores[candidate_id],
                score
            )


# ============================================================
# 9. POPULARITY SCORES
# ============================================================

print("\nLoading popularity scores...")

popularity_scores = {}

for _, row in popular_products.head(1000).iterrows():

    product_id = row["product_id"]

    if product_id not in seen_products:

        popularity_scores[product_id] = (
            row["popularity_score"]
        )


# ============================================================
# 10. NORMALIZATION FUNCTION
# ============================================================

def normalize_scores(scores):

    if not scores:
        return {}

    values = np.array(
        list(scores.values()),
        dtype=float
    )

    minimum = values.min()
    maximum = values.max()

    if maximum == minimum:

        return {
            key: 1.0
            for key in scores
        }

    return {
        key: (value - minimum) /
             (maximum - minimum)
        for key, value in scores.items()
    }


collaborative_scores = normalize_scores(
    collaborative_scores
)

content_scores = normalize_scores(
    content_scores
)

popularity_scores = normalize_scores(
    popularity_scores
)


# ============================================================
# 11. COMBINE MODELS
# ============================================================

print("\nCombining recommendation scores...")

hybrid_scores = {}

all_products = set()

all_products.update(
    collaborative_scores.keys()
)

all_products.update(
    content_scores.keys()
)

all_products.update(
    popularity_scores.keys()
)


for product_id in all_products:

    collaborative = collaborative_scores.get(
        product_id,
        0
    )

    content = content_scores.get(
        product_id,
        0
    )

    popularity = popularity_scores.get(
        product_id,
        0
    )

    hybrid_score = (
        0.50 * collaborative
        + 0.30 * content
        + 0.20 * popularity
    )

    hybrid_scores[product_id] = hybrid_score


# ============================================================
# 12. TOP 10 RECOMMENDATIONS
# ============================================================

top_recommendations = sorted(
    hybrid_scores.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]


# ============================================================
# 13. DISPLAY RESULTS
# ============================================================

print("\nTop 10 Hybrid Recommendations:")
print("-" * 60)

for rank, (product_id, score) in enumerate(
    top_recommendations,
    start=1
):

    product_rows = products[
        products["product_id"] == product_id
    ]

    if len(product_rows) > 0:

        product_name = product_rows.iloc[0][
            "product_name"
        ]

    else:

        product_name = "Unknown Product"

    print(
        f"{rank}. {product_name} | "
        f"Product ID: {product_id} | "
        f"Hybrid Score: {score:.4f}"
    )


print("\n" + "=" * 60)
print("HYBRID RECOMMENDATION COMPLETED")
print("=" * 60)