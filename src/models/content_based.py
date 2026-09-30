"""
Content-Based Recommendation Model
Project 3: Personalized Product Recommendation Model
Product text representation via TF-IDF on product_name,
and cosine similarity recommendation using user seed items.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRODUCTS_PATH = BASE_DIR / "data" / "processed" / "products.csv"
TRAIN_PATH = BASE_DIR / "data" / "interim" / "train_interactions.csv"
FALLBACK_PATH = BASE_DIR / "data" / "processed" / "interactions.csv"


class ContentBasedRecommender:
    def __init__(
        self,
        products_path: Path | str | None = None,
        interactions_path: Path | str | None = None,
        max_features: int = 30000
    ):
        p_path = Path(products_path or PRODUCTS_PATH)
        i_path = Path(interactions_path or (TRAIN_PATH if TRAIN_PATH.exists() else FALLBACK_PATH))

        print(f"Loading products from {p_path}...")
        self.products = pd.read_csv(p_path, dtype={"product_id": str})
        self.products["product_id"] = self.products["product_id"].astype(str)
        product_names = self.products["product_name"].fillna("Unknown Product").astype(str)

        print(f"Fitting TF-IDF on {len(self.products):,} product titles...")
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=max_features)
        self.tfidf_matrix = self.vectorizer.fit_transform(product_names)
        self.product_index = {pid: idx for idx, pid in enumerate(self.products["product_id"])}

        if i_path.exists():
            interactions = pd.read_csv(i_path, dtype={"user_id": str, "product_id": str})
            self.user_history = (
                interactions.groupby("user_id")[["product_id", "rating"]]
                .apply(lambda g: dict(zip(g["product_id"], g["rating"])))
                .to_dict()
            )
            self.user_seen = interactions.groupby("user_id")["product_id"].apply(set).to_dict()
        else:
            self.user_history = {}
            self.user_seen = {}

    def similar_items(self, product_id: str, top_n: int = 10) -> list[tuple[str, float]]:
        """Returns top_n items similar to given product_id."""
        product_id = str(product_id)
        if product_id not in self.product_index:
            return []
        idx = self.product_index[product_id]
        sims = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        top_indices = np.argsort(sims)[::-1][1 : top_n + 1]
        return [(self.products.iloc[i]["product_id"], float(sims[i])) for i in top_indices]

    def recommend(
        self,
        user_id: str,
        n: int = 10,
        exclude_seen: bool = True,
        top_seeds: int = 5
    ) -> list[tuple[str, float]]:
        """Recommends products based on user's top-rated seed products."""
        user_id = str(user_id)
        ratings = self.user_history.get(user_id, {})
        if not ratings:
            return []

        seen = self.user_seen.get(user_id, set()) if exclude_seen else set()
        sorted_seeds = sorted(ratings.items(), key=lambda x: x[1], reverse=True)[:top_seeds]

        candidate_scores = {}
        for seed_pid, r in sorted_seeds:
            if seed_pid not in self.product_index:
                continue
            idx = self.product_index[seed_pid]
            sims = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
            top_sims = np.argpartition(sims, -50)[-50:]
            for c_idx in top_sims:
                c_pid = self.products.iloc[c_idx]["product_id"]
                if c_pid in seen:
                    continue
                score = float(sims[c_idx]) * (r / 5.0)
                if score > 0:
                    candidate_scores[c_pid] = max(candidate_scores.get(c_pid, 0.0), score)

        ranked = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return ranked


if __name__ == "__main__":
    cb = ContentBasedRecommender()
    print("Content-based recommender initialized.")
    sample_pid = cb.products.iloc[0]["product_id"]
    sims = cb.similar_items(sample_pid, top_n=3)
    print(f"Similar items to {sample_pid}: {sims}")