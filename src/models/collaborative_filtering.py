import pandas as pd
import numpy as np

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


# ============================================================
# 1. LOAD DATA
# ============================================================

INPUT_PATH = "data/processed/interactions.csv"

print("=" * 60)
print("COLLABORATIVE FILTERING")
print("=" * 60)

df = pd.read_csv(INPUT_PATH)

print(f"\nInteractions: {len(df):,}")
print(f"Users: {df['user_id'].nunique():,}")
print(f"Products: {df['product_id'].nunique():,}")


# ============================================================
# 2. CREATE INTEGER INDEXES
# ============================================================

user_ids = df["user_id"].unique()
product_ids = df["product_id"].unique()

user_to_index = {
    user_id: index
    for index, user_id in enumerate(user_ids)
}

product_to_index = {
    product_id: index
    for index, product_id in enumerate(product_ids)
}

index_to_user = {
    index: user_id
    for user_id, index in user_to_index.items()
}

index_to_product = {
    index: product_id
    for product_id, index in product_to_index.items()
}


# ============================================================
# 3. CREATE SPARSE USER-ITEM MATRIX
# ============================================================

rows = df["user_id"].map(user_to_index)
cols = df["product_id"].map(product_to_index)

user_item_matrix = csr_matrix(
    (
        df["rating"].astype(np.float32),
        (rows, cols)
    ),
    shape=(
        len(user_ids),
        len(product_ids)
    )
)

print("\n" + "=" * 60)
print("SPARSE USER-ITEM MATRIX")
print("=" * 60)

print(f"Rows (users):       {user_item_matrix.shape[0]:,}")
print(f"Columns (products): {user_item_matrix.shape[1]:,}")
print(f"Stored ratings:     {user_item_matrix.nnz:,}")


# ============================================================
# 4. CALCULATE MATRIX DENSITY
# ============================================================

total_entries = (
    user_item_matrix.shape[0]
    * user_item_matrix.shape[1]
)

density = (
    user_item_matrix.nnz / total_entries
) * 100

print(f"Matrix density: {density:.6f}%")


# ============================================================
# 5. BUILD COLLABORATIVE FILTERING MODEL
# ============================================================

print("\nBuilding nearest-neighbor model...")

model = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=6
)

model.fit(user_item_matrix)

print("Model trained successfully.")


# ============================================================
# 6. SELECT A USER
# ============================================================

target_user = user_ids[0]

target_index = user_to_index[target_user]

print("\n" + "=" * 60)
print("TARGET USER")
print("=" * 60)

print(f"User ID: {target_user}")


# ============================================================
# 7. FIND SIMILAR USERS
# ============================================================

target_vector = user_item_matrix[
    target_index
]

distances, indices = model.kneighbors(
    target_vector,
    n_neighbors=6
)

print("\nSimilar users:")

for distance, index in zip(
    distances[0][1:],
    indices[0][1:]
):

    similarity = 1 - distance

    print(
        f"User: {index_to_user[index]} | "
        f"Similarity: {similarity:.4f}"
    )


# ============================================================
# 8. COLLECT PRODUCTS FROM SIMILAR USERS
# ============================================================

similar_user_indices = indices[0][1:]

candidate_scores = {}

for similar_index in similar_user_indices:

    similarity = 1 - distances[0][
        list(indices[0]).index(similar_index)
    ]

    products_for_user = (
        user_item_matrix[similar_index]
        .indices
    )

    for product_index in products_for_user:

        # Don't recommend products the target user
        # has already interacted with.
        if user_item_matrix[
            target_index,
            product_index
        ] > 0:
            continue

        if product_index not in candidate_scores:
            candidate_scores[product_index] = 0

        candidate_scores[product_index] += similarity


# ============================================================
# 9. RANK RECOMMENDATIONS
# ============================================================

ranked_products = sorted(
    candidate_scores.items(),
    key=lambda x: x[1],
    reverse=True
)

top_n = 10

recommendations = ranked_products[:top_n]


# ============================================================
# 10. DISPLAY RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 60)
print("TOP RECOMMENDED PRODUCTS")
print("=" * 60)

product_names = (
    df[
        ["product_id", "product_name"]
    ]
    .drop_duplicates("product_id")
    .set_index("product_id")[
        "product_name"
    ]
    .to_dict()
)

for rank, (product_index, score) in enumerate(
    recommendations,
    start=1
):

    product_id = index_to_product[
        product_index
    ]

    product_name = product_names.get(
        product_id,
        "Unknown Product"
    )

    print(
        f"{rank}. {product_name[:70]} "
        f"| Product ID: {product_id} "
        f"| Score: {score:.4f}"
    )


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("COLLABORATIVE FILTERING COMPLETED")
print("=" * 60)