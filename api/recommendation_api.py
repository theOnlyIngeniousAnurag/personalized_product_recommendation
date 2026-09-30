from pathlib import Path
import sys
from typing import Optional
from fastapi import FastAPI, HTTPException, Query

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.recommendation.recommendation_engine import RecommendationEngine

# ---------------------------------------------------------
# Create FastAPI application
# ---------------------------------------------------------
app = FastAPI(
    title="Personalized Product Recommendation API",
    description=(
        "Production REST API for personalized product recommendations "
        "supporting Popularity, Collaborative Filtering, Matrix Factorization, "
        "Content-Based, and Hybrid models with cold-start fallbacks."
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
        "default_model": "Hybrid Recommendation",
        "supported_models": [
            "hybrid",
            "collaborative",
            "matrix_factorization",
            "content",
            "popularity"
        ],
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
    n: int = Query(default=10, ge=1, le=50, description="Number of recommendations (1-50)"),
    model: Optional[str] = Query(
        default="hybrid",
        description="Model choice: hybrid, collaborative, matrix_factorization, content, popularity"
    )
):
    user_id = str(user_id).strip()
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="user_id cannot be empty."
        )

    model_key = (model or "hybrid").lower().strip()
    valid_models = {
        "hybrid": engine.recommend_hybrid,
        "collaborative": engine.recommend_collaborative,
        "cf": engine.recommend_collaborative,
        "matrix_factorization": engine.recommend_matrix_factorization,
        "svd": engine.recommend_matrix_factorization,
        "mf": engine.recommend_matrix_factorization,
        "content": engine.recommend_content,
        "content_based": engine.recommend_content,
        "popularity": engine.recommend_popularity
    }

    if model_key not in valid_models:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model '{model}'. Supported models: {list(valid_models.keys())}"
        )

    try:
        rec_fn = valid_models[model_key]
        recommendations = rec_fn(user_id=user_id, n=n)

        # Convert NaN values to None for valid JSON output
        recommendations = recommendations.where(
            recommendations.notna(),
            None
        )

        is_known_user = user_id in engine.user_to_index
        return {
            "user_id": user_id,
            "is_known_user": is_known_user,
            "model_requested": model_key,
            "number_of_recommendations": len(recommendations),
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
        "recommendation_engine": "loaded",
        "total_users": len(engine.user_ids),
        "total_catalog_items": len(engine.products)
    }