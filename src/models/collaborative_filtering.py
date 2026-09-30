"""
Collaborative Filtering Recommendation Model
Project 3: Personalized Product Recommendation Model
User-based Collaborative Filtering using Nearest Neighbors (cosine metric)
on the authentic explicit rating matrix.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TRAIN_PATH = BASE_DIR / "data" / "interim" / "train_interactions.csv"
FALLBACK_PATH = BASE_DIR / "data" / "processed" / "interactions.csv"


class UserKNNRecommender:
    def __init__(self, data_path: Path | str | None = None, n_neighbors: int = 10):
        path = Path(data_path or (TRAIN_PATH if TRAIN_PATH.exists() else FALLBACK_PATH))
        print(f"Loading data from {path}...")
        self.df = pd.read_csv(path, dtype={"user_id": str, "product_id": str})
        self.n_neighbors = n_neighbors

        self.user_ids = self.df["user_id"].unique()
        self.product_ids = self.df["product_id"].unique()

        self.user_to_index = {u: i for i, u in enumerate(self.user_ids)}
        self.index_to_user = {i: u for i, u in enumerate(self.user_ids)}
        self.product_to_index = {p: i for i, p in enumerate(self.product_ids)}
        self.index_to_product = {i: p for i, p in enumerate(self.product_ids)}

        rows = self.df["user_id"].map(self.user_to_index)
        cols = self.df["product_id"].map(self.product_to_index)
        ratings = self.df["rating"].astype(np.float32)

        self.user_item_matrix = csr_matrix(
            (ratings, (rows, cols)),
            shape=(len(self.user_ids), len(self.product_ids))
        )

        self.knn = NearestNeighbors(
            metric="cosine",
            algorithm="brute",
            n_neighbors=min(self.n_neighbors, len(self.user_ids))
        )
        self.knn.fit(self.user_item_matrix)
        self.user_seen = self.df.groupby("user_id")["product_id"].apply(set).to_dict()

    def recommend(self, user_id: str, n: int = 10, exclude_seen: bool = True) -> list[tuple[str, float]]:
        user_id = str(user_id)
        if user_id not in self.user_to_index:
            return []

        u_idx = self.user_to_index[user_id]
        distances, indices = self.knn.kneighbors(
            self.user_item_matrix[u_idx],
            n_neighbors=min(self.n_neighbors, len(self.user_ids))
        )

        seen = self.user_seen.get(user_id, set()) if exclude_seen else set()
        scores = {}
        for dist, n_idx in zip(distances[0], indices[0]):
            if n_idx == u_idx:
                continue
            sim = max(0.0, 1.0 - dist)
            row = self.user_item_matrix[n_idx]
            for p_idx, r in zip(row.indices, row.data):
                pid = self.index_to_product[p_idx]
                if pid in seen:
                    continue
                scores[pid] = scores.get(pid, 0.0) + (sim * r)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return ranked


if __name__ == "__main__":
    cf = UserKNNRecommender()
    print("User-kNN Recommender initialized.")
    sample_user = cf.user_ids[0]
    recs = cf.recommend(sample_user, n=5)
    print(f"Top 5 recommendations for user {sample_user}:")
    for pid, sc in recs:
        print(f"  Product {pid}: score = {sc:.4f}")