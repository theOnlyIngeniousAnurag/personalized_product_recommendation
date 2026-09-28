from fastapi import FastAPI, HTTPException
from pathlib import Path
import sys


# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Import recommendation engine
# ---------------------------------------------------------

from src.recommendation.recommendation_engine import (
    RecommendationEngine
)


# ---------------------------------------------------------
# Create FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Personalized Product Recommendation API",
    description=(
        "API for generating personalized product "
        "recommendations using a hybrid recommendation model."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# Load recommendation engine
# ---------------------------------------------------------

engine = RecommendationEngine()


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Personalized Product Recommendation API",
        "status": "running",
        "model": "Hybrid Recommendation",
        "weights": {
            "collaborative": 0.50,
            "content": 0.30,
            "popularity": 0.20
        }
    }


# ---------------------------------------------------------
# Recommendation endpoint
# ---------------------------------------------------------

@app.get("/recommend/{user_id}")
def recommend_products(
    user_id: str,
    n: int = 10
):

    if n < 1:
        raise HTTPException(
            status_code=400,
            detail="n must be greater than 0."
        )

    if n > 50:
        raise HTTPException(
            status_code=400,
            detail="n cannot be greater than 50."
        )

    try:

        recommendations = engine.recommend(
            user_id=user_id,
            n=n
        )

        # Convert NaN values to None
        recommendations = recommendations.where(
            recommendations.notna(),
            None
        )

        return {
            "user_id": user_id,
            "number_of_recommendations": len(
                recommendations
            ),
            "recommendations": recommendations.to_dict(
                orient="records"
            )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "recommendation_engine": "loaded"
    }