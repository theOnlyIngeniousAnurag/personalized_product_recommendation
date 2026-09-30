"""
Canonical Recommendation Engine
Project 3: Personalized Product Recommendation Model
Unified architecture providing:
1. Popularity Baseline Recommender
2. User-kNN Collaborative Filtering
3. TruncatedSVD Matrix Factorization
4. Content-Based (TF-IDF + Cosine Similarity) Recommender
5. Hybrid & Cold-Start Fallback Recommender
6. Standard Evaluation & API Inference Interfaces
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:
    """
    Unified Recommendation Engine implementing all canonical recommendation strategies
    for the Monash FIT5212 authentic explicit-rating dataset.
    """

    def __init__(
        self,
        interactions_file: str | Path | None = None,
        products_file: str | Path | None = None,
        popular_file: str | Path | None = None,
        n_components: int = 20,
    ):
        self.base_dir = Path(__file__).resolve().parents[2]

        self.interactions_file = Path(
            interactions_file or (self.base_dir / "data" / "processed" / "interactions.csv")
        )
        self.products_file = Path(
            products_file or (self.base_dir / "data" / "processed" / "products.csv")
        )
        self.popular_file = Path(
            popular_file or (self.base_dir / "data" / "processed" / "popular_products.csv")
        )

        print(f"Loading recommendation data from {self.interactions_file.name}...")

        self.interactions = pd.read_csv(
            self.interactions_file,
            dtype={"user_id": str, "product_id": str}
        )
        self.products = pd.read_csv(
            self.products_file,
            dtype={"product_id": str}
        )
        self.popular_products = pd.read_csv(
            self.popular_file,
            dtype={"product_id": str}
        )

        # Standardize strings & drop nulls
        self.interactions["user_id"] = self.interactions["user_id"].astype(str)
        self.interactions["product_id"] = self.interactions["product_id"].astype(str)
        self.products["product_id"] = self.products["product_id"].astype(str)
        self.popular_products["product_id"] = self.popular_products["product_id"].astype(str)

        self.product_name_lookup = dict(
            zip(self.products["product_id"], self.products["product_name"].fillna("Unknown Product"))
        )

        # ---------------------------------------------------------
        # User-Item Interaction Matrix Construction
        # ---------------------------------------------------------
        self.user_ids = self.interactions["user_id"].drop_duplicates().tolist()
        self.product_ids = self.interactions["product_id"].drop_duplicates().tolist()

        self.user_to_index = {u: i for i, u in enumerate(self.user_ids)}
        self.index_to_user = {i: u for i, u in enumerate(self.user_ids)}
        self.product_to_index = {p: i for i, p in enumerate(self.product_ids)}
        self.index_to_product = {i: p for i, p in enumerate(self.product_ids)}

        rows = self.interactions["user_id"].map(self.user_to_index)
        cols = self.interactions["product_id"].map(self.product_to_index)
        ratings = self.interactions["rating"].astype(np.float32)

        self.user_item_matrix = csr_matrix(
            (ratings, (rows, cols)),
            shape=(len(self.user_ids), len(self.product_ids))
        )

        # ---------------------------------------------------------
        # Model 1: User-Based Collaborative Filtering (k-NN)
        # ---------------------------------------------------------
        self.n_neighbors = min(10, max(2, len(self.user_ids)))
        self.knn_model = NearestNeighbors(
            metric="cosine",
            algorithm="brute",
            n_neighbors=self.n_neighbors
        )
        self.knn_model.fit(self.user_item_matrix)

        # ---------------------------------------------------------
        # Model 2: Matrix Factorization (Truncated SVD)
        # ---------------------------------------------------------
        self.n_components = min(n_components, max(2, min(self.user_item_matrix.shape) - 1))
        self.svd = TruncatedSVD(
            n_components=self.n_components,
            random_state=42
        )
        self.user_factors = self.svd.fit_transform(self.user_item_matrix)
        self.item_factors = self.svd.components_

        # ---------------------------------------------------------
        # Model 3: Content-Based Recommender (TF-IDF + Cosine)
        # ---------------------------------------------------------
        product_names = self.products["product_name"].fillna("Unknown Product").astype(str)
        self.tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=30000
        )
        self.tfidf_matrix = self.tfidf.fit_transform(product_names)
        self.catalog_product_index = {
            pid: idx for idx, pid in enumerate(self.products["product_id"])
        }

        # User history cache for fast lookup
        self.user_history_map = (
            self.interactions.groupby("user_id")["product_id"]
            .apply(set)
            .to_dict()
        )
        self.user_history_ratings = (
            self.interactions.groupby("user_id")[["product_id", "rating"]]
            .apply(lambda g: dict(zip(g["product_id"], g["rating"])))
            .to_dict()
        )

        print(
            f"Recommendation engine initialized: {len(self.user_ids):,} users, "
            f"{len(self.product_ids):,} training items, {len(self.products):,} catalog items."
        )

    # ============================================================
    # HELPER UTILITIES
    # ============================================================

    def get_product_name(self, product_id: str | int) -> str:
        """Resolves authentic product name for a product_id from canonical catalog."""
        pid_str = str(product_id).strip()
        if pid_str in self.product_name_lookup:
            return self.product_name_lookup[pid_str]
        try:
            pid_int = int(pid_str)
            if pid_int in self.product_name_lookup:
                return self.product_name_lookup[pid_int]
        except (ValueError, TypeError):
            pass
        return f"Item {pid_str}"

    def get_user_history(self, user_id: str) -> set:
        """Returns set of product IDs already interacted with by the user."""
        return self.user_history_map.get(str(user_id), set())

    def _normalize_dict_scores(self, scores: dict[str, float]) -> dict[str, float]:
        """Min-max normalizes a dictionary of scores to [0.0, 1.0]."""
        if not scores:
            return {}
        vals = np.array(list(scores.values()), dtype=float)
        min_v = vals.min()
        max_v = vals.max()
        if max_v == min_v:
            return {k: 1.0 for k in scores}
        diff = max_v - min_v
        return {k: float((v - min_v) / diff) for k, v in scores.items()}

    def _format_dataframe(self, ranked_items: list[tuple[str, float]], reason: str, n: int) -> pd.DataFrame:
        """Formats top-N ranked items into standardized output DataFrame."""
        top_items = ranked_items[:n]
        if not top_items:
            # Fallback to popular products if empty
            return self.recommend_popularity(n=n, reason="Popularity fallback (empty recommendation pool)")

        pids = [str(item[0]) for item in top_items]
        scores = [round(float(item[1]), 4) for item in top_items]
        names = [self.get_product_name(pid) for pid in pids]

        df = pd.DataFrame({
            "product_id": pids,
            "product_name": names,
            "recommendation_score": scores,
            "recommendation_reason": [reason] * len(pids)
        })
        return df

    # ============================================================
    # 1. POPULARITY RECOMMENDER
    # ============================================================

    def recommend_popularity(
        self,
        user_id: str | None = None,
        n: int = 10,
        exclude_seen: bool = True,
        reason: str | None = None
    ) -> pd.DataFrame:
        """
        Generates popularity baseline recommendations using global popularity rank.
        Deterministic and fast fallback for cold users.
        """
        seen = self.get_user_history(str(user_id)) if (user_id and exclude_seen) else set()
        
        candidates = []
        for _, row in self.popular_products.iterrows():
            pid = str(row["product_id"])
            if pid in seen:
                continue
            score = float(row.get("popularity_score", 1.0 / (len(candidates) + 1)))
            candidates.append((pid, score))
            if len(candidates) >= n:
                break

        rec_reason = reason or ("Popularity baseline (new/cold user)" if user_id not in self.user_to_index else "Popularity baseline")
        return self._format_dataframe(candidates, rec_reason, n)

    # ============================================================
    # 2. COLLABORATIVE FILTERING (User-kNN)
    # ============================================================

    def collaborative_scores(
        self,
        user_id: str,
        candidates: set[str] | None = None
    ) -> dict[str, float]:
        """Calculates User-kNN collaborative filtering scores."""
        user_id = str(user_id)
        if user_id not in self.user_to_index:
            return {}

        user_idx = self.user_to_index[user_id]
        distances, indices = self.knn_model.kneighbors(
            self.user_item_matrix[user_idx],
            n_neighbors=self.n_neighbors
        )

        scores = {}
        for dist, neighbor_idx in zip(distances[0], indices[0]):
            if neighbor_idx == user_idx:
                continue
            sim = max(0.0, 1.0 - dist)
            neighbor_vec = self.user_item_matrix[neighbor_idx]
            n_pids = neighbor_vec.indices
            n_ratings = neighbor_vec.data

            for p_idx, rating in zip(n_pids, n_ratings):
                pid = self.index_to_product[p_idx]
                if candidates is not None and pid not in candidates:
                    continue
                scores[pid] = scores.get(pid, 0.0) + (sim * rating)

        return scores

    def recommend_collaborative(
        self,
        user_id: str,
        n: int = 10,
        exclude_seen: bool = True
    ) -> pd.DataFrame:
        """Generates collaborative filtering recommendations using User-kNN."""
        user_id = str(user_id)
        seen = self.get_user_history(user_id) if exclude_seen else set()

        if user_id not in self.user_to_index:
            return self.recommend_popularity(user_id=user_id, n=n, exclude_seen=exclude_seen)

        raw_scores = self.collaborative_scores(user_id)
        for s in seen:
            raw_scores.pop(s, None)

        if not raw_scores:
            return self.recommend_popularity(user_id=user_id, n=n, exclude_seen=exclude_seen, reason="Popularity fallback (no collaborative neighbors found)")

        normalized = self._normalize_dict_scores(raw_scores)
        ranked = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
        return self._format_dataframe(ranked, "Collaborative filtering (User-kNN)", n)

    # ============================================================
    # 3. MATRIX FACTORIZATION (TruncatedSVD)
    # ============================================================

    def matrix_factorization_scores(
        self,
        user_id: str,
        candidates: set[str] | None = None
    ) -> dict[str, float]:
        """Calculates TruncatedSVD latent factor prediction scores."""
        user_id = str(user_id)
        if user_id not in self.user_to_index:
            return {}

        user_idx = self.user_to_index[user_id]
        u_vector = self.user_factors[user_idx]  # shape: (n_components,)
        # Predicted ratings across all items in training matrix
        predicted = np.dot(u_vector, self.item_factors)  # shape: (n_items,)

        if candidates is not None:
            scores = {}
            for pid in candidates:
                if pid in self.product_to_index:
                    scores[pid] = float(predicted[self.product_to_index[pid]])
            return scores

        scores = {self.index_to_product[idx]: float(val) for idx, val in enumerate(predicted)}
        return scores

    def recommend_matrix_factorization(
        self,
        user_id: str,
        n: int = 10,
        exclude_seen: bool = True
    ) -> pd.DataFrame:
        """Generates matrix factorization recommendations using TruncatedSVD."""
        user_id = str(user_id)
        seen = self.get_user_history(user_id) if exclude_seen else set()

        if user_id not in self.user_to_index:
            return self.recommend_popularity(user_id=user_id, n=n, exclude_seen=exclude_seen)

        raw_scores = self.matrix_factorization_scores(user_id)
        for s in seen:
            raw_scores.pop(s, None)

        if not raw_scores:
            return self.recommend_popularity(user_id=user_id, n=n, exclude_seen=exclude_seen)

        normalized = self._normalize_dict_scores(raw_scores)
        ranked = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
        return self._format_dataframe(ranked, f"Matrix factorization (TruncatedSVD k={self.n_components})", n)

    # ============================================================
    # 4. CONTENT-BASED RECOMMENDER (TF-IDF + Cosine Similarity)
    # ============================================================

    def content_scores(
        self,
        user_id: str,
        candidates: set[str] | None = None,
        top_seeds: int = 5
    ) -> dict[str, float]:
        """Calculates content similarity scores using user's top-rated seeds."""
        user_id = str(user_id)
        user_ratings = self.user_history_ratings.get(user_id, {})
        if not user_ratings:
            return {}

        # Pick seeds sorted by rating descending
        sorted_seeds = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)[:top_seeds]
        scores = {}

        for seed_pid, seed_rating in sorted_seeds:
            if seed_pid not in self.catalog_product_index:
                continue
            seed_idx = self.catalog_product_index[seed_pid]
            sims = cosine_similarity(self.tfidf_matrix[seed_idx], self.tfidf_matrix).flatten()

            top_sim_indices = np.argpartition(sims, -50)[-50:]
            for c_idx in top_sim_indices:
                sim_score = float(sims[c_idx])
                if sim_score <= 0.0:
                    continue
                c_pid = self.products.iloc[c_idx]["product_id"]
                if candidates is not None and c_pid not in candidates:
                    continue
                weighted_sim = sim_score * (seed_rating / 5.0)
                scores[c_pid] = max(scores.get(c_pid, 0.0), weighted_sim)

        return scores

    def recommend_content(
        self,
        user_id: str,
        n: int = 10,
        exclude_seen: bool = True
    ) -> pd.DataFrame:
        """Generates content-based recommendations based on product text similarity."""
        user_id = str(user_id)
        seen = self.get_user_history(user_id) if exclude_seen else set()

        if user_id not in self.user_history_ratings:
            return self.recommend_popularity(user_id=user_id, n=n, exclude_seen=exclude_seen)

        raw_scores = self.content_scores(user_id)
        for s in seen:
            raw_scores.pop(s, None)

        if not raw_scores:
            return self.recommend_popularity(user_id=user_id, n=n, exclude_seen=exclude_seen, reason="Popularity fallback (no content seeds available)")

        normalized = self._normalize_dict_scores(raw_scores)
        ranked = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
        return self._format_dataframe(ranked, "Content-based (TF-IDF metadata)", n)

    # ============================================================
    # 5. HYBRID & COLD-START RECOMMENDER
    # ============================================================

    def get_popularity_scores(self, candidates: set[str]) -> dict[str, float]:
        """Calculates normalized popularity scores for a candidate set."""
        popular = self.popular_products[
            self.popular_products["product_id"].isin(candidates)
        ].copy()

        if popular.empty:
            return {}

        max_interactions = popular["interaction_count"].max() if "interaction_count" in popular.columns else 1
        max_interactions = max(1, max_interactions)

        scores = {}
        for _, row in popular.iterrows():
            pid = str(row["product_id"])
            rating_s = float(row.get("average_rating", 3.0)) / 5.0
            count_s = float(row.get("interaction_count", 0)) / max_interactions
            scores[pid] = 0.5 * rating_s + 0.5 * count_s

        return self._normalize_dict_scores(scores)

    def recommend_hybrid(
        self,
        user_id: str,
        n: int = 10,
        weights: dict[str, float] | None = None,
        exclude_seen: bool = True
    ) -> pd.DataFrame:
        """
        Generates robust hybrid recommendations with deterministic cold-start fallback.
        Default weights: 50% Collaborative (User-kNN), 30% Content-based, 20% Popularity.
        """
        user_id = str(user_id)
        history = self.get_user_history(user_id)

        # Cold / unknown user fallback
        if not history or user_id not in self.user_to_index:
            return self.recommend_popularity(
                user_id=user_id,
                n=n,
                exclude_seen=exclude_seen,
                reason="Popular products for new user"
            )

        if weights is None:
            weights = {"collaborative": 0.50, "content": 0.30, "popularity": 0.20}

        # Build candidate pool: top popular products + content candidates
        popular_candidates = set(self.popular_products.head(1000)["product_id"].astype(str))
        candidates = popular_candidates.copy()
        if exclude_seen:
            candidates -= history

        # Calculate constituent scores
        collab_scores = self._normalize_dict_scores(self.collaborative_scores(user_id, candidates))
        content_scores = self._normalize_dict_scores(self.content_scores(user_id, candidates))
        pop_scores = self.get_popularity_scores(candidates)

        all_candidate_pids = set(collab_scores) | set(content_scores) | set(pop_scores)
        if not all_candidate_pids:
            return self.recommend_popularity(user_id=user_id, n=n, exclude_seen=exclude_seen)

        w_collab = weights.get("collaborative", 0.50)
        w_content = weights.get("content", 0.30)
        w_pop = weights.get("popularity", 0.20)

        hybrid_scores = {}
        for pid in all_candidate_pids:
            score = (
                w_collab * collab_scores.get(pid, 0.0) +
                w_content * content_scores.get(pid, 0.0) +
                w_pop * pop_scores.get(pid, 0.0)
            )
            hybrid_scores[pid] = score

        ranked = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
        reason = f"Hybrid: {int(w_collab*100)}% collaborative + {int(w_content*100)}% content + {int(w_pop*100)}% popularity"
        return self._format_dataframe(ranked, reason, n)

    # Standard alias for backward compatibility
    def recommend(self, user_id: str, n: int = 10) -> pd.DataFrame:
        """Standard canonical recommendation method."""
        return self.recommend_hybrid(user_id=user_id, n=n)

    def get_recommendation_list(
        self,
        user_id: str,
        n: int = 10,
        model_type: str = "hybrid"
    ) -> list[str]:
        """Returns ordered list of product IDs for specified model type."""
        model_type = model_type.lower()
        if model_type == "popularity":
            df = self.recommend_popularity(user_id=user_id, n=n)
        elif model_type in ["collaborative", "cf"]:
            df = self.recommend_collaborative(user_id=user_id, n=n)
        elif model_type in ["matrix_factorization", "svd", "mf"]:
            df = self.recommend_matrix_factorization(user_id=user_id, n=n)
        elif model_type in ["content", "content_based"]:
            df = self.recommend_content(user_id=user_id, n=n)
        else:
            df = self.recommend_hybrid(user_id=user_id, n=n)

        return df["product_id"].tolist()


if __name__ == "__main__":
    engine = RecommendationEngine()
    print("\n--- Popularity Baseline ---")
    print(engine.recommend_popularity("1813", n=3).to_string(index=False))
    print("\n--- Collaborative Filtering ---")
    print(engine.recommend_collaborative("1813", n=3).to_string(index=False))
    print("\n--- Matrix Factorization (SVD) ---")
    print(engine.recommend_matrix_factorization("1813", n=3).to_string(index=False))
    print("\n--- Content-Based ---")
    print(engine.recommend_content("1813", n=3).to_string(index=False))
    print("\n--- Canonical Hybrid ---")
    print(engine.recommend("1813", n=3).to_string(index=False))