import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personalized Product Recommendation",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🛍️ Personalized Product Recommendation System")

st.write(
    "A hybrid recommendation system using "
    "product similarity and popularity."
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    interactions = pd.read_csv(
        "data/processed/interactions.csv",
        dtype={"user_id": str, "product_id": str}
    )

    products = pd.read_csv(
        "data/processed/products.csv",
        dtype={"product_id": str}
    )

    popular_products = pd.read_csv(
        "data/processed/popular_products.csv",
        dtype={"product_id": str}
    )

    return (
        interactions,
        products,
        popular_products
    )


(
    interactions,
    products,
    popular_products
) = load_data()


# ============================================================
# PREPARE PRODUCT DATA
# ============================================================

products["product_name"] = (
    products["product_name"]
    .fillna("Unknown Product")
)

products["product_text"] = (
    products["product_name"]
    .astype(str)
    .str.lower()
)


# ============================================================
# CANONICAL RECOMMENDATION ENGINE INTEGRATION
# ============================================================

import sys
from pathlib import Path
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.recommendation.recommendation_engine import RecommendationEngine

@st.cache_resource
def get_recommendation_engine():
    return RecommendationEngine()

engine = get_recommendation_engine()


def generate_recommendations(
    user_id,
    number_of_recommendations,
    model_choice="Hybrid (Collaborative + Content + Popularity)"
):
    user_id = str(user_id)
    is_new_user = user_id not in engine.user_to_index

    if "Collaborative" in model_choice:
        rec_df = engine.recommend_collaborative(user_id, n=number_of_recommendations)
    elif "Matrix Factorization" in model_choice or "SVD" in model_choice:
        rec_df = engine.recommend_matrix_factorization(user_id, n=number_of_recommendations)
    elif "Content" in model_choice:
        rec_df = engine.recommend_content(user_id, n=number_of_recommendations)
    elif "Popularity" in model_choice:
        rec_df = engine.recommend_popularity(user_id, n=number_of_recommendations)
    else:
        rec_df = engine.recommend_hybrid(user_id, n=number_of_recommendations)

    recommendations = [
        {
            "product_id": str(row["product_id"]),
            "product_name": str(row["product_name"]),
            "score": float(row["recommendation_score"]),
            "reason": str(row.get("recommendation_reason", "Recommended"))
        }
        for _, row in rec_df.iterrows()
    ]
    return recommendations, is_new_user


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Recommendation Settings")

user_id = st.sidebar.text_input(
    "Enter User ID",
    value="1813"
)

number_of_recommendations = st.sidebar.slider(
    "Number of Recommendations",
    min_value=5,
    max_value=20,
    value=10
)

model_choice = st.sidebar.selectbox(
    "Recommendation Model",
    [
        "Hybrid (Collaborative + Content + Popularity)",
        "Collaborative Filtering (User-kNN)",
        "Matrix Factorization (TruncatedSVD)",
        "Content-Based (TF-IDF)",
        "Popularity Baseline"
    ],
    index=0
)

generate_button = st.sidebar.button(
    "Generate Recommendations",
    type="primary"
)


# ============================================================
# INFORMATION CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "👥 Users",
        f"{interactions['user_id'].nunique():,}"
    )

with col2:

    st.metric(
        "🛍️ Products",
        f"{products['product_id'].nunique():,}"
    )

with col3:

    st.metric(
        "🔄 Interactions",
        f"{len(interactions):,}"
    )


st.divider()


# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

st.header("📊 Recommendation Analytics")

tab1, tab2, tab3 = st.tabs(
    [
        "⭐ Rating Analysis",
        "👥 User Segments",
        "🔥 Popular Products"
    ]
)


# ============================================================
# TAB 1 - RATING ANALYSIS
# ============================================================

