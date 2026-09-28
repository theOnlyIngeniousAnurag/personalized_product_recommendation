from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


# Model directory
MODEL_DIR = BASE_DIR / "models"


# Output directories
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"
REPORTS_DIR = OUTPUT_DIR / "reports"


# Recommendation settings
TOP_K = 10

# Minimum number of interactions required
# for popularity-based recommendation
MIN_INTERACTIONS = 5

# Ratings equal to or above this value
# are considered relevant during evaluation
RATING_THRESHOLD = 4


# Dataset files
TRAIN_FILE = RAW_DATA_DIR / "train.csv"
TEST_FILE = RAW_DATA_DIR / "test.csv"

INTERACTIONS_FILE = PROCESSED_DATA_DIR / "interactions.csv"


# Project information
PROJECT_NAME = "Personalized Product Recommendation System"
RANDOM_STATE = 42