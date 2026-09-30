"""
Phase 1 Data Foundation Test Suite
Validates schema integrity, identifier consistency, rating domain,
leakage prevention, and split reproducibility.
"""

import os
import json
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.data.split_data import split_user_holdout
from src.data.acquire_data import check_and_register_raw_data


def test_popular_products_schema_and_domain():
    """Validates schema, non-emptiness, and rating bounds for popular_products.csv."""
    path = "data/processed/popular_products.csv"
    assert os.path.exists(path), f"Missing {path}"
    
    df = pd.read_csv(path)
    assert len(df) > 0, "popular_products.csv is empty"
    
    expected_cols = [
        "rank", "product_id", "product_name",
        "interaction_count", "unique_users",
        "average_rating", "popularity_score"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
        
    assert (df["average_rating"] >= 1.0).all() and (df["average_rating"] <= 5.0).all(), (
        "Product average ratings violate [1.0, 5.0] domain"
    )
    assert (df["interaction_count"] >= 1).all(), "Interaction count must be >= 1"


def test_users_schema_and_domain():
    """Validates schema, non-emptiness, and rating bounds for users.csv."""
    path = "data/processed/users.csv"
    assert os.path.exists(path), f"Missing {path}"
    
    df = pd.read_csv(path)
    assert len(df) > 0, "users.csv is empty"
    
    expected_cols = [
        "user_id", "interaction_count", "unique_products",
        "average_rating", "total_votes"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
        
    assert (df["average_rating"] >= 1.0).all() and (df["average_rating"] <= 5.0).all(), (
        "User average ratings violate [1.0, 5.0] domain"
    )
    assert df["user_id"].nunique() == len(df), "user_id contains duplicates in users.csv"


def test_split_holdout_leakage_and_determinism():
    """
    Validates split_user_holdout for:
    1. Zero leakage (disjoint train/val index sets).
    2. Determinism with identical random seed.
    3. Proper stratification for active vs sparse users.
    """
    # Create controlled mock interactions to test split mechanics
    records = []
    # User 1: 10 interactions (eligible)
    for p in range(10):
        records.append({"user_id": "u1", "product_id": f"p{p}", "rating": 4, "votes": 1, "helpful_votes": 1})
    # User 2: 3 interactions (sparse, < 5, non-eligible)
    for p in range(3):
        records.append({"user_id": "u2", "product_id": f"p{p}", "rating": 5, "votes": 0, "helpful_votes": 0})
        
    mock_df = pd.DataFrame(records)
    
    train1, val1, stats1 = split_user_holdout(mock_df, test_ratio=0.2, min_interactions=5, random_state=42)
    train2, val2, stats2 = split_user_holdout(mock_df, test_ratio=0.2, min_interactions=5, random_state=42)
    
    # 1. Leakage check: zero overlapping indices
    overlap = set(train1.index).intersection(set(val1.index))
    assert len(overlap) == 0, f"Leakage detected: overlapping indices {overlap}"
    
    # 2. Total preservation: train + val = total
    assert len(train1) + len(val1) == len(mock_df)
    
    # 3. Determinism check
    pd.testing.assert_frame_equal(train1, train2)
    pd.testing.assert_frame_equal(val1, val2)
    
    # 4. Sparse user check: User 2 must have 0 validation interactions
    assert "u2" not in val1["user_id"].values
    assert len(train1[train1["user_id"] == "u2"]) == 3
    
    # 5. Eligible user check: User 1 has 10 * 0.2 = 2 val interactions
    assert len(val1[val1["user_id"] == "u1"]) == 2
    assert len(train1[train1["user_id"] == "u1"]) == 8


def test_raw_data_registry_structure():
    """Validates raw data registration execution and JSON output."""
    registry = check_and_register_raw_data()
    assert isinstance(registry, dict)
    assert "dataset_name" in registry
    assert "competition_slug" in registry
    assert "files" in registry
    assert ("train.csv" in registry["files"]) or ("train_part1.csv" in registry["files"] and "train_part2.csv" in registry["files"])
    assert "test.csv" in registry["files"]
    assert os.path.exists("data/raw/raw_data_registry.json")


def test_data_foundation_audit_json_exists():
    """Verifies that the machine-readable audit report exists and has required sections."""
    path = "outputs/reports/data_foundation_audit.json"
    assert os.path.exists(path), f"Missing {path}"
    
    with open(path, "r") as f:
        data = json.load(f)
        
    assert "dataset_name" in data
    assert "timestamp_investigation" in data
    assert ("authentic_artifacts_audit" in data) or ("authentic_entities_verification" in data)
    assert "phase_1_exit_decision" in data
    assert data["timestamp_investigation"]["status"] == "NO LEGITIMATE TIMESTAMP SOURCE IDENTIFIED"
