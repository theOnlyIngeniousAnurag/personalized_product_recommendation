"""
Authentic RetailRocket High-Performance Vectorized Preprocessing Pipeline
Transforms raw RetailRocket behavior, taxonomy, and item properties
into canonical processed entities, popular products baseline, user segments,
and chronological zero-leakage evaluation partitions.
"""

import os
import gc
import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path

from src.data.acquire_data import check_and_register_raw_data
from src.data.split_data import create_temporal_split
from config.config import (
    RAW_DATA_DIR,
    RAW_EVENTS_FILE,
    RAW_CATEGORY_TREE_FILE,
    RAW_ITEM_PROPERTIES_1,
    RAW_ITEM_PROPERTIES_2,
    PROCESSED_DATA_DIR,
    PROCESSED_INTERACTIONS,
    PROCESSED_PRODUCTS,
    PROCESSED_USERS,
    PROCESSED_CATEGORIES,
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
    """Executes end-to-end RetailRocket ingestion and canonical preparation."""
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(INTERIM_DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("================================================================")
    print("STEP 1: VERIFYING & REGISTERING RAW RETAILROCKET ASSETS")
    print("================================================================")
    raw_registry = check_and_register_raw_data()

    print("\n================================================================")
    print("STEP 2: EXTRACTING CATEGORY TREE TAXONOMY")
    print("================================================================")
    if os.path.exists(RAW_CATEGORY_TREE_FILE):
        df_cat = pd.read_csv(RAW_CATEGORY_TREE_FILE)
        df_cat.rename(columns={"categoryid": "category_id", "parentid": "parent_category_id"}, inplace=True)
        df_cat.to_csv(PROCESSED_CATEGORIES, index=False)
        print(f"Saved {len(df_cat):,} categories to {PROCESSED_CATEGORIES}")
    else:
        print(f"Warning: Category tree file not found at {RAW_CATEGORY_TREE_FILE}")

    print("\n================================================================")
    print("STEP 3: INGESTING, VALIDATING, AND CANONIZING BEHAVIORAL EVENTS")
    print("================================================================")
    print(f"Reading events from {RAW_EVENTS_FILE}...")
    df_events = pd.read_csv(
        RAW_EVENTS_FILE,
        dtype={
            "timestamp": "int64",
            "visitorid": "int64",
            "event": "category",
            "itemid": "int64",
            "transactionid": "float64",
        }
    )
    raw_event_count = len(df_events)
    print(f"Raw behavioral events read: {raw_event_count:,}")

    # Deterministic Deduplication
    df_events.drop_duplicates(subset=["timestamp", "visitorid", "event", "itemid"], inplace=True)
    dedup_count = len(df_events)
    duplicates_removed = raw_event_count - dedup_count

    # Deterministic Validation Filter
    valid_mask = (
        (df_events["visitorid"] > 0) &
        (df_events["itemid"] > 0) &
        (df_events["timestamp"] > 1400000000000) &
        (df_events["event"].isin(["view", "addtocart", "transaction"]))
    )
    df_events = df_events[valid_mask].copy()
    valid_count = len(df_events)
    invalid_removed = dedup_count - valid_count

    # Map to Canonical Schema
    df_events.rename(columns={
        "visitorid": "user_id",
        "itemid": "product_id",
        "event": "event_type"
    }, inplace=True)

    # Provide item_id and product_name aliases for backwards compatibility
    df_events["item_id"] = df_events["product_id"]
    df_events["product_name"] = "Item " + df_events["product_id"].astype(str)

    # Event weights (implicit feedback strength)
    event_weight_map = {"view": 1.0, "addtocart": 3.0, "transaction": 5.0}
    df_events["rating"] = df_events["event_type"].map(event_weight_map).astype(np.float32)
    df_events["weight"] = df_events["rating"]

    # Sort chronologically by authentic timestamp
    df_events.sort_values(by="timestamp", ascending=True, inplace=True)
    df_events.reset_index(drop=True, inplace=True)
    df_events["interaction_id"] = np.arange(1, len(df_events) + 1, dtype=np.int64)

    # Indicator columns for high-speed vectorized aggregations
    df_events["is_view"] = (df_events["event_type"] == "view").astype(np.int8)
    df_events["is_cart"] = (df_events["event_type"] == "addtocart").astype(np.int8)
    df_events["is_buy"] = (df_events["event_type"] == "transaction").astype(np.int8)

    # Save Canonical Interactions
    cols = [
        "interaction_id",
        "user_id",
        "product_id",
        "item_id",
        "product_name",
        "event_type",
        "rating",
        "weight",
        "timestamp",
        "transactionid"
    ]
    df_events[cols].to_csv(PROCESSED_INTERACTIONS, index=False)
    print(f"Saved canonical interactions to {PROCESSED_INTERACTIONS} ({len(df_events):,} rows)")

    unique_users = df_events["user_id"].nunique()
    unique_products = df_events["product_id"].nunique()
    print(f"Unique Users: {unique_users:,} | Unique Products: {unique_products:,}")

    print("\n================================================================")
    print("STEP 4: EXTRACTING PRODUCT CATEGORY METADATA FROM ITEM PROPERTIES")
    print("================================================================")
    active_products = set(df_events["product_id"].unique())
    category_map = {}

    for prop_file in [RAW_ITEM_PROPERTIES_1, RAW_ITEM_PROPERTIES_2]:
        if prop_file and os.path.exists(prop_file):
            print(f"Scanning {os.path.basename(prop_file)} for category assignments...")
            for chunk in pd.read_csv(
                prop_file,
                chunksize=1000000,
                usecols=["itemid", "property", "value"]
            ):
                sub = chunk[
                    (chunk["property"] == "categoryid") &
                    (chunk["itemid"].isin(active_products))
                ][["itemid", "value"]]
                if not sub.empty:
                    for item_id, cat_val in zip(sub["itemid"], sub["value"]):
                        category_map[item_id] = cat_val
            gc.collect()

    print(f"Mapped categories for {len(category_map):,} active products.")

    print("\n================================================================")
    print("STEP 5: GENERATING PRODUCTS CATALOG & POPULARITY BASELINE")
    print("================================================================")
    prod_agg = df_events.groupby("product_id").agg(
        interaction_count=("interaction_id", "count"),
        view_count=("is_view", "sum"),
        cart_count=("is_cart", "sum"),
        purchase_count=("is_buy", "sum"),
        popularity_score=("rating", "sum"),
        average_rating=("rating", "mean"),
        unique_users=("user_id", "nunique"),
    ).reset_index()

    prod_agg["item_id"] = prod_agg["product_id"]
    prod_agg["product_name"] = "Item " + prod_agg["product_id"].astype(str)
    prod_agg["category_id"] = prod_agg["product_id"].map(category_map)
    prod_agg.sort_values(by="popularity_score", ascending=False, inplace=True)
    prod_agg.to_csv(PROCESSED_PRODUCTS, index=False)
    print(f"Saved products catalog to {PROCESSED_PRODUCTS} ({len(prod_agg):,} products)")

    # Popular Products Baseline (Top 1,000 items)
    popular_df = prod_agg.head(1000).copy()
    popular_df.to_csv(PROCESSED_POPULAR_PRODUCTS, index=False)
    print(f"Saved popular products baseline to {PROCESSED_POPULAR_PRODUCTS}")

    print("\n================================================================")
    print("STEP 6: GENERATING USER PROFILES & BEHAVIORAL SEGMENTATION")
    print("================================================================")
    # Perform user aggregation efficiently
    user_agg = df_events.groupby("user_id").agg(
        interaction_count=("interaction_id", "count"),
        unique_items=("product_id", "nunique"),
        view_count=("is_view", "sum"),
        cart_count=("is_cart", "sum"),
        purchase_count=("is_buy", "sum"),
        total_affinity=("rating", "sum"),
        first_timestamp=("timestamp", "min"),
        last_timestamp=("timestamp", "max"),
    ).reset_index()

    conditions = [
        user_agg["purchase_count"] > 0,
        user_agg["cart_count"] > 0,
        user_agg["view_count"] >= 5
    ]
    choices = ["Purchaser", "Cart Abandoner", "Active Browser"]
    user_agg["user_segment"] = np.select(conditions, choices, default="Casual Browser")

    user_agg.to_csv(PROCESSED_USERS, index=False)
    print(f"Saved user profiles to {PROCESSED_USERS} ({len(user_agg):,} users)")

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
    print("STEP 7: CHRONOLOGICAL ZERO-LEAKAGE TEMPORAL SPLITTING")
    print("================================================================")
    split_audit = create_temporal_split(val_days=14, test_days=14)

    # Compile comprehensive cleaning and reconciliation audit
    audit_report = {
        "dataset_name": "RetailRocket E-Commerce Recommender System",
        "raw_events_count": raw_event_count,
        "duplicates_removed": duplicates_removed,
        "invalid_removed": invalid_removed,
        "canonical_interactions_count": len(df_events),
        "unique_users": unique_users,
        "unique_products": unique_products,
        "timestamp_min": int(df_events["timestamp"].min()),
        "timestamp_max": int(df_events["timestamp"].max()),
        "date_min_utc": pd.to_datetime(df_events["timestamp"].min(), unit="ms", utc=True).isoformat(),
        "date_max_utc": pd.to_datetime(df_events["timestamp"].max(), unit="ms", utc=True).isoformat(),
        "event_distribution": df_events["event_type"].value_counts().to_dict(),
        "temporal_split": split_audit
    }

    with open(REPORTS_DIR / "retailrocket_data_foundation_audit.json", "w") as f:
        json.dump(audit_report, f, indent=2)

    print("\n================================================================")
    print("RETAILROCKET PREPROCESSING & INGESTION COMPLETED SUCCESSFULLY!")
    print("================================================================")
    return audit_report


if __name__ == "__main__":
    run_full_preprocessing()
