import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. LOAD PRODUCT DATA
# ============================================================

products = pd.read_csv("data/processed/products.csv")

print("=" * 60)
print("CONTENT-BASED RECOMMENDATION")
print("=" * 60)

print(f"Total products: {len(products)}")


# ============================================================
# 2. PREPARE PRODUCT NAMES
# ============================================================

products["product_name"] = products["product_name"].fillna("Unknown Product")

products["product_text"] = (
    products["product_name"]
    .astype(str)
    .str.lower()
)


# ============================================================
# 3. CREATE TF-IDF FEATURES
# ============================================================

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=50000
)

tfidf_matrix = vectorizer.fit_transform(products["product_text"])

print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")


# ============================================================
# 4. SELECT A PRODUCT
# ============================================================

target_index = 0

target_product = products.iloc[target_index]

print("\nTarget Product:")
print(f"Product ID   : {target_product['product_id']}")
print(f"Product Name : {target_product['product_name']}")


# ============================================================
# 5. CALCULATE CONTENT SIMILARITY
# ============================================================

target_vector = tfidf_matrix[target_index]

similarity_scores = cosine_similarity(
    target_vector,
    tfidf_matrix
).flatten()


# ============================================================
# 6. REMOVE THE TARGET PRODUCT
# ============================================================

similarity_scores[target_index] = -1


# ============================================================
# 7. GET TOP 10 SIMILAR PRODUCTS
# ============================================================

top_indices = np.argsort(similarity_scores)[::-1][:10]


# ============================================================
# 8. DISPLAY RECOMMENDATIONS
# ============================================================

print("\nTop 10 Content-Based Recommendations:")
print("-" * 60)

for rank, index in enumerate(top_indices, start=1):

    product_id = products.iloc[index]["product_id"]
    product_name = products.iloc[index]["product_name"]
    score = similarity_scores[index]

    print(
        f"{rank}. {product_name} | "
        f"Product ID: {product_id} | "
        f"Similarity: {score:.4f}"
    )


print("\n" + "=" * 60)
print("CONTENT-BASED RECOMMENDATION COMPLETED")
print("=" * 60)