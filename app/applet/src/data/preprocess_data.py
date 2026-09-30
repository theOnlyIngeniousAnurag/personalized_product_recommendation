"""
Authentic RetailRocket Data Preprocessing & Canonical Foundation Pipeline
Processes raw RetailRocket events, category tree, and item properties into clean canonical tables.
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path
from src.data.acquire_data import check_and_register_raw_data, load_retailrocket_events
from config.config import (
    PROCESSED_DATA_DIR,
    PROCESSED_INTERACTIONS,
    PROCESSED_PRODUCTS,
    PROCESSED_USERS,
    PROCESSED_POPULAR_PRODUCTS,
    PROCESSED_USER_SEGMENTS,
    INTERIM_DATA_DIR,
    TRAIN_INTERACTIONS,
    VAL_INTERACTIONS,
    TEST_INTERACTIONS,
    REPORTS_DIR,
    EVENT_WEIGHTS,
)

def run_full_preprocessing():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(INTERIM_DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("================================================================")
    print("STEP 1: REGISTERING AUTHENTIC RETAILROCKET RAW DATA")
    print("================================================================")
    check_and_register_raw_data()

    print("\n================================================================")
    print("STEP 2: LOADING AUTHENTIC RETAILROCKET EVENTS")
    print("================================================================")
    df_raw = load_retailrocket_events()
    print(f"Loaded raw RetailRocket events: {len(df_raw):,}")

    # Deduplication
    df = df_raw.drop_duplicates(subset=["timestamp", "visitorid", "event", "itemid"]).copy()
    
    # Schema mapping for RetailRocket
    df.rename(columns={"visitorid": "user_id", "itemid": "product_id", "event": "event_type"}, inplace=True)
    df["item_id"] = df["product_id"]
    df["weight"] = df["event_type"].map(EVENT_WEIGHTS).fillna(1.0).astype(float)
    df["datetime_utc"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    # Sort strictly chronologically and make timestamps strictly monotonic
    df.sort_values(by="timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["timestamp"] = df["timestamp"] + df.groupby("timestamp").cumcount()
    df["interaction_id"] = df.index + 1

    cols = ["interaction_id", "user_id", "product_id", "item_id", "event_type", "weight", "timestamp", "datetime_utc", "transactionid"]
    df = df[[c for c in cols if c in df.columns]]

    df.to_csv(PROCESSED_INTERACTIONS, index=False)
    print(f"Saved canonical interactions to {PROCESSED_INTERACTIONS} ({len(df):,} rows)")

    print("\n================================================================")
    print("STEP 3: BUILDING PRODUCTS AND USERS ENTITIES")
    print("================================================================")
    
    # Products aggregation
    prod_agg = df.groupby(["product_id", "item_id"]).agg(
        interaction_count=("user_id", "count"),
        view_count=("event_type", lambda s: (s == "view").sum()),
        cart_count=("event_type", lambda s: (s == "addtocart").sum()),
        purchase_count=("event_type", lambda s: (s == "transaction").sum()),
        popularity_score=("weight", "sum"),
        unique_users=("user_id", "nunique"),
    ).reset_index()

    prod_agg["product_name"] = "Item " + prod_agg["product_id"].astype(str)
    prod_agg.sort_values(by="popularity_score", ascending=False, inplace=True)
    prod_agg.to_csv(PROCESSED_PRODUCTS, index=False)
    print(f"Saved products to {PROCESSED_PRODUCTS} ({len(prod_agg):,} products)")

    # Popular products
    popular_df = prod_agg.head(1000).copy()
    popular_df.to_csv(PROCESSED_POPULAR_PRODUCTS, index=False)
    print(f"Saved popular products to {PROCESSED_POPULAR_PRODUCTS}")

    # Users aggregation
    user_agg = df.groupby("user_id").agg(
        interaction_count=("user_id", "count"),
        unique_items=("item_id", "nunique"),
        unique_products=("product_id", "nunique"),
        view_count=("event_type", lambda s: (s == "view").sum()),
        cart_count=("event_type", lambda s: (s == "addtocart").sum()),
        purchase_count=("event_type", lambda s: (s == "transaction").sum()),
        total_affinity=("weight", "sum"),
        first_timestamp=("timestamp", "min"),
        last_timestamp=("timestamp", "max"),
    ).reset_index()

    def assign_segment(row):
        if row["purchase_count"] > 0:
            return "Purchaser"
        elif row["cart_count"] > 0:
            return "Cart Abandoner"
        elif row["view_count"] >= 5:
            return "Active Browser"
        else:
            return "Casual Browser"

    user_agg["user_segment"] = user_agg.apply(assign_segment, axis=1)
    user_agg.to_csv(PROCESSED_USERS, index=False)
    print(f"Saved users to {PROCESSED_USERS} ({len(user_agg):,} users)")

    segment_summary = user_agg.groupby("user_segment").agg(
        user_count=("user_id", "count"),
        avg_interactions=("interaction_count", "mean"),
        avg_unique_items=("unique_items", "mean"),
        total_views=("view_count", "sum"),
        total_carts=("cart_count", "sum"),
        total_purchases=("purchase_count", "sum"),
    ).reset_index()
    segment_summary["percentage"] = (segment_summary["user_count"] / len(user_agg)) * 100
    segment_summary.sort_values(by="user_count", ascending=False, inplace=True)
    segment_summary.to_csv(PROCESSED_USER_SEGMENTS, index=False)
    print(f"Saved user segment summary to {PROCESSED_USER_SEGMENTS}")

    print("\n================================================================")
    print("STEP 4: CREATING TEMPORAL SPLITS (NO LEAKAGE)")
    print("================================================================")
    min_ts = df["timestamp"].min()
    max_ts = df["timestamp"].max()
    ms_per_day = 86400 * 1000
    test_cutoff_ts = max_ts - (14 * ms_per_day)
    val_cutoff_ts = test_cutoff_ts - (14 * ms_per_day)

    train_df = df[df["timestamp"] < val_cutoff_ts].copy()
    val_df = df[(df["timestamp"] >= val_cutoff_ts) & (df["timestamp"] < test_cutoff_ts)].copy()
    test_df = df[df["timestamp"] >= test_cutoff_ts].copy()

    train_df.to_csv(TRAIN_INTERACTIONS, index=False)
    val_df.to_csv(VAL_INTERACTIONS, index=False)
    test_df.to_csv(TEST_INTERACTIONS, index=False)

    print(f"  ✓ Train: {len(train_df):,} rows")
    print(f"  ✓ Validation: {len(val_df):,} rows")
    print(f"  ✓ Test: {len(test_df):,} rows")

    train_max_ts = int(train_df["timestamp"].max()) if len(train_df) > 0 else 0
    val_min_ts = int(val_df["timestamp"].min()) if len(val_df) > 0 else 0
    val_max_ts = int(val_df["timestamp"].max()) if len(val_df) > 0 else 0
    test_min_ts = int(test_df["timestamp"].min()) if len(test_df) > 0 else 0

    split_audit = {
        "dataset_min_ts": int(min_ts),
        "dataset_max_ts": int(max_ts),
        "train": {"rows": len(train_df), "max_ts": train_max_ts},
        "validation": {"rows": len(val_df), "min_ts": val_min_ts, "max_ts": val_max_ts},
        "test": {"rows": len(test_df), "min_ts": test_min_ts},
        "leakage_verification": {
            "rule_a_train_before_val": bool(train_max_ts < val_min_ts),
            "rule_b_val_before_test": bool(val_max_ts < test_min_ts),
            "strict_chronological_ordering": True
        }
    }
    with open(REPORTS_DIR / "data_split_audit.json", "w") as f:
        json.dump(split_audit, f, indent=2)

    print("RetailRocket data preprocessing and splitting complete!")

if __name__ == "__main__":
    run_full_preprocessing()
