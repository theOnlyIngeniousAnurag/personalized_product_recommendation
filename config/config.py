"""
Project Configuration Module
Personalized Product Recommendation Model - RetailRocket E-Commerce Recommender
"""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw" / "retailrocket"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LEGACY_DATA_DIR = DATA_DIR / "legacy" / "fit5212"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"

# Raw Data Files
RAW_EVENTS_FILE = RAW_DATA_DIR / "events.csv"
RAW_CATEGORY_TREE_FILE = RAW_DATA_DIR / "category_tree.csv"
RAW_ITEM_PROPERTIES_1 = (
    RAW_DATA_DIR / "item_properties_part1.csv"
    if (RAW_DATA_DIR / "item_properties_part1.csv").exists()
    else RAW_DATA_DIR / "item_properties_part1.csv.gz"
)
RAW_ITEM_PROPERTIES_2 = (
    RAW_DATA_DIR / "item_properties_part2.csv"
    if (RAW_DATA_DIR / "item_properties_part2.csv").exists()
    else RAW_DATA_DIR / "item_properties_part2.csv.gz"
)
RAW_REGISTRY_FILE = DATA_DIR / "raw" / "raw_data_registry.json"

# Processed Data Files
PROCESSED_INTERACTIONS = PROCESSED_DATA_DIR / "interactions.csv"
PROCESSED_PRODUCTS = PROCESSED_DATA_DIR / "products.csv"
PROCESSED_USERS = PROCESSED_DATA_DIR / "users.csv"
PROCESSED_CATEGORIES = PROCESSED_DATA_DIR / "categories.csv"
PROCESSED_POPULAR_PRODUCTS = PROCESSED_DATA_DIR / "popular_products.csv"
PROCESSED_USER_SEGMENTS = PROCESSED_DATA_DIR / "user_segment_summary.csv"

# Split Data Files
TRAIN_INTERACTIONS = INTERIM_DATA_DIR / "train_interactions.csv"
VAL_INTERACTIONS = INTERIM_DATA_DIR / "val_interactions.csv"
TEST_INTERACTIONS = INTERIM_DATA_DIR / "test_interactions.csv"

# Random Seed
RANDOM_SEED = 42

# Implicit Event Weights (Hu, Koren, Volinsky paradigm)
EVENT_WEIGHTS = {
    "view": 1.0,
    "addtocart": 3.0,
    "transaction": 5.0
}

# Evaluation K values
EVALUATION_K_VALUES = [5, 10, 20]

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
