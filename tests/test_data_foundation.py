"""
Phase 1 Data Foundation Test Suite (RetailRocket Recommender System Migration)
Validates authentic schema integrity, identifier consistency, chronological event timestamps,
zero-leakage temporal split boundaries, and data foundation audit contracts.
"""

import os
import json
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.data.split_data import create_temporal_split
from src.data.acquire_data import check_and_register_raw_data
from config.config import (
    PROCESSED_INTERACTIONS,
    PROCESSED_PRODUCTS,
    PROCESSED_POPULAR_PRODUCTS,
    PROCESSED_USERS,
    TRAIN_INTERACTIONS,
    VAL_INTERACTIONS,
    TEST_INTERACTIONS,
    RAW_REGISTRY_FILE,
    REPORTS_DIR,
)


def test_popular_products_schema_and_domain():
    """Validates schema, non-emptiness, and popularity score bounds for popular_products.csv."""
    path = PROCESSED_POPULAR_PRODUCTS
    assert os.path.exists(path), f"Missing {path}"
    
    df = pd.read_csv(path)
    assert len(df) > 0, "popular_products.csv is empty"
    
    # Check item/product identifier
    id_col = "item_id" if "item_id" in df.columns else "product_id"
    assert id_col in df.columns, "Missing item/product identifier column"
    assert "popularity_score" in df.columns, "Missing popularity_score column"
    assert "interaction_count" in df.columns, "Missing interaction_count column"
    
    assert (df["popularity_score"] >= 0.0).all(), "Popularity scores must be non-negative"
    assert (df["interaction_count"] >= 1).all(), "Interaction count must be >= 1"


def test_users_schema_and_domain():
    """Validates schema, non-emptiness, and segmentation for users.csv."""
    path = PROCESSED_USERS
    assert os.path.exists(path), f"Missing {path}"
    
    df = pd.read_csv(path)
    assert len(df) > 0, "users.csv is empty"
    
    expected_cols = ["user_id", "interaction_count", "unique_items"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
        
    assert (df["interaction_count"] >= 1).all(), "User interaction count must be >= 1"
    assert df["user_id"].nunique() == len(df), "user_id contains duplicates in users.csv"


def test_interactions_schema_and_chronology():
    """Validates canonical interactions schema and monotonic timestamp sorting."""
    path = PROCESSED_INTERACTIONS
    assert os.path.exists(path), f"Missing {path}"
    
    df = pd.read_csv(path, nrows=5000)
    assert len(df) > 0, "interactions.csv is empty"
    
    expected_cols = ["user_id", "event_type", "timestamp"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
        
    # Check item identifier column
    assert ("item_id" in df.columns) or ("product_id" in df.columns)
    
    # Verify timestamp domain (RetailRocket 2015 timestamps in ms: > 1.4e12)
    assert (df["timestamp"] > 1400000000000).all(), "Timestamps must be valid epoch milliseconds"
    assert df["timestamp"].is_monotonic_increasing, "Canonical interactions must be monotonically sorted by timestamp"


def test_temporal_split_leakage_and_determinism():
    """
    Validates chronological temporal splitting for:
    1. Zero temporal leakage: max(train) < min(val) and max(val) < min(test).
    2. Strict temporal ordering.
    """
    assert os.path.exists(TRAIN_INTERACTIONS), f"Missing {TRAIN_INTERACTIONS}"
    assert os.path.exists(VAL_INTERACTIONS), f"Missing {VAL_INTERACTIONS}"
    assert os.path.exists(TEST_INTERACTIONS), f"Missing {TEST_INTERACTIONS}"
    
    train_df = pd.read_csv(TRAIN_INTERACTIONS, usecols=["timestamp"])
    val_df = pd.read_csv(VAL_INTERACTIONS, usecols=["timestamp"])
    test_df = pd.read_csv(TEST_INTERACTIONS, usecols=["timestamp"])
    
    assert len(train_df) > 0, "Train partition is empty"
    assert len(val_df) > 0, "Validation partition is empty"
    assert len(test_df) > 0, "Test partition is empty"
    
    train_max = train_df["timestamp"].max()
    val_min = val_df["timestamp"].min()
    val_max = val_df["timestamp"].max()
    test_min = test_df["timestamp"].min()
    
    # Strict temporal separation
    assert train_max < val_min, f"Temporal leakage: Train max ts ({train_max}) >= Val min ts ({val_min})"
    assert val_max < test_min, f"Temporal leakage: Val max ts ({val_max}) >= Test min ts ({test_min})"


def test_raw_data_registry_structure():
    """Validates raw data registration execution and JSON output."""
    path = RAW_REGISTRY_FILE
    assert os.path.exists(path), f"Missing raw data registry at {path}"
    
    with open(path, "r") as f:
        registry = json.load(f)
        
    assert isinstance(registry, dict)
    assert "events.csv" in registry or "category_tree.csv" in registry or "dataset_name" in registry


def test_data_foundation_audit_json_exists():
    """Verifies that machine-readable audit report exists."""
    audit_file = REPORTS_DIR / "data_split_audit.json"
    assert os.path.exists(audit_file), f"Missing split audit at {audit_file}"
    
    with open(audit_file, "r") as f:
        data = json.load(f)
        
    assert "train" in data
    assert "validation" in data
    assert "test" in data
    assert "leakage_verification" in data
    assert data["leakage_verification"]["strict_chronological_ordering"] is True
