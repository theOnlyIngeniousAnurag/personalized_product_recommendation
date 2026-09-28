import pandas as pd
import numpy as np

from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


# ============================================================
# 1. LOAD DATA
# ============================================================

INPUT_PATH = "data/processed/interactions.csv"

print("=" * 60)
print("MATRIX FACTORIZATION")
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

print(f"Rows:    {user_item_matrix.shape[0]:,}")
print(f"Columns: {user_item_matrix.shape[1]:,}")
print(f"Ratings: {user_item_matrix.nnz:,}")


# ============================================================
# 4. MATRIX FACTORIZATION USING SVD
# ============================================================

N_COMPONENTS = 20

print("\n" + "=" * 60)
print("TRAINING SVD MODEL")
print("=" * 60)

svd = TruncatedSVD(
    n_components=N_COMPONENTS,
    random_state=42
)

user_factors = svd.fit_transform(
    user_item_matrix
)

product_factors = svd.components_

print(f"\nLatent factors: {N_COMPONENTS}")

print(
    f"Explained variance ratio: "
    f"{svd.explained_variance_ratio_.sum():.4f}"
)


# ============================================================
# 5. SELECT A USER
# ============================================================

target_user = user_ids[0]

target_user_index = user_to_index[
    target_user
]

print("\n" + "=" * 60)
print("TARGET USER")
print("=" * 60)

print(f"User ID: {target_user}")


# ============================================================
# 6. PREDICT USER-PRODUCT SCORES
# ============================================================

user_vector = user_factors[
    target_user_index
]

predicted_scores = (
    user_vector @ product_factors
)


# ============================================================
# 7. REMOVE ALREADY INTERACTED PRODUCTS
# ============================================================

already_interacted = set(
    user_item_matrix[
        target_user_index
    ].indices
)

predicted_scores[
    list(already_interacted)
] = -np.inf


# ============================================================
# 8. GET TOP RECOMMENDATIONS
# ============================================================

top_n = 10

top_indices = np.argpartition(
    predicted_scores,
    -top_n
)[-top_n:]

top_indices = top_indices[
    np.argsort(
        predicted_scores[top_indices]
    )[::-1]
]


# ============================================================
# 9. PRODUCT NAMES
# ============================================================

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


# ============================================================
# 10. DISPLAY RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 MATRIX FACTORIZATION RECOMMENDATIONS")
print("=" * 60)

for rank, product_index in enumerate(
    top_indices,
    start=1
):

    product_id = index_to_product[
        product_index
    ]

    product_name = product_names.get(
        product_id,
        "Unknown Product"
    )

    score = predicted_scores[
        product_index
    ]

    print(
        f"{rank}. {product_name[:70]} "
        f"| Product ID: {product_id} "
        f"| Score: {score:.4f}"
    )


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("MATRIX FACTORIZATION COMPLETED")
print("=" * 60)