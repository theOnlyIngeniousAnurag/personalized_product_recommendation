import pandas as pd
import os

# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_PATH = "data/processed/products.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_PATH = "data/processed/popular_products.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("POPULARITY-BASED RECOMMENDATION MODEL")
print("=" * 60)

# --------------------------------------------------
# Load product statistics
# --------------------------------------------------

products = pd.read_csv(INPUT_PATH)

print(f"\nTotal products: {len(products):,}")

# --------------------------------------------------
# Minimum interaction requirement
# --------------------------------------------------

# Products with very few interactions can have
# unreliable average ratings.

MIN_INTERACTIONS = 5

popular = products[
    products["interaction_count"] >= MIN_INTERACTIONS
].copy()

print(
    f"Products with at least {MIN_INTERACTIONS} interactions: "
    f"{len(popular):,}"
)

# --------------------------------------------------
# Calculate popularity score
# --------------------------------------------------

popular["popularity_score"] = (
    popular["average_rating"] *
    popular["interaction_count"]
)

# --------------------------------------------------
# Sort products
# --------------------------------------------------

popular = popular.sort_values(
    by="popularity_score",
    ascending=False
)

# --------------------------------------------------
# Create recommendation rank
# --------------------------------------------------

popular["rank"] = range(1, len(popular) + 1)

# --------------------------------------------------
# Select useful columns
# --------------------------------------------------

popular = popular[
    [
        "rank",
        "product_id",
        "product_name",
        "interaction_count",
        "unique_users",
        "average_rating",
        "popularity_score"
    ]
]

# --------------------------------------------------
# Save results
# --------------------------------------------------

popular.to_csv(
    OUTPUT_PATH,
    index=False
)

# --------------------------------------------------
# Display top recommendations
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP 20 POPULAR PRODUCTS")
print("=" * 60)

print(
    popular.head(20).to_string(index=False)
)

print("\n" + "=" * 60)
print("MODEL COMPLETED")
print("=" * 60)

print(f"\nSaved to:")
print(OUTPUT_PATH)