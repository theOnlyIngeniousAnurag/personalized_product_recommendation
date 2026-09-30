"""
Data Preprocessing Pipeline
Project 3: Personalized Product Recommendation Model
Processes authentic Monash FIT5212 S1 2025 raw training data into interactions.csv
"""

import os
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "interactions.csv"
AUDIT_LOG_PATH = BASE_DIR / "outputs" / "reports" / "data_cleaning_audit.json"

# Create directories if they do not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_raw_data() -> tuple[pd.DataFrame, str]:
    """Loads raw training data from train.csv or train_part1 + train_part2."""
    train_full = RAW_DIR / "train.csv"
    p1 = RAW_DIR / "train_part1.csv"
    p2 = RAW_DIR / "train_part2.csv"
    
    if train_full.exists() and train_full.stat().st_size > 0:
        source_desc = "Single train.csv file"
        df = pd.read_csv(train_full)
    elif p1.exists() and p2.exists():
        source_desc = "Logical concatenation of train_part1.csv and train_part2.csv"
        df1 = pd.read_csv(p1)
        df2 = pd.read_csv(p2)
        df = pd.concat([df1, df2], ignore_index=True)
    else:
        raise FileNotFoundError(
            f"No valid raw training data found in {RAW_DIR}. Expected train.csv or (train_part1.csv + train_part2.csv)"
        )
    return df, source_desc


def preprocess():
    print("=" * 60)
    print("LOADING AUTHENTIC TRAINING DATA")
    print("=" * 60)
    
    df, source_desc = load_raw_data()
    initial_rows = len(df)
    initial_cols = len(df.columns)
    print(f"Source: {source_desc}")
    print(f"Original shape: {df.shape}")
    
    audit_data = {
        "pipeline": "src/data/preprocess_data.py",
        "source": source_desc,
        "initial_rows": initial_rows,
        "initial_cols": initial_cols,
        "initial_columns": list(df.columns)
    }

    # --------------------------------------------------
    # Select useful columns (excluding Kaggle competition row 'ID')
    # --------------------------------------------------
    required_cols = [
        "user_id",
        "product_id",
        "product_name",
        "rating",
        "votes",
        "helpful_votes"
    ]
    df = df[required_cols].copy()

    # --------------------------------------------------
    # Investigate & Remove duplicate user-product pairs
    # --------------------------------------------------
    before_dedup = len(df)
    exact_duplicates = int(df.duplicated().sum())
    user_item_duplicates = int(df.duplicated(subset=["user_id", "product_id"]).sum())
    
    df = df.drop_duplicates(subset=["user_id", "product_id"])
    after_dedup = len(df)
    dedup_removed = before_dedup - after_dedup
    
    print(f"\nExact duplicate rows: {exact_duplicates}")
    print(f"Duplicate user-product pairs removed: {dedup_removed}")
    
    audit_data["duplicates"] = {
        "exact_duplicates": exact_duplicates,
        "user_item_duplicates": user_item_duplicates,
        "rows_removed": dedup_removed
    }

    # --------------------------------------------------
    # Handle missing values
    # --------------------------------------------------
    missing_before = df.isnull().sum().to_dict()
    print("\nMissing values before cleaning:")
    for col, count in missing_before.items():
        print(f"  {col}: {count}")

    # Remove rows without mandatory fields: user, product, rating
    before_null_drop = len(df)
    df = df.dropna(subset=["user_id", "product_id", "rating"])
    after_null_drop = len(df)
    null_rows_dropped = before_null_drop - after_null_drop

    # Fill optional metadata fields deterministically
    df["product_name"] = df["product_name"].fillna("Unknown Product")
    df["votes"] = df["votes"].fillna(0)
    df["helpful_votes"] = df["helpful_votes"].fillna(0)
    
    audit_data["missing_values"] = {
        "missing_before": missing_before,
        "null_rows_dropped": null_rows_dropped
    }

    # --------------------------------------------------
    # Convert data types safely
    # --------------------------------------------------
    df["user_id"] = df["user_id"].astype(str)
    df["product_id"] = df["product_id"].astype(str)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)
    df["helpful_votes"] = pd.to_numeric(df["helpful_votes"], errors="coerce").fillna(0).astype(int)

    # --------------------------------------------------
    # Domain validation for ratings: 1 <= rating <= 5
    # --------------------------------------------------
    before_domain = len(df)
    df = df[(df["rating"] >= 1) & (df["rating"] <= 5)]
    df["rating"] = df["rating"].astype(int)
    after_domain = len(df)
    domain_invalid_dropped = before_domain - after_domain

    audit_data["rating_domain"] = {
        "domain_min": 1,
        "domain_max": 5,
        "invalid_ratings_dropped": domain_invalid_dropped
    }

    # --------------------------------------------------
    # Save processed authentic interactions
    # --------------------------------------------------
    df.to_csv(OUTPUT_PATH, index=False)
    
    final_rows = len(df)
    final_cols = len(df.columns)
    unique_users = int(df["user_id"].nunique())
    unique_products = int(df["product_id"].nunique())
    rating_distribution = df["rating"].value_counts().sort_index().to_dict()

    audit_data["final_dataset"] = {
        "output_path": str(OUTPUT_PATH.relative_to(BASE_DIR)),
        "final_rows": final_rows,
        "final_cols": final_cols,
        "unique_users": unique_users,
        "unique_products": unique_products,
        "rating_distribution": rating_distribution,
        "mean_rating": float(round(df["rating"].mean(), 4))
    }

    with open(AUDIT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2)

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Final shape: {df.shape}")
    print(f"Unique users: {unique_users:,}")
    print(f"Unique products: {unique_products:,}")
    print("\nRating distribution:")
    for r, count in rating_distribution.items():
        print(f"  Rating {r}: {count:,} ({count / final_rows * 100:.2f}%)")
    print(f"\nSaved to: {OUTPUT_PATH}")
    print(f"Audit log saved to: {AUDIT_LOG_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    preprocess()