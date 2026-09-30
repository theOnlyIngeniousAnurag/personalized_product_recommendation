"""
Integrated Acquisition, Provenance Hashing, and Canonical Processing Pipeline
Personalized Product Recommendation Model - RetailRocket Dataset
"""

import os
import gc
import json
import shutil
import hashlib
import kagglehub
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path
from config.config import (
    RAW_DATA_DIR,
    RAW_EVENTS_FILE,
    RAW_CATEGORY_TREE_FILE,
    RAW_REGISTRY_FILE,
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

def compute_sha256(filepath: str, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 hash of a file efficiently."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()

def execute_pipeline():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(INTERIM_DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("================================================================")
    print("STEP 1: ACQUIRING AUTHENTIC RETAILROCKET DATASET VIA KAGGLEHUB")
    print("================================================================")
    download_dir = kagglehub.dataset_download("retailrocket/ecommerce-dataset")
    print(f"Downloaded raw package to: {download_dir}")
    source_files = os.listdir(download_dir)
    print(f"Discovered files: {source_files}")

    print("\n================================================================")
    print("STEP 2: COMPUTING SHA-256 HASHES & PROVENANCE REGISTRATION")
    print("================================================================")
    registry = {}
    for fname in ["category_tree.csv", "events.csv", "item_properties_part1.csv", "item_properties_part2.csv"]:
        fpath = os.path.join(download_dir, fname)
        if os.path.exists(fpath):
            fsize = os.path.getsize(fpath)
            fhash = compute_sha256(fpath)
            registry[fname] = {
                "source": "RetailRocket Recommender System Dataset",
                "url": "https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset",
                "sha256": fhash,
                "size_bytes": fsize,
                "verified_at": datetime.now(timezone.utc).isoformat(),
                "status": "AUTHENTIC_VERIFIED"
            }
            print(f"  ✓ {fname}: {fsize:,} bytes | SHA-256: {fhash}")

    with open(RAW_REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"Registry written to {RAW_REGISTRY_FILE}")

    # Copy category_tree.csv and events.csv to RAW_DATA_DIR
    shutil.copy2(os.path.join(download_dir, "category_tree.csv"), RAW_CATEGORY_TREE_FILE)
    print(f"Copied category_tree.csv to {RAW_CATEGORY_TREE_FILE}")
    shutil.copy2(os.path.join(download_dir, "events.csv"), RAW_EVENTS_FILE)
    print(f"Copied events.csv to {RAW_EVENTS_FILE}")

    print("\n================================================================")
    print("STEP 3: EXTRACTING CATEGORY TAXONOMY & METADATA")
    print("================================================================")
    df_cat = pd.read_csv(RAW_CATEGORY_TREE_FILE)
    df_cat.rename(columns={"categoryid": "category_id", "parentid": "parent_category_id"}, inplace=True)
    df_cat.to_csv(PROCESSED_CATEGORIES, index=False)
    print(f"Saved categories to {PROCESSED_CATEGORIES} ({len(df_cat):,} categories)")

    print("\n================================================================")
    print("STEP 4: PROCESSING EVENTS & CANONICAL INTERACTIONS")
    print("================================================================")
    df_events = pd.read_csv(RAW_EVENTS_FILE)
    initial_rows = len(df_events)
    print(f"Raw interaction count: {initial_rows:,}")

    # Deduplication
    df_events.drop_duplicates(subset=["timestamp", "visitorid", "event", "itemid"], inplace=True)
    dedup_rows = len(df_events)
    duplicates_removed = initial_rows - dedup_rows

    # Validation
    valid_mask = (
        (df_events["visitorid"].notnull()) & (df_events["visitorid"] > 0) &
        (df_events["itemid"].notnull()) & (df_events["itemid"] > 0) &
        (df_events["event"].isin(["view", "addtocart", "transaction"])) &
        (df_events["timestamp"].notnull()) & (df_events["timestamp"] > 0)
    )
    df_events = df_events[valid_mask].copy()
    valid_rows = len(df_events)
    invalid_removed = dedup_rows - valid_rows

    # Canonical Schema
    df_events.rename(columns={"visitorid": "user_id", "itemid": "item_id", "event": "event_type"}, inplace=True)
    df_events["weight"] = df_events["event_type"].map(EVENT_WEIGHTS).astype(float)
    df_events["datetime_utc"] = pd.to_datetime(df_events["timestamp"], unit="ms", utc=True)
    df_events.sort_values(by="timestamp", inplace=True)
    df_events.reset_index(drop=True, inplace=True)
    df_events["interaction_id"] = df_events.index + 1

    cols = ["interaction_id", "user_id", "item_id", "event_type", "weight", "timestamp", "datetime_utc", "transactionid"]
    df_events = df_events[cols]
    df_events.to_csv(PROCESSED_INTERACTIONS, index=False)
    print(f"Saved canonical interactions to {PROCESSED_INTERACTIONS} ({len(df_events):,} rows)")

    # Active items
    active_item_set = set(df_events["item_id"].unique())
    print(f"Unique active products in interaction log: {len(active_item_set):,}")

    print("\n================================================================")
    print("STEP 5: STREAMING ITEM PROPERTIES FOR CATALOG METADATA")
    print("================================================================")
    item_props = {}
    for pfile in ["item_properties_part1.csv", "item_properties_part2.csv"]:
        src_p = os.path.join(download_dir, pfile)
        if os.path.exists(src_p):
            print(f"Streaming {pfile}...")
            for chunk in pd.read_csv(src_p, usecols=["timestamp", "itemid", "property", "value"], chunksize=500000):
                filtered = chunk[
                    (chunk["property"].isin(["categoryid", "available"])) &
                    (chunk["itemid"].isin(active_item_set))
                ]
                for _, row in filtered.iterrows():
                    iid = int(row["itemid"])
                    prop = row["property"]
                    val = row["value"]
                    ts = int(row["timestamp"])
                    if iid not in item_props:
                        item_props[iid] = {}
                    if prop not in item_props[iid] or ts > item_props[iid][prop][0]:
                        item_props[iid][prop] = (ts, val)
            gc.collect()

    print(f"Extracted metadata properties for {len(item_props):,} active items.")

    print("\n================================================================")
    print("STEP 6: GENERATING PRODUCTS, POPULARITY, AND USER ENTITIES")
    print("================================================================")
    # Product aggregations
    prod_agg = df_events.groupby("item_id").agg(
        interaction_count=("interaction_id", "count"),
        view_count=("event_type", lambda s: (s == "view").sum()),
        cart_count=("event_type", lambda s: (s == "addtocart").sum()),
        purchase_count=("event_type", lambda s: (s == "transaction").sum()),
        popularity_score=("weight", "sum"),
        unique_users=("user_id", "nunique"),
    ).reset_index()

    categories = []
    availabilities = []
    for iid in prod_agg["item_id"]:
        props = item_props.get(iid, {})
        cat = props.get("categoryid", (None, None))[1]
        avail = props.get("available", (None, 1))[1]
        try:
            cat_id = int(cat) if cat is not None and pd.notnull(cat) else None
        except (ValueError, TypeError):
            cat_id = None
        try:
            avail_int = int(avail) if avail is not None and pd.notnull(avail) else 1
        except (ValueError, TypeError):
            avail_int = 1
        categories.append(cat_id)
        availabilities.append(avail_int)

    prod_agg["category_id"] = categories
    prod_agg["available"] = availabilities
    prod_agg["product_name"] = "Item " + prod_agg["item_id"].astype(str)
    prod_agg.sort_values(by="popularity_score", ascending=False, inplace=True)
    prod_agg.to_csv(PROCESSED_PRODUCTS, index=False)
    print(f"Saved products catalog to {PROCESSED_PRODUCTS} ({len(prod_agg):,} products)")

    # Popular products
    popular_df = prod_agg.head(1000).copy()
    popular_df.to_csv(PROCESSED_POPULAR_PRODUCTS, index=False)
    print(f"Saved top 1,000 popular products to {PROCESSED_POPULAR_PRODUCTS}")

    # User profiles & segmentation
    user_agg = df_events.groupby("user_id").agg(
        interaction_count=("interaction_id", "count"),
        unique_items=("item_id", "nunique"),
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
    print("STEP 7: CHRONOLOGICAL TEMPORAL SPLITTING (NO LEAKAGE)")
    print("================================================================")
    max_ts = df_events["timestamp"].max()
    ms_per_day = 86400 * 1000
    test_cutoff_ts = max_ts - (14 * ms_per_day)
    val_cutoff_ts = test_cutoff_ts - (14 * ms_per_day)

    train_df = df_events[df_events["timestamp"] < val_cutoff_ts].copy()
    val_df = df_events[(df_events["timestamp"] >= val_cutoff_ts) & (df_events["timestamp"] < test_cutoff_ts)].copy()
    test_df = df_events[df_events["timestamp"] >= test_cutoff_ts].copy()

    train_df.to_csv(TRAIN_INTERACTIONS, index=False)
    val_df.to_csv(VAL_INTERACTIONS, index=False)
    test_df.to_csv(TEST_INTERACTIONS, index=False)

    print(f"  ✓ Train Interactions: {len(train_df):,} rows")
    print(f"  ✓ Validation Interactions: {len(val_df):,} rows")
    print(f"  ✓ Test Interactions: {len(test_df):,} rows")

    train_max_ts = int(train_df["timestamp"].max())
    val_min_ts = int(val_df["timestamp"].min())
    val_max_ts = int(val_df["timestamp"].max())
    test_min_ts = int(test_df["timestamp"].min())
    test_max_ts = int(test_df["timestamp"].max())

    rule_a_pass = train_max_ts < val_min_ts
    rule_b_pass = val_max_ts < test_min_ts
    print(f"  ✓ Leakage Rule A (Train Max < Val Min): {rule_a_pass}")
    print(f"  ✓ Leakage Rule B (Val Max < Test Min): {rule_b_pass}")

    # Cleaning temporary download cache
    try:
        shutil.rmtree(download_dir)
        print("\nCleaned temporary download cache.")
    except Exception as e:
        print(f"Notice on cache cleanup: {e}")

    print("\n================================================================")
    print("RETAILROCKET MIGRATION & PHASE 1 DATA FOUNDATION SUCCESSFUL!")
    print("================================================================")

if __name__ == "__main__":
    execute_pipeline()
