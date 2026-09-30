"""
Hybrid Recommendation Model
Project 3: Personalized Product Recommendation Model
Combines Collaborative Filtering (User-kNN), Content-Based (TF-IDF),
and Popularity Baseline with deterministic fallback for cold-start cases.
"""

from pathlib import Path
import pandas as pd
from src.recommendation.recommendation_engine import RecommendationEngine


def run_hybrid_demo(user_id: str = "1813", n: int = 10):
    print("=" * 60)
    print("HYBRID RECOMMENDATION MODEL")
    print("=" * 60)

    engine = RecommendationEngine()
    recs = engine.recommend(user_id=user_id, n=n)

    print(f"\nRecommendations for User {user_id}:")
    print(recs.to_string(index=False))
    return recs


if __name__ == "__main__":
    run_hybrid_demo()