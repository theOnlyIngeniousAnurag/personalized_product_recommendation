"""
Matrix Factorization Recommendation Model
Project 3: Personalized Product Recommendation Model
TruncatedSVD Matrix Factorization trained on authentic explicit rating matrix.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TRAIN_PATH = BASE_DIR / "data" / "interim" / "train_interactions.csv"
FALLBACK_PATH = BASE_DIR / "data" / "processed" / "interactions.csv"


class TruncatedSVDRecommender:
    def __init__(self, data_path: Path | str | None = None, n_components: int = 20):
        path = Path(data_path or (TRAIN_PATH if TRAIN_PATH.exists() else FALLBACK_PATH))
        print(f"Loading data from {path}...")
        self.df = pd.read_csv(path, dtype={"user_id": str, "product_id": str})
        self.n_components = n_components

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

        n_comp = min(self.n_components, min(self.user_item_matrix.shape) - 1)
        self.svd = TruncatedSVD(n_components=n_comp, random_state=42)
        self.user_factors = self.svd.fit_transform(self.user_item_matrix)
        self.item_factors = self.svd.components_
        self.user_seen = self.df.groupby("user_id")["product_id"].apply(set).to_dict()

    def recommend(self, user_id: str, n: int = 10, exclude_seen: bool = True) -> list[tuple[str, float]]:
        user_id = str(user_id)
        if user_id not in self.user_to_index:
            return []

        u_idx = self.user_to_index[user_id]
        u_vector = self.user_factors[u_idx]
        predicted_ratings = np.dot(u_vector, self.item_factors)

        seen = self.user_seen.get(user_id, set()) if exclude_seen else set()
        scores = {}
        for p_idx, score in enumerate(predicted_ratings):
            pid = self.index_to_product[p_idx]
            if pid in seen:
                continue
            scores[pid] = float(score)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return ranked


if __name__ == "__main__":
    svd = TruncatedSVDRecommender()
    print("SVD Recommender initialized.")
    sample_user = svd.user_ids[0]
    recs = svd.recommend(sample_user, n=5)
    print(f"Top 5 SVD recommendations for user {sample_user}:")
    for pid, sc in recs:
        print(f"  Product {pid}: score = {sc:.4f}")