with tab1:

    st.subheader("⭐ Rating Distribution")

    rating_distribution = (
        interactions["rating"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_distribution.columns = [
        "Rating",
        "Count"
    ]

    st.bar_chart(
        rating_distribution.set_index("Rating")
    )

    st.subheader("Rating Statistics")

    rating_col1, rating_col2, rating_col3 = st.columns(3)

    with rating_col1:

        st.metric(
            "Average Rating",
            f"{interactions['rating'].mean():.2f}"
        )

    with rating_col2:

        st.metric(
            "Highest Rating",
            f"{interactions['rating'].max():.0f}"
        )

    with rating_col3:

        st.metric(
            "Lowest Rating",
            f"{interactions['rating'].min():.0f}"
        )


# ============================================================
# TAB 2 - USER SEGMENTS
# ============================================================

with tab2:

    st.subheader("👥 User Activity Segments")

    # --------------------------------------------------------
    # CALCULATE USER ACTIVITY
    # --------------------------------------------------------

    user_activity = (
        interactions
        .groupby("user_id")
        .agg(
            interaction_count=("product_id", "count"),
            average_rating=("rating", "mean")
        )
        .reset_index()
    )


    # --------------------------------------------------------
    # CREATE USER SEGMENTS
    # --------------------------------------------------------

    user_activity["segment"] = np.select(
        [
            user_activity["interaction_count"] < 3,
            user_activity["interaction_count"].between(3, 10),
            user_activity["interaction_count"] > 10
        ],
        [
            "Low Activity",
            "Medium Activity",
            "High Activity"
        ],
        default="Unknown"
    )


    # --------------------------------------------------------
    # USER COUNT BY SEGMENT
    # --------------------------------------------------------

    segment_count = (
        user_activity["segment"]
        .value_counts()
        .reindex(
            [
                "Low Activity",
                "Medium Activity",
                "High Activity"
            ],
            fill_value=0
        )
        .reset_index()
    )

    segment_count.columns = [
        "segment",
        "user_count"
    ]

    st.subheader(
        "📊 Number of Users by Activity Level"
    )

    st.bar_chart(
        segment_count.set_index("segment")
    )


    # --------------------------------------------------------
    # AVERAGE RATING BY SEGMENT
    # --------------------------------------------------------

    st.subheader(
        "⭐ Average Rating by User Segment"
    )

    segment_rating = (
        user_activity
        .groupby("segment")["average_rating"]
        .mean()
        .reindex(
            [
                "Low Activity",
                "Medium Activity",
                "High Activity"
            ]
        )
        .dropna()
        .reset_index()
    )

    segment_rating.columns = [
        "segment",
        "average_rating"
    ]

    st.bar_chart(
        segment_rating.set_index("segment")
    )


    # --------------------------------------------------------
    # USER SEGMENT SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "📋 User Segment Summary"
    )

    segment_summary = (
        user_activity
        .groupby("segment")
        .agg(
            Users=("user_id", "count"),
            Average_Interactions=(
                "interaction_count",
                "mean"
            ),
            Average_Rating=(
                "average_rating",
                "mean"
            )
        )
        .reindex(
            [
                "Low Activity",
                "Medium Activity",
                "High Activity"
            ]
        )
        .round(2)
    )

    st.dataframe(
        segment_summary,
        use_container_width=True
    )


# ============================================================
# TAB 3 - POPULAR PRODUCTS
# ============================================================

with tab3:

    st.subheader("🔥 Top 10 Popular Products")

    top_popular = (
        popular_products
        .head(10)
        [
            [
                "product_name",
                "popularity_score"
            ]
        ]
        .copy()
    )

    # Reverse order so highest appears at the top
    top_popular = top_popular.iloc[::-1]

    top_popular = top_popular.set_index(
        "product_name"
    )

    st.bar_chart(
        top_popular
    )


    st.subheader("🏆 Popular Product Table")

    popular_table = (
        popular_products
        .head(10)
        [
            [
                "product_id",
                "product_name",
                "average_rating",
                "interaction_count",
                "popularity_score"
            ]
        ]
        .copy()
    )

    popular_table["average_rating"] = (
        popular_table["average_rating"]
        .round(2)
    )

    popular_table["popularity_score"] = (
        popular_table["popularity_score"]
        .round(2)
    )

    st.dataframe(
        popular_table,
        use_container_width=True
    )


st.divider()


# ============================================================
# GENERATE RECOMMENDATIONS
# ============================================================

if generate_button:

    try:

        user_id_str = str(user_id)

        recommendations, is_new_user = (
            generate_recommendations(
                user_id_str,
                number_of_recommendations,
                model_choice=model_choice
            )
        )


        # ----------------------------------------------------
        # USER TYPE
        # ----------------------------------------------------

        if is_new_user:

            st.info(
                "🆕 New user detected. "
                "Showing popularity-based recommendations."
            )

        else:

            st.success(
                "✅ Personalized recommendations "
                "generated successfully."
            )


        # ----------------------------------------------------
        # USER HISTORY
        # ----------------------------------------------------

        user_history = interactions[
            interactions["user_id"] == user_id_str
        ]

        if not user_history.empty:

            history_col1, history_col2, history_col3 = (
                st.columns(3)
            )

            with history_col1:

                st.metric(
                    "Past Interactions",
                    f"{len(user_history):,}"
                )

            with history_col2:

                st.metric(
                    "Products Viewed",
                    f"{user_history['product_id'].nunique():,}"
                )

            with history_col3:

                st.metric(
                    "Average Rating",
                    f"{user_history['rating'].mean():.2f}"
                )


        # ----------------------------------------------------
        # DISPLAY RECOMMENDATIONS
        # ----------------------------------------------------

        st.subheader(
            f"🎯 Recommended Products for User {user_id_str}"
        )

        if recommendations:

            recommendation_df = pd.DataFrame(
                recommendations
            )

            recommendation_df.index = (
                recommendation_df.index + 1
            )

            recommendation_df.index.name = "Rank"

            recommendation_df["score"] = (
                recommendation_df["score"]
                .round(4)
            )


            # ------------------------------------------------
            # RECOMMENDATION TABLE
            # ------------------------------------------------

            st.dataframe(
                recommendation_df,
                use_container_width=True
            )


            # ------------------------------------------------
            # RECOMMENDATION SCORE GRAPH
            # ------------------------------------------------

            st.subheader(
                "📈 Recommendation Scores"
            )

            chart_df = recommendation_df[
                [
                    "product_name",
                    "score"
                ]
            ].copy()

            chart_df = chart_df.iloc[::-1]

            chart_df = chart_df.set_index(
                "product_name"
            )

            st.bar_chart(
                chart_df
            )


        else:

            st.warning(
                "No recommendations found."
            )


    except ValueError:

        st.error(
            "Please enter a valid numeric User ID."
        )


# ============================================================
# DEFAULT MESSAGE
# ============================================================

else:

    st.info(
        "👈 Enter a User ID in the sidebar and "
        "click 'Generate Recommendations'."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Personalized Product Recommendation System "
    "| Python • Scikit-learn • Streamlit"
)