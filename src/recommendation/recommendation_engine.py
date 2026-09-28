import pandas as pd
import numpy as np

from pathlib import Path
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:

    def __init__(self):

        # ---------------------------------------------------------
        # Project paths
        # ---------------------------------------------------------

        self.base_dir = Path(__file__).resolve().parents[2]

        self.interactions_file = (
            self.base_dir
            / "data"
            / "processed"
            / "interactions.csv"
        )

        self.products_file = (
            self.base_dir
            / "data"
            / "processed"
            / "products.csv"
        )

        self.popular_file = (
            self.base_dir
            / "data"
            / "processed"
            / "popular_products.csv"
        )

        # ---------------------------------------------------------
        # Load data
        # ---------------------------------------------------------

        print("Loading recommendation data...")

        self.interactions = pd.read_csv(
            self.interactions_file
        )

        self.products = pd.read_csv(
            self.products_file
        )

        self.popular_products = pd.read_csv(
            self.popular_file
        )

        # ---------------------------------------------------------
        # Standardize IDs
        # ---------------------------------------------------------

        self.interactions["user_id"] = (
            self.interactions["user_id"].astype(str)
        )

        self.interactions["product_id"] = (
            self.interactions["product_id"].astype(str)
        )

        self.products["product_id"] = (
            self.products["product_id"].astype(str)
        )

        self.popular_products["product_id"] = (
            self.popular_products["product_id"].astype(str)
        )

        # ---------------------------------------------------------
        # Create user-item matrix
        # ---------------------------------------------------------

        self.user_ids = (
            self.interactions["user_id"]
            .drop_duplicates()
            .tolist()
        )

        self.product_ids = (
            self.interactions["product_id"]
            .drop_duplicates()
            .tolist()
        )

        self.user_to_index = {
            user_id: index
            for index, user_id in enumerate(self.user_ids)
        }

        self.product_to_index = {
            product_id: index
            for index, product_id in enumerate(self.product_ids)
        }

        rows = self.interactions["user_id"].map(
            self.user_to_index
        )

        cols = self.interactions["product_id"].map(
            self.product_to_index
        )

        values = self.interactions["rating"].astype(float)

        self.user_item_matrix = csr_matrix(
            (
                values,
                (rows, cols)
            ),
            shape=(
                len(self.user_ids),
                len(self.product_ids)
            )
        )

        # ---------------------------------------------------------
        # Collaborative filtering model
        # ---------------------------------------------------------

        self.knn_model = NearestNeighbors(
            metric="cosine",
            algorithm="brute",
            n_neighbors=6
        )

        self.knn_model.fit(
            self.user_item_matrix
        )

        # ---------------------------------------------------------
        # Content-based model
        # ---------------------------------------------------------

        product_names = (
            self.products["product_name"]
            .fillna("")
            .astype(str)
        )

        self.tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=30000
        )

        self.tfidf_matrix = self.tfidf.fit_transform(
            product_names
        )

        # ---------------------------------------------------------
        # Product index
        # ---------------------------------------------------------

        self.product_index = pd.Series(
            self.products.index,
            index=self.products["product_id"]
        )

        print("Recommendation engine loaded successfully.")

    # ============================================================
    # USER HISTORY
    # ============================================================

    def get_user_history(self, user_id):

        user_id = str(user_id)

        history = self.interactions[
            self.interactions["user_id"] == user_id
        ]

        return set(
            history["product_id"].tolist()
        )

    # ============================================================
    # POPULARITY SCORE
    # ============================================================

    def get_popularity_scores(self, candidates):

        popular = self.popular_products[
            self.popular_products["product_id"].isin(candidates)
        ].copy()

        if popular.empty:
            return {}

        if "average_rating" in popular.columns:
            rating_score = (
                popular["average_rating"] / 5.0
            )
        else:
            rating_score = pd.Series(
                0.5,
                index=popular.index
            )

        if "interaction_count" in popular.columns:

            max_interactions = (
                popular["interaction_count"].max()
            )

            if max_interactions > 0:

                interaction_score = (
                    popular["interaction_count"]
                    / max_interactions
                )

            else:

                interaction_score = pd.Series(
                    0.0,
                    index=popular.index
                )

        else:

            interaction_score = pd.Series(
                0.0,
                index=popular.index
            )

        popular["popularity_score"] = (
            0.5 * rating_score
            + 0.5 * interaction_score
        )

        return dict(
            zip(
                popular["product_id"],
                popular["popularity_score"]
            )
        )

    # ============================================================
    # COLLABORATIVE FILTERING
    # ============================================================

    def collaborative_scores(
        self,
        user_id,
        candidates
    ):

        user_id = str(user_id)

        if user_id not in self.user_to_index:
            return {}

        user_index = self.user_to_index[user_id]

        distances, indices = (
            self.knn_model.kneighbors(
                self.user_item_matrix[user_index],
                n_neighbors=6
            )
        )

        scores = {}

        for distance, neighbor_index in zip(
            distances[0],
            indices[0]
        ):

            if neighbor_index == user_index:
                continue

            similarity = 1.0 - distance

            neighbor_vector = (
                self.user_item_matrix[
                    neighbor_index
                ]
            )

            products = (
                neighbor_vector.indices
            )

            ratings = (
                neighbor_vector.data
            )

            for product_index, rating in zip(
                products,
                ratings
            ):

                product_id = (
                    self.product_ids[
                        product_index
                    ]
                )

                if product_id in candidates:

                    scores[product_id] = (
                        scores.get(
                            product_id,
                            0
                        )
                        + similarity * rating
                    )

        return scores

    # ============================================================
    # CONTENT-BASED RECOMMENDATION
    # ============================================================

    def content_scores(
        self,
        user_id,
        candidates
    ):

        user_id = str(user_id)

        history = self.interactions[
            self.interactions["user_id"] == user_id
        ].copy()

        if history.empty:
            return {}

        # Use the highest-rated products as seeds
        history = history.sort_values(
            "rating",
            ascending=False
        ).head(5)

        scores = {}

        for product_id in history["product_id"]:

            if product_id not in self.product_index:
                continue

            product_index = self.product_index[
                product_id
            ]

            similarity = cosine_similarity(
                self.tfidf_matrix[
                    product_index
                ],
                self.tfidf_matrix
            ).flatten()

            top_indices = np.argsort(
                similarity
            )[::-1][:50]

            for index in top_indices:

                candidate_id = (
                    self.products.iloc[
                        index
                    ]["product_id"]
                )

                if candidate_id in candidates:

                    scores[candidate_id] = max(
                        scores.get(
                            candidate_id,
                            0
                        ),
                        float(similarity[index])
                    )

        return scores

    # ============================================================
    # NORMALIZE SCORES
    # ============================================================

    def normalize_scores(self, scores):

        if not scores:
            return {}

        maximum = max(
            scores.values()
        )

        minimum = min(
            scores.values()
        )

        if maximum == minimum:

            return {
                key: 1.0
                for key in scores
            }

        return {
            key: (
                (value - minimum)
                / (maximum - minimum)
            )
            for key, value in scores.items()
        }

    # ============================================================
    # FINAL HYBRID RECOMMENDATION
    # ============================================================

    def recommend(
        self,
        user_id,
        n=10
    ):

        user_id = str(user_id)

        history = self.get_user_history(
            user_id
        )

        # --------------------------------------------------------
        # New user
        # --------------------------------------------------------

        if not history:

            recommendations = (
                self.popular_products
                .head(n)
                .copy()
            )

            recommendations[
                "recommendation_reason"
            ] = "Popular products for new user"

            return recommendations

        # --------------------------------------------------------
        # Candidate products
        # --------------------------------------------------------

        popular_candidates = (
            self.popular_products
            .head(1000)
        )

        candidates = set(
            popular_candidates[
                "product_id"
            ]
        )

        # Remove products already seen
        candidates -= history

        # --------------------------------------------------------
        # Calculate three scores
        # --------------------------------------------------------

        collaborative = (
            self.collaborative_scores(
                user_id,
                candidates
            )
        )

        content = (
            self.content_scores(
                user_id,
                candidates
            )
        )

        popularity = (
            self.get_popularity_scores(
                candidates
            )
        )

        # --------------------------------------------------------
        # Normalize
        # --------------------------------------------------------

        collaborative = (
            self.normalize_scores(
                collaborative
            )
        )

        content = (
            self.normalize_scores(
                content
            )
        )

        popularity = (
            self.normalize_scores(
                popularity
            )
        )

        # --------------------------------------------------------
        # Hybrid score
        #
        # 50% Collaborative
        # 30% Content
        # 20% Popularity
        # --------------------------------------------------------

        all_products = (
            set(collaborative)
            | set(content)
            | set(popularity)
        )

        final_scores = {}

        for product_id in all_products:

            collaborative_score = (
                collaborative.get(
                    product_id,
                    0.0
                )
            )

            content_score = (
                content.get(
                    product_id,
                    0.0
                )
            )

            popularity_score = (
                popularity.get(
                    product_id,
                    0.0
                )
            )

            final_scores[product_id] = (
                0.50 * collaborative_score
                + 0.30 * content_score
                + 0.20 * popularity_score
            )

        # --------------------------------------------------------
        # Rank products
        # --------------------------------------------------------

        ranked_products = sorted(
            final_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]

        recommendation_ids = [
            product_id
            for product_id, score
            in ranked_products
        ]

        recommendation_scores = [
            score
            for product_id, score
            in ranked_products
        ]

        # --------------------------------------------------------
        # Create output
        # --------------------------------------------------------

        recommendations = (
            self.products[
                self.products["product_id"].isin(
                    recommendation_ids
                )
            ]
            .copy()
        )

        score_map = dict(
            ranked_products
        )

        recommendations[
            "recommendation_score"
        ] = recommendations[
            "product_id"
        ].map(score_map)

        recommendations = (
            recommendations
            .sort_values(
                "recommendation_score",
                ascending=False
            )
            .head(n)
        )

        recommendations[
            "recommendation_reason"
        ] = (
            "Hybrid: 50% collaborative + "
            "30% content + 20% popularity"
        )

        return recommendations

    # ============================================================
    # SIMPLE LIST
    # ============================================================

    def get_recommendation_list(
        self,
        user_id,
        n=10
    ):

        recommendations = self.recommend(
            user_id,
            n
        )

        return (
            recommendations[
                "product_id"
            ]
            .tolist()
        )


if __name__ == "__main__":

    engine = RecommendationEngine()

    recommendations = engine.recommend(
        user_id="1813",
        n=10
    )

    print("\nHybrid Recommendations")
    print("=" * 70)

    print(
        recommendations[
            [
                "product_id",
                "recommendation_score",
                "recommendation_reason"
            ]
        ].to_string(index=False)
    )