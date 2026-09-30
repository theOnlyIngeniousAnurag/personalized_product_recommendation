"""
Train / Validation / Test Data Foundation Split Module
Project 3: Personalized Product Recommendation Model
Strategy: Path B — User-Level Stratified Holdout (Non-Temporal)
"""

import os
import json
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
INTERIM_DIR = BASE_DIR / "data" / "interim"
AUDIT_DIR = BASE_DIR / "outputs" / "reports"


def split_user_holdout(
    interactions_df: pd.DataFrame,
    test_ratio: float = 0.2,
    min_interactions: int = 5,
    random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Performs a deterministic, reproducible user-level holdout split.
    
    For users with at least `min_interactions`, `test_ratio` of their
    interactions are held out for ranking evaluation. Users with fewer
    than `min_interactions` have all their interactions placed in the
    training set to avoid unrepresentative zero/single-item evaluation sets.
    
    Leakage Controls:
    - Train and validation sets are strictly disjoint (intersection = empty).
    - Ratings of 4 or 5 in the validation set serve as ground-truth relevant items.
    """
    rng = np.random.RandomState(random_state)
    
    train_indices = []
    val_indices = []
    
    user_counts = interactions_df.groupby("user_id").size()
    eligible_users = set(user_counts[user_counts >= min_interactions].index)
    
    for user_id, group in interactions_df.groupby("user_id"):
        indices = group.index.tolist()
        if user_id in eligible_users:
            rng.shuffle(indices)
            n_val = max(1, int(len(indices) * test_ratio))
            val_indices.extend(indices[:n_val])
            train_indices.extend(indices[n_val:])
        else:
            train_indices.extend(indices)
            
    train_df = interactions_df.loc[train_indices].copy()
    val_df = interactions_df.loc[val_indices].copy()
    
    # Leakage check: disjoint indices
    assert len(set(train_indices).intersection(set(val_indices))) == 0, "Leakage detected: overlapping indices"
    
    # Compute split metadata
    stats = {
        "split_strategy": "Path B: User-Level Stratified Holdout (Non-Temporal)",
        "random_state": random_state,
        "test_ratio": test_ratio,
        "min_interactions_threshold": min_interactions,
        "total_interactions": len(interactions_df),
        "train_interactions": len(train_df),
        "val_interactions": len(val_df),
        "unique_users_total": int(interactions_df["user_id"].nunique()),
        "unique_users_train": int(train_df["user_id"].nunique()),
        "eligible_eval_users": int(val_df["user_id"].nunique()),
        "unique_products_train": int(train_df["product_id"].nunique()),
        "unique_products_val": int(val_df["product_id"].nunique()),
        "new_products_in_val": int(len(set(val_df["product_id"]) - set(train_df["product_id"]))),
        "val_relevant_items_count": int((val_df["rating"] >= 4).sum()),
        "val_relevant_ratio": float(round((val_df["rating"] >= 4).mean(), 4))
    }
    
    return train_df, val_df, stats


def execute_split():
    input_path = PROCESSED_DIR / "interactions.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Missing processed interactions: {input_path}")
        
    print("=" * 60)
    print("EXECUTING PATH B USER-LEVEL HOLDOUT SPLIT")
    print("=" * 60)
    
    interactions = pd.read_csv(input_path)
    train_df, val_df, stats = split_user_holdout(interactions)
    
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    
    train_out = INTERIM_DIR / "train_interactions.csv"
    val_out = INTERIM_DIR / "val_interactions.csv"
    audit_out = AUDIT_DIR / "data_split_audit.json"
    
    train_df.to_csv(train_out, index=False)
    val_df.to_csv(val_out, index=False)
    
    with open(audit_out, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        
    print(f"Total interactions:       {stats['total_interactions']:,}")
    print(f"Train split interactions: {stats['train_interactions']:,} ({stats['train_interactions'] / stats['total_interactions'] * 100:.1f}%)")
    print(f"Val split interactions:   {stats['val_interactions']:,} ({stats['val_interactions'] / stats['total_interactions'] * 100:.1f}%)")
    print(f"Eligible eval users:      {stats['eligible_eval_users']:,} / {stats['unique_users_total']:,}")
    print(f"Val ground-truth items:   {stats['val_relevant_items_count']:,} (Ratings >= 4, {stats['val_relevant_ratio']*100:.1f}%)")
    print(f"Saved train interactions: {train_out}")
    print(f"Saved val interactions:   {val_out}")
    print(f"Saved split audit log:    {audit_out}")
    print("=" * 60)


if __name__ == "__main__":
    execute_split()
