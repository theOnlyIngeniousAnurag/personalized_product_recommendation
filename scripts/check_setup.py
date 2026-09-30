#!/usr/bin/env python3
"""
Environment and Data Foundation Setup Verification Utility.
Monash FIT5212 Personalized Product Recommendation System.
"""

import sys
import os
import json
import pandas as pd
from pathlib import Path

# Ensure root directory is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def run_check():
    print("================================================================")
    print("REPOSITY & DATA FOUNDATION SETUP CHECK")
    print("================================================================")
    print(f"✓ Python Version: {sys.version.split()[0]} ({sys.executable})")
    print(f"✓ Project Root: {PROJECT_ROOT}")

    errors = []

    # Check Required Directories
    required_dirs = [
        PROJECT_ROOT / "config",
        PROJECT_ROOT / "src",
        PROJECT_ROOT / "api",
        PROJECT_ROOT / "app",
        PROJECT_ROOT / "data" / "raw",
        PROJECT_ROOT / "data" / "interim",
        PROJECT_ROOT / "data" / "processed",
        PROJECT_ROOT / "outputs",
        PROJECT_ROOT / "screenshots",
        PROJECT_ROOT / "tests",
    ]

    for d in required_dirs:
        if d.exists():
            print(f"  [OK] Directory present: {d.relative_to(PROJECT_ROOT)}")
        else:
            print(f"  [MISSING] Directory: {d.relative_to(PROJECT_ROOT)}")
            errors.append(f"Missing directory: {d.relative_to(PROJECT_ROOT)}")

    # Check Processed Canonical Artifacts
    processed_files = {
        "interactions.csv": PROJECT_ROOT / "data" / "processed" / "interactions.csv",
        "products.csv": PROJECT_ROOT / "data" / "processed" / "products.csv",
        "users.csv": PROJECT_ROOT / "data" / "processed" / "users.csv",
        "popular_products.csv": PROJECT_ROOT / "data" / "processed" / "popular_products.csv",
    }

    print("\n--- Processed Artifact Validation ---")
    for name, path in processed_files.items():
        if path.exists():
            try:
                df = pd.read_csv(path, nrows=5)
                size_mb = path.stat().st_size / (1024 * 1024)
                print(f"  [OK] {name}: {size_mb:.2f} MB present.")
            except Exception as e:
                print(f"  [ERROR] {name}: unreadable ({e})")
                errors.append(f"Corrupt artifact: {name}")
        else:
            print(f"  [MISSING] {name}")
            errors.append(f"Missing processed artifact: {name}")

    # Check Raw FIT5212 Dataset Files
    raw_files = {
        "train_part1.csv": PROJECT_ROOT / "data" / "raw" / "train_part1.csv",
        "train_part2.csv": PROJECT_ROOT / "data" / "raw" / "train_part2.csv",
        "test.csv": PROJECT_ROOT / "data" / "raw" / "test.csv",
    }

    print("\n--- Raw FIT5212 Dataset Validation ---")
    raw_present = True
    for name, path in raw_files.items():
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"  [OK] {name}: {size_mb:.2f} MB present.")
        else:
            print(f"  [MISSING] {name} (Optional if canonical processed artifacts exist)")
            raw_present = False

    print("\n================================================================")
    if not errors:
        print("✓ STATUS: PROJECT READY — ALL CORE ASSETS VERIFIED")
        print("================================================================")
        return True
    else:
        print("⚠ STATUS: ISSUES DETECTED")
        for err in errors:
            print(f"  - {err}")
        print("================================================================")
        return False

if __name__ == "__main__":
    success = run_check()
    sys.exit(0 if success else 1)
