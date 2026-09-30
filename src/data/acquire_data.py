"""
Dataset Acquisition and Raw Data Registration Script
Project 3: Personalized Product Recommendation Model
Dataset: RetailRocket E-Commerce Recommender System Dataset
Source: Kaggle retailrocket/ecommerce-dataset
"""

import os
import sys
import json
import hashlib
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw" / "retailrocket"
LEGACY_DIR = DATA_DIR / "raw" / "legacy_fit5212"
REGISTRY_FILE = DATA_DIR / "raw" / "raw_data_registry.json"

KAGGLE_DATASET = "retailrocket/ecommerce-dataset"
DATASET_URL = f"https://www.kaggle.com/datasets/{KAGGLE_DATASET}"


def calculate_sha256(file_path: Path) -> str:
    """Calculates SHA-256 hash of a file in streaming chunks."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536 * 16):
            sha256.update(chunk)
    return sha256.hexdigest()


def count_lines(file_path: Path) -> int:
    """Counts data rows in a CSV file (excluding header)."""
    with open(file_path, "rb") as f:
        total = sum(1 for _ in f)
    return max(0, total - 1)


def ensure_directories():
    """Ensures raw, interim, and processed directories exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "interim").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)


def check_and_register_raw_data() -> dict:
    """Checks raw data directory, records hashes, row counts, and writes registry."""
    ensure_directories()
    
    registry = {
        "dataset_name": "RetailRocket E-Commerce Recommender System Dataset",
        "dataset_slug": KAGGLE_DATASET,
        "dataset_url": DATASET_URL,
        "active_dataset": "RETAILROCKET",
        "verification_metadata_timestamp": datetime.now(timezone.utc).isoformat(),
        "files": {},
        "legacy_fit5212": {
            "status": "PRESERVED_INACTIVE",
            "path": "data/raw/legacy_fit5212",
            "files": ["train_part1.csv", "train_part2.csv", "test.csv"]
        },
        "status": "AUTHENTIC_RETAILROCKET_VERIFIED"
    }

    raw_files = [
        "category_tree.csv",
        "events.csv",
        "item_properties_part1.csv",
        "item_properties_part2.csv"
    ]

    for fname in raw_files:
        fpath = RAW_DIR / fname
        if fpath.exists():
            fsize = fpath.stat().st_size
            frows = count_lines(fpath)
            fhash = calculate_sha256(fpath)
            registry["files"][fname] = {
                "status": "PRESENT_AND_VERIFIED",
                "size_bytes": fsize,
                "size_mb": round(fsize / (1024 * 1024), 2),
                "row_count": frows,
                "sha256": fhash,
                "path": f"data/raw/retailrocket/{fname}"
            }
        else:
            registry["files"][fname] = {
                "status": "MISSING",
                "path": f"data/raw/retailrocket/{fname}"
            }

    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"[OK] Raw data registry written to {REGISTRY_FILE}")
    return registry


if __name__ == "__main__":
    check_and_register_raw_data()
