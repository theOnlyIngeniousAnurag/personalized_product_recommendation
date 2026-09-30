"""
Project Configuration Module
Personalized Product Recommendation System - Monash FIT5212 Recommender
"""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"

# Raw Data Files
RAW_TRAIN_PART1 = RAW_DATA_DIR / "train_part1.csv"
RAW_TRAIN_PART2 = RAW_DATA_DIR / "train_part2.csv"
RAW_TEST_FILE = RAW_DATA_DIR / "test.csv"
RAW_REGISTRY_FILE = RAW_DATA_DIR / "raw_data_registry.json"

# Processed Data Files
PROCESSED_INTERACTIONS = PROCESSED_DATA_DIR / "interactions.csv"
PROCESSED_PRODUCTS = PROCESSED_DATA_DIR / "products.csv"
PROCESSED_USERS = PROCESSED_DATA_DIR / "users.csv"
PROCESSED_POPULAR_PRODUCTS = PROCESSED_DATA_DIR / "popular_products.csv"
PROCESSED_USER_SEGMENTS = PROCESSED_DATA_DIR / "user_segment_summary.csv"

# Split Data Files
TRAIN_INTERACTIONS = INTERIM_DATA_DIR / "train_interactions.csv"
VAL_INTERACTIONS = INTERIM_DATA_DIR / "val_interactions.csv"
TEST_INTERACTIONS = RAW_DATA_DIR / "test.csv"

# Random Seed
RANDOM_SEED = 42

# Evaluation K values
EVALUATION_K_VALUES = [5, 10, 20]

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
