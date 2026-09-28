import pandas as pd
import os

INPUT_PATH = "data/processed/interactions.csv"

USERS_PATH = "data/processed/users.csv"
PRODUCTS_PATH = "data/processed/products.csv"

print("=" * 60)
print("LOADING PROCESSED INTERACTIONS")
print("=" * 60)

df = pd.read_csv(INPUT_PATH)

# --------------------------------------------------
# Create user statistics
# --------------------------------------------------

print("\nCreating user statistics...")

users = (
    df.groupby("user_id")
    .agg(
        interaction_count=("product_id", "count"),
        unique_products=("product_id", "nunique"),
        average_rating=("rating", "mean"),
        total_votes=("votes", "sum")
    )
    .reset_index()
)

users["average_rating"] = users["average_rating"].round(2)

# --------------------------------------------------
# Create product statistics
# --------------------------------------------------

print("Creating product statistics...")

products = (
    df.groupby("product_id")
    .agg(
        product_name=("product_name", "first"),
        interaction_count=("user_id", "count"),
        unique_users=("user_id", "nunique"),
        average_rating=("rating", "mean"),
        total_votes=("votes", "sum")
    )
    .reset_index()
)

products["average_rating"] = products["average_rating"].round(2)

# --------------------------------------------------
# Save
# --------------------------------------------------

users.to_csv(USERS_PATH, index=False)
products.to_csv(PRODUCTS_PATH, index=False)

# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n" + "=" * 60)
print("ENTITY CREATION COMPLETED")
print("=" * 60)

print(f"\nUsers: {len(users):,}")
print(f"Products: {len(products):,}")

print(f"\nSaved:")
print(USERS_PATH)
print(PRODUCTS_PATH)

print("\nTop 10 products by interactions:")

print(
    products
    .sort_values("interaction_count", ascending=False)
    [["product_id", "product_name", "interaction_count", "average_rating"]]
    .head(10)
    .to_string(index=False)
)

print("\n" + "=" * 60)