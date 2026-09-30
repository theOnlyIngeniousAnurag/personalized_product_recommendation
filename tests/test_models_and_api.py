"""
Comprehensive Model, Evaluation, and API Test Suite
Project 3: Personalized Product Recommendation Model
Validates Popularity, User-kNN CF, SVD Matrix Factorization, Content-Based,
Hybrid recommender, cold-start fallbacks, metric computations, and REST API.
"""

import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from src.recommendation.recommendation_engine import RecommendationEngine
from src.evaluation.evaluate_recommendations import precision_at_k, recall_at_k, ndcg_at_k
from api.recommendation_api import app


@pytest.fixture(scope="module")
def engine():
    return RecommendationEngine()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_popularity_recommender(engine):
    recs = engine.recommend_popularity("1813", n=5)
    assert isinstance(recs, pd.DataFrame)
    assert len(recs) == 5
    assert "product_id" in recs.columns
    assert "recommendation_score" in recs.columns


def test_collaborative_recommender(engine):
    recs = engine.recommend_collaborative("1813", n=5)
    assert isinstance(recs, pd.DataFrame)
    assert len(recs) == 5
    assert (recs["recommendation_score"] >= 0.0).all()


def test_matrix_factorization_recommender(engine):
    recs = engine.recommend_matrix_factorization("1813", n=5)
    assert isinstance(recs, pd.DataFrame)
    assert len(recs) == 5
    assert (recs["recommendation_score"] >= 0.0).all()


def test_content_based_recommender(engine):
    recs = engine.recommend_content("1813", n=5)
    assert isinstance(recs, pd.DataFrame)
    assert len(recs) == 5
    assert "product_name" in recs.columns


def test_hybrid_recommender(engine):
    recs = engine.recommend_hybrid("1813", n=5)
    assert isinstance(recs, pd.DataFrame)
    assert len(recs) == 5
    assert "recommendation_reason" in recs.columns


def test_cold_start_unknown_user(engine):
    unknown_id = "completely_unknown_user_99999"
    recs = engine.recommend_hybrid(unknown_id, n=5)
    assert isinstance(recs, pd.DataFrame)
    assert len(recs) == 5
    # Should fall back to popularity gracefully
    assert "popular" in recs["recommendation_reason"].iloc[0].lower()


def test_evaluation_metrics_math():
    relevant = {"p1", "p2", "p3"}
    # Perfect match top 3
    rec_perfect = ["p1", "p2", "p3", "p4", "p5"]
    assert precision_at_k(rec_perfect, relevant, 5) == 3 / 5
    assert recall_at_k(rec_perfect, relevant, 5) == 3 / 3
    assert ndcg_at_k(rec_perfect, relevant, 5) == 1.0

    # Zero match
    rec_zero = ["p10", "p20", "p30"]
    assert precision_at_k(rec_zero, relevant, 3) == 0.0
    assert recall_at_k(rec_zero, relevant, 3) == 0.0
    assert ndcg_at_k(rec_zero, relevant, 3) == 0.0

    # Empty inputs
    assert precision_at_k([], relevant, 5) == 0.0
    assert recall_at_k([], relevant, 5) == 0.0
    assert ndcg_at_k([], relevant, 5) == 0.0


def test_fastapi_endpoints(client):
    # Root
    r_root = client.get("/")
    assert r_root.status_code == 200
    assert "supported_models" in r_root.json()

    # Health
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "healthy"

    # Known user recommendation
    r_rec = client.get("/recommend/1813?n=5&model=hybrid")
    assert r_rec.status_code == 200
    data = r_rec.json()
    assert len(data["recommendations"]) == 5
    assert data["is_known_user"] is True

    # Unknown user recommendation (cold start)
    r_cold = client.get("/recommend/cold_user_xyz?n=5&model=popularity")
    assert r_cold.status_code == 200
    assert len(r_cold.json()["recommendations"]) == 5
    assert r_cold.json()["is_known_user"] is False

    # Edge cases
    r_bad_k = client.get("/recommend/1813?n=0")
    assert r_bad_k.status_code in [400, 422]

    r_bad_model = client.get("/recommend/1813?model=non_existent_model")
    assert r_bad_model.status_code == 400


def test_user_segments_artifact():
    path = "data/processed/user_segment_summary.csv"
    df = pd.read_csv(path)
    assert len(df) == 3
    expected_segs = {"Low Activity", "Medium Activity", "High Activity"}
    assert set(df["segment"]) == expected_segs
    # Non-collapsed check
    assert (df["users"] > 0).all()
