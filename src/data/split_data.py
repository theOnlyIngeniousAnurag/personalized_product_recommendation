"""
Temporal Splitting Module
Implements leakage-safe chronological train/validation/test splits based on authentic timestamps.
"""

import os
import json
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
from config.config import (
    PROCESSED_INTERACTIONS,
    TRAIN_INTERACTIONS,
    VAL_INTERACTIONS,
    TEST_INTERACTIONS,
    REPORTS_DIR,
)

def create_temporal_split(val_days: int = 14, test_days: int = 14):
    """
    Split interactions chronologically into Train, Validation, and Test partitions.
    
    Parameters:
    -----------
    val_days : int
        Duration in days for the validation period immediately preceding the test period.
    test_days : int
        Duration in days for the test period at the end of the observation window.
    """
    print("\n[SPLIT] Ingesting canonical interactions for temporal splitting...")
    df = pd.read_csv(PROCESSED_INTERACTIONS)
    
    # Verify chronological sorting
    if not df["timestamp"].is_monotonic_increasing:
        df.sort_values(by="timestamp", inplace=True)
        df.reset_index(drop=True, inplace=True)

    min_ts = df["timestamp"].min()
    max_ts = df["timestamp"].max()

    # Calculate cutoff timestamps in milliseconds
    ms_per_day = 86400 * 1000
    test_cutoff_ts = max_ts - (test_days * ms_per_day)
    val_cutoff_ts = test_cutoff_ts - (val_days * ms_per_day)

    train_df = df[df["timestamp"] < val_cutoff_ts].copy()
    val_df = df[(df["timestamp"] >= val_cutoff_ts) & (df["timestamp"] < test_cutoff_ts)].copy()
    test_df = df[df["timestamp"] >= test_cutoff_ts].copy()

    # Save partitions
    os.makedirs(TRAIN_INTERACTIONS.parent, exist_ok=True)
    train_df.to_csv(TRAIN_INTERACTIONS, index=False)
    val_df.to_csv(VAL_INTERACTIONS, index=False)
    test_df.to_csv(TEST_INTERACTIONS, index=False)

    print(f"  ✓ Train Partition: {len(train_df):,} rows")
    print(f"  ✓ Validation Partition: {len(val_df):,} rows")
    print(f"  ✓ Test Partition: {len(test_df):,} rows")

    # Analyze User and Item Overlap (Warm vs Cold)
    train_users = set(train_df["user_id"].unique())
    val_users = set(val_df["user_id"].unique())
    test_users = set(test_df["user_id"].unique())

    train_items = set(train_df["item_id"].unique())
    val_items = set(val_df["item_id"].unique())
    test_items = set(test_df["item_id"].unique())

    val_warm_users = len(val_users.intersection(train_users))
    val_cold_users = len(val_users - train_users)
    test_warm_users = len(test_users.intersection(train_users))
    test_cold_users = len(test_users - train_users)

    val_warm_items = len(val_items.intersection(train_items))
    val_cold_items = len(val_items - train_items)
    test_warm_items = len(test_items.intersection(train_items))
    test_cold_items = len(test_items - train_items)

    # Leakage Verifications:
    train_max_ts = int(train_df["timestamp"].max())
    val_min_ts = int(val_df["timestamp"].min())
    val_max_ts = int(val_df["timestamp"].max())
    test_min_ts = int(test_df["timestamp"].min())
    test_max_ts = int(test_df["timestamp"].max())

    rule_a_pass = train_max_ts < val_min_ts
    rule_b_pass = val_max_ts < test_min_ts

    split_audit = {
        "dataset_min_ts": int(min_ts),
        "dataset_max_ts": int(max_ts),
        "val_cutoff_ts": int(val_cutoff_ts),
        "test_cutoff_ts": int(test_cutoff_ts),
        "train": {
            "rows": len(train_df),
            "users": len(train_users),
            "items": len(train_items),
            "min_ts": train_max_ts if len(train_df) == 0 else int(train_df["timestamp"].min()),
            "max_ts": train_max_ts,
            "min_dt": datetime.fromtimestamp(int(train_df["timestamp"].min()) / 1000.0, tz=timezone.utc).isoformat(),
            "max_dt": datetime.fromtimestamp(train_max_ts / 1000.0, tz=timezone.utc).isoformat(),
        },
        "validation": {
            "rows": len(val_df),
            "users": len(val_users),
            "items": len(val_items),
            "min_ts": val_min_ts,
            "max_ts": val_max_ts,
            "min_dt": datetime.fromtimestamp(val_min_ts / 1000.0, tz=timezone.utc).isoformat(),
            "max_dt": datetime.fromtimestamp(val_max_ts / 1000.0, tz=timezone.utc).isoformat(),
            "warm_users": val_warm_users,
            "cold_users": val_cold_users,
            "warm_items": val_warm_items,
            "cold_items": val_cold_items,
        },
        "test": {
            "rows": len(test_df),
            "users": len(test_users),
            "items": len(test_items),
            "min_ts": test_min_ts,
            "max_ts": test_max_ts,
            "min_dt": datetime.fromtimestamp(test_min_ts / 1000.0, tz=timezone.utc).isoformat(),
            "max_dt": datetime.fromtimestamp(test_max_ts / 1000.0, tz=timezone.utc).isoformat(),
            "warm_users": test_warm_users,
            "cold_users": test_cold_users,
            "warm_items": test_warm_items,
            "cold_items": test_cold_items,
        },
        "leakage_verification": {
            "rule_a_train_before_val": bool(rule_a_pass),
            "rule_b_val_before_test": bool(rule_b_pass),
            "strict_chronological_ordering": bool(rule_a_pass and rule_b_pass),
        }
    }

    os.makedirs(REPORTS_DIR, exist_ok=True)
    audit_file = REPORTS_DIR / "data_split_audit.json"
    with open(audit_file, "w") as f:
        json.dump(split_audit, f, indent=2)

    print(f"\n[AUDIT] Saved split audit to {audit_file}")
    print(f"  ✓ Rule A (Train < Val): {'PASS' if rule_a_pass else 'FAIL'}")
    print(f"  ✓ Rule B (Val < Test): {'PASS' if rule_b_pass else 'FAIL'}")
    return split_audit

if __name__ == "__main__":
    create_temporal_split()
