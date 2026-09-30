"""
Popularity-Based Recommendation Model
Project 3: Personalized Product Recommendation Model
Computes global popularity ranking from authentic training data.
Formula: popularity_score = average_rating * interaction_count (with min_interactions >= 5)
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TRAIN_INTERACTIONS_PATH = BASE_DIR / "data" / "interim" / "train_interactions.csv"
PRODUCTS_PATH = BASE_DIR / "data" / "processed" / "products.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "popular_products.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_popularity_ranking(
    min_interactions: int = 5,
    train_path: Path | str | None = None,
    output_path: Path | str | None = None
) -> pd.DataFrame:
    train_file = Path(train_path or TRAIN_INTERACTIONS_PATH)
    out_file = Path(output_path or OUTPUT_PATH)

    print("=" * 60)
    print("POPULARITY-BASED RECOMMENDATION MODEL")
    print("=" * 60)

    if train_file.exists():
        print(f"Aggregating popularity directly from training interactions: {train_file}")
        df = pd.read_csv(train_file, dtype={"user_id": str, "product_id": str})
        grouped = df.groupby(["product_id", "product_name"]).agg(
            interaction_count=("rating", "count"),
            unique_users=("user_id", "nunique"),
            average_rating=("rating", "mean")
        ).reset_index()
    elif PRODUCTS_PATH.exists():
        print(f"Loading existing product aggregations from: {PRODUCTS_PATH}")
        grouped = pd.read_csv(PRODUCTS_PATH, dtype={"product_id": str})
    else:
        raise FileNotFoundError(f"Neither {train_file} nor {PRODUCTS_PATH} exists.")

    print(f"Total candidate products: {len(grouped):,}")

    # Filter for minimum interactions
    popular = grouped[grouped["interaction_count"] >= min_interactions].copy()
    print(f"Products with at least {min_interactions} interactions: {len(popular):,}")

    # Compute popularity score
    popular["popularity_score"] = popular["average_rating"] * popular["interaction_count"]
    popular = popular.sort_values(by="popularity_score", ascending=False).reset_index(drop=True)
    popular["rank"] = range(1, len(popular) + 1)

    columns = [
        "rank",
        "product_id",
        "product_name",
        "interaction_count",
        "unique_users",
        "average_rating",
        "popularity_score"
    ]
    popular = popular[[col for col in columns if col in popular.columns]]

    popular.to_csv(out_file, index=False)
    print(f"Saved popularity rankings to {out_file}")

    print("\n" + "=" * 60)
    print("TOP 10 POPULAR PRODUCTS")
    print("=" * 60)
    print(popular.head(10).to_string(index=False))
    return popular


if __name__ == "__main__":
    build_popularity_ranking()