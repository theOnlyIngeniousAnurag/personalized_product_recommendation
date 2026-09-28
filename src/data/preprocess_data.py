import pandas as pd
import os

# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_PATH = "data/raw/train.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_PATH = "data/processed/interactions.csv"

# Create processed folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("LOADING TRAINING DATA")
print("=" * 60)

df = pd.read_csv(INPUT_PATH)

print(f"Original shape: {df.shape}")

# --------------------------------------------------
# Select useful columns
# --------------------------------------------------

df = df[
    [
        "user_id",
        "product_id",
        "product_name",
        "rating",
        "votes",
        "helpful_votes"
    ]
].copy()

# --------------------------------------------------
# Remove duplicate interactions
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["user_id", "product_id"]
)

after = len(df)

print(f"\nDuplicates removed: {before - after}")

# --------------------------------------------------
# Handle missing values
# --------------------------------------------------

print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Remove rows without user, product or rating
df = df.dropna(
    subset=["user_id", "product_id", "rating"]
)

# Fill optional columns
df["product_name"] = df["product_name"].fillna("Unknown Product")
df["votes"] = df["votes"].fillna(0)
df["helpful_votes"] = df["helpful_votes"].fillna(0)

# --------------------------------------------------
# Convert data types
# --------------------------------------------------

df["user_id"] = df["user_id"].astype(str)
df["product_id"] = df["product_id"].astype(str)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["votes"] = pd.to_numeric(
    df["votes"],
    errors="coerce"
).fillna(0)

df["helpful_votes"] = pd.to_numeric(
    df["helpful_votes"],
    errors="coerce"
).fillna(0)

# Remove invalid ratings
df = df[
    (df["rating"] >= 1) &
    (df["rating"] <= 5)
]

# --------------------------------------------------
# Save processed data
# --------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# --------------------------------------------------
# Final information
# --------------------------------------------------

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETED")
print("=" * 60)

print(f"Final shape: {df.shape}")

print(f"Unique users: {df['user_id'].nunique():,}")
print(f"Unique products: {df['product_id'].nunique():,}")

print("\nRating distribution:")
print(df["rating"].value_counts().sort_index())

print(f"\nSaved to:")
print(OUTPUT_PATH)

print("=" * 60)