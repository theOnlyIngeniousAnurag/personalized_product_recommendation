import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config import PROCESSED_INTERACTIONS
from src.utils.data_utils import (
    load_csv,
    check_required_columns,
    get_unique_count
)
from src.recommendation.recommendation_engine import RecommendationEngine


def test_load_interactions():
    file_path = str(PROCESSED_INTERACTIONS)
    df = load_csv(file_path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_required_columns():
    file_path = str(PROCESSED_INTERACTIONS)
    df = load_csv(file_path)

    # Core canonical fields in FIT5212 Amazon dataset
    required_columns = ["user_id", "product_id", "rating"]
    assert check_required_columns(df, required_columns)
    assert ("item_id" in df.columns) or ("product_id" in df.columns)


def test_unique_users():
    file_path = "data/processed/interactions.csv"
    df = load_csv(file_path)
    user_count = get_unique_count(df, "user_id")
    assert user_count > 0


def test_recommendation_engine_cold_start():
    engine = RecommendationEngine()
    # Test on a non-existent new user for cold-start fallback
    recommendations = engine.recommend("999999999", n=5)
    assert isinstance(recommendations, pd.DataFrame)
    assert len(recommendations) <= 5
    assert len(recommendations) > 0


def test_recommendation_columns():
    engine = RecommendationEngine()
    test_user = engine.user_ids[0] if engine.user_ids else "1813"
    recommendations = engine.recommend(test_user, n=5)

    expected_columns = [
        "product_id",
        "product_name",
        "recommendation_score",
        "recommendation_reason"
    ]
    for column in expected_columns:
        assert column in recommendations.columns


def test_recommendation_not_empty():
    engine = RecommendationEngine()
    test_user = engine.user_ids[0] if engine.user_ids else "1813"
    recommendations = engine.recommend(test_user, n=5)
    assert len(recommendations) > 0