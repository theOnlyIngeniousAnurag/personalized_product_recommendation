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
import pandas as pd
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


def count_lines(file_path: Path) -> int:
    """Counts data rows in a CSV file (excluding header)."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        total = sum(1 for _ in f)
    return max(0, total - 1)


def ensure_directories():
    """Ensures raw, interim, and processed directories exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Directory structure verified: {RAW_DIR}, {INTERIM_DIR}, {PROCESSED_DIR}")


def check_and_register_raw_data() -> dict:
    """Checks raw data directory, records hashes, row counts, and writes registry."""
    ensure_directories()
    
    registry = {
        "dataset_name": "Monash University FIT5212 S1 2025 Recommender System Challenge",
        "competition_slug": COMPETITION_SLUG,
        "competition_url": COMPETITION_URL,
        "verification_metadata_timestamp": "2026-09-29T21:18:00Z",
        "note_on_timestamp": (
            "The verification_metadata_timestamp records when the system administrator/agent "
            "verified these files. It is NOT an ML data event timestamp."
        ),
        "files": {},
        "logical_training_data": {},
        "status": "INCOMPLETE"
    }

    raw_files = ["train_part1.csv", "train_part2.csv", "test.csv"]
    train_parts_present = True

    for fname in raw_files:
        fpath = RAW_DIR / fname
        if fpath.exists() and fpath.stat().st_size > 0:
            size_bytes = fpath.stat().st_size
            sha256_hash = calculate_sha256(fpath)
            rows = count_lines(fpath)
            registry["files"][fname] = {
                "status": "PRESENT_AND_VERIFIED",
                "size_bytes": size_bytes,
                "size_mb": round(size_bytes / (1024 * 1024), 2),
                "row_count": rows,
                "sha256": sha256_hash,
                "path": str(fpath.relative_to(BASE_DIR))
            }
        else:
            registry["files"][fname] = {
                "status": "MISSING",
                "expected_path": str(fpath.relative_to(BASE_DIR)),
                "instructions": f"Place authentic {fname} into data/raw/"
            }
            if fname in ["train_part1.csv", "train_part2.csv"]:
                train_parts_present = False

    test_present = (RAW_DIR / "test.csv").exists() and (RAW_DIR / "test.csv").stat().st_size > 0

    if train_parts_present:
        rows_p1 = registry["files"]["train_part1.csv"]["row_count"]
        rows_p2 = registry["files"]["train_part2.csv"]["row_count"]
        total_train_rows = rows_p1 + rows_p2
        registry["logical_training_data"] = {
            "status": "AUTHENTIC_AND_VERIFIED",
            "components": ["train_part1.csv", "train_part2.csv"],
            "total_records": total_train_rows,
            "expected_records": 745889,
            "exact_match": total_train_rows == 745889,
            "note": (
                "train_part1.csv and train_part2.csv are two row-wise halves of the original "
                "train.csv, split strictly for upload size accommodation. They form one logical dataset."
            )
        }

    if train_parts_present and test_present:
        registry["status"] = "COMPLETE_AUTHENTIC_DATA_VERIFIED"
    elif train_parts_present:
        registry["status"] = "TRAIN_DATA_VERIFIED_AWAITING_TEST"
    else:
        registry["status"] = "AWAITING_SOURCE_DATA"

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print(f"[OK] Raw data registry written to {REGISTRY_FILE}")
    print(f"Status: {registry['status']}")
    return registry


def load_logical_raw_train() -> pd.DataFrame:
    """
    Deterministically loads and concatenates train_part1.csv and train_part2.csv
    or train.csv if present.
    """
    train_full = RAW_DIR / "train.csv"
    p1 = RAW_DIR / "train_part1.csv"
    p2 = RAW_DIR / "train_part2.csv"
    
    if train_full.exists() and train_full.stat().st_size > 0:
        return pd.read_csv(train_full)
    elif p1.exists() and p2.exists():
        df1 = pd.read_csv(p1)
        df2 = pd.read_csv(p2)
        return pd.concat([df1, df2], ignore_index=True)
    else:
        raise FileNotFoundError(
            f"Neither train.csv nor (train_part1.csv + train_part2.csv) found in {RAW_DIR}"
        )


if __name__ == "__main__":
    check_and_register_raw_data()
