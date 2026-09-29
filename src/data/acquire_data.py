"""
Dataset Acquisition and Raw Data Registration Script
Project 3: Personalized Product Recommendation Model
Dataset: Monash University FIT5212 S1 2025 Recommender System Challenge
Kaggle Slug: fit-5212-s-1-2025
"""

import os
import sys
import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REGISTRY_FILE = RAW_DIR / "raw_data_registry.json"

COMPETITION_SLUG = "fit-5212-s-1-2025"
COMPETITION_URL = f"https://www.kaggle.com/competitions/{COMPETITION_SLUG}"


def calculate_sha256(file_path: Path) -> str:
    """Calculates SHA-256 hash of a file in streaming chunks."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def ensure_directories():
    """Ensures raw, interim, and processed directories exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Directory structure verified: {RAW_DIR}, {INTERIM_DIR}, {PROCESSED_DIR}")


def check_and_register_raw_data() -> dict:
    """Checks raw data directory, records hashes, and writes registry."""
    ensure_directories()
    
    registry = {
        "dataset_name": "Monash University FIT5212 S1 2025 Recommender System Challenge",
        "competition_slug": COMPETITION_SLUG,
        "competition_url": COMPETITION_URL,
        "registration_timestamp": "2026-09-29T20:30:00Z",
        "files": {},
        "status": "INCOMPLETE"
    }

    train_path = RAW_DIR / "train.csv"
    test_path = RAW_DIR / "test.csv"

    if train_path.exists():
        size_bytes = train_path.stat().st_size
        sha256_hash = calculate_sha256(train_path)
        registry["files"]["train.csv"] = {
            "status": "PRESENT",
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "sha256": sha256_hash,
            "path": str(train_path.relative_to(BASE_DIR))
        }
    else:
        registry["files"]["train.csv"] = {
            "status": "MISSING",
            "expected_path": str(train_path.relative_to(BASE_DIR)),
            "instructions": (
                f"Obtain train.csv from {COMPETITION_URL} or student archive and place into data/raw/train.csv"
            )
        }

    if test_path.exists():
        size_bytes = test_path.stat().st_size
        sha256_hash = calculate_sha256(test_path)
        registry["files"]["test.csv"] = {
            "status": "PRESENT",
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "sha256": sha256_hash,
            "path": str(test_path.relative_to(BASE_DIR))
        }
    else:
        registry["files"]["test.csv"] = {
            "status": "MISSING",
            "expected_path": str(test_path.relative_to(BASE_DIR)),
            "instructions": (
                f"Obtain test.csv from {COMPETITION_URL} or student archive and place into data/raw/test.csv"
            )
        }

    train_present = train_path.exists()
    registry["status"] = "COMPLETE" if train_present else "AWAITING_SOURCE_DATA"

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print(f"[OK] Raw data registry written to {REGISTRY_FILE}")
    print(f"Status: {registry['status']}")
    return registry


if __name__ == "__main__":
    check_and_register_raw_data()
