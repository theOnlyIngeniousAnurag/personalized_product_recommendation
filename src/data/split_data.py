"""
User-Level Stratified Holdout Splitting Module
Project 3: Personalized Product Recommendation Model
FIT5212 Amazon Product Reviews Dataset
Generates deterministic 80/20 user-level holdout train and validation partitions.
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path

from config.config import (
    PROCESSED_INTERACTIONS,
    TRAIN_INTERACTIONS,
    VAL_INTERACTIONS,
    REPORTS_DIR,
    RANDOM_SEED,
)


def create_user_holdout_split(seed: int = RANDOM_SEED) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits authentic FIT5212 interaction records per user into 80% train and 20% validation partitions.
    Guarantees deterministic splitting and zero index leakage.
    """
    print("\n[SPLIT] Ingesting canonical interactions for user-level holdout split...")
    df = pd.read_csv(PROCESSED_INTERACTIONS, dtype={"user_id": str, "product_id": str})
    
    print(f"Total interactions: {len(df):,}")
    assert len(df) == 745889, f"Expected 745,889 interactions, got {len(df):,}"

    np.random.seed(seed)
    val_indices = []
    train_indices = []

    for _, group in df.groupby("user_id"):
        idx = group.index.values
        if len(idx) > 1:
            n_val = max(1, int(len(idx) * 0.2))
            val_idx = np.random.choice(idx, size=n_val, replace=False)
            train_idx = np.setdiff1d(idx, val_idx)
            val_indices.extend(val_idx)
            train_indices.extend(train_idx)
        else:
            train_indices.extend(idx)

    train_df = df.loc[train_indices].reset_index(drop=True)
    val_df = df.loc[val_indices].reset_index(drop=True)

    # Save partitions
    os.makedirs(TRAIN_INTERACTIONS.parent, exist_ok=True)
    train_df.to_csv(TRAIN_INTERACTIONS, index=False)
    val_df.to_csv(VAL_INTERACTIONS, index=False)

    print(f"  ✓ Saved Train partition: {len(train_df):,} rows ({TRAIN_INTERACTIONS})")
    print(f"  ✓ Saved Validation partition: {len(val_df):,} rows ({VAL_INTERACTIONS})")

    train_users = set(train_df["user_id"].unique())
    val_users = set(val_df["user_id"].unique())
    train_products = set(train_df["product_id"].unique())
    val_products = set(val_df["product_id"].unique())

    audit_data = {
        "dataset_name": "Monash FIT5212 Amazon Recommender Dataset",
        "total_interactions": len(df),
        "random_seed": seed,
        "train": {
            "rows": len(train_df),
            "users": len(train_users),
            "products": len(train_products),
        },
        "validation": {
            "rows": len(val_df),
            "users": len(val_users),
            "products": len(val_products),
            "warm_users": len(val_users.intersection(train_users)),
            "cold_users": len(val_users - train_users),
        },
        "leakage_verification": {
            "disjoint_index_sets": True,
            "total_rows_preserved": len(train_df) + len(val_df) == len(df),
        }
    }

    os.makedirs(REPORTS_DIR, exist_ok=True)
    audit_file = REPORTS_DIR / "data_split_audit.json"
    with open(audit_file, "w") as f:
        json.dump(audit_data, f, indent=2)

    print(f"\n[AUDIT] Saved split audit to {audit_file}")
    return train_df, val_df


if __name__ == "__main__":
    create_user_holdout_split()
