import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Ensure project root is on sys.path
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.recommendation.recommendation_engine import RecommendationEngine

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personalized Product Recommendation System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM PREMIUM CSS (Dark Glassmorphism & Refined Typography)
# ============================================================

CUSTOM_CSS = """
<style>
/* Global resets and typography */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #E2E8F0;
}

/* Background canvas */
.stApp {
    background-color: #0B0F19;
    background-image: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.15), transparent),
        radial-gradient(ellipse 60% 40% at 85% 60%, rgba(139, 92, 246, 0.08), transparent),
        radial-gradient(ellipse 50% 30% at 15% 40%, rgba(14, 165, 233, 0.08), transparent);
    background-attachment: fixed;
}

/* Clean header and footer */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0D1322 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Sidebar section headers */
.sidebar-header {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #818CF8;
    margin-bottom: 0.5rem;
    margin-top: 0.2rem;
}

.sidebar-note {
    font-size: 0.8rem;
    color: #94A3B8;
    margin-bottom: 1.25rem;
    line-height: 1.4;
}

.model-desc-badge {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 8px;
    padding: 0.45rem 0.7rem;
    font-size: 0.75rem;
    color: #C7D2FE;
    margin-top: -0.25rem;
    margin-bottom: 1.25rem;
    line-height: 1.4;
}

/* Hero Section */
.hero-container {
    padding: 1.5rem 0 1.25rem 0;
    margin-bottom: 0.5rem;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #818CF8;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    margin-bottom: 0.85rem;
}

.hero-title {
    font-size: 2.25rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #F8FAFC;
    line-height: 1.15;
    margin: 0 0 0.5rem 0;
}

.hero-subtitle {
    font-size: 1.0rem;
    color: #94A3B8;
    max-width: 780px;
    line-height: 1.55;
    margin: 0 0 1rem 0;
}

.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: #34D399;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
}

.pulse-dot {
    width: 6px;
    height: 6px;
    background: #34D399;
    border-radius: 50%;
    box-shadow: 0 0 8px #34D399;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.25rem 0 2rem 0;
}

.kpi-card {
    background: rgba(17, 24, 39, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 1.2rem 1.25rem;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.35);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}

.kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.4rem;
}

.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94A3B8;
}

.kpi-icon {
    font-size: 1.1rem;
    opacity: 0.85;
}

.kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #F8FAFC;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}

.kpi-sub {
    font-size: 0.75rem;
    color: #64748B;
}

/* Glass Surface Containers */
.glass-panel {
    background: rgba(17, 24, 39, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}

/* Tabs customization */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    gap: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding-bottom: 0.25rem;
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    padding: 0 1.25rem;
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px 8px 0 0 !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #F8FAFC !important;
    background: rgba(255, 255, 255, 0.05) !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(99, 102, 241, 0.12) !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
    color: #F8FAFC !important;
    border-bottom: 2px solid #818CF8 !important;
    font-weight: 600 !important;
}

/* Primary Button Styling */
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1.25rem !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6) !important;
    transform: translateY(-1px) !important;
}

/* Recommendation Result Header Card */
.user-profile-card {
    background: rgba(17, 24, 39, 0.85);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

.user-profile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding-bottom: 0.85rem;
}

.user-profile-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.02em;
}

.user-stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

.user-stat-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 0.75rem 1rem;
}

.user-stat-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin-bottom: 0.2rem;
}

.user-stat-val {
    font-size: 1.35rem;
    font-weight: 700;
    color: #F8FAFC;
}

/* Recommendation Item Cards */
.rec-card {
    background: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.rec-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateX(3px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
}

.rec-card-top1 {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(20, 26, 42, 0.85) 100%);
    border: 1px solid rgba(245, 158, 11, 0.35);
    box-shadow: 0 4px 24px rgba(245, 158, 11, 0.08);
}

.rec-card-top1:hover {
    border-color: rgba(245, 158, 11, 0.55);
}

.rank-badge {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #A5B4FC;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.95rem;
    flex-shrink: 0;
}

.rank-badge-top1 {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.15) 100%);
    border: 1px solid rgba(245, 158, 11, 0.5);
    color: #FCD34D;
}

.rec-info {
    flex-grow: 1;
    min-width: 0;
}

.rec-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 0.3rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.rec-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.rec-reason {
    font-size: 0.72rem;
    color: #94A3B8;
    background: rgba(255, 255, 255, 0.04);
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.rec-id {
    font-size: 0.7rem;
    color: #64748B;
    font-family: monospace;
}

.rec-score-box {
    text-align: right;
    flex-shrink: 0;
}

.rec-score-val {
    font-size: 1.15rem;
    font-weight: 700;
    color: #818CF8;
    font-family: monospace;
}

.rec-score-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
}

/* Empty State Card */
.empty-state-card {
    background: rgba(17, 24, 39, 0.6);
    border: 1px dashed rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
}

.empty-state-icon {
    font-size: 2.25rem;
    color: #818CF8;
    margin-bottom: 0.75rem;
}

.empty-state-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 0.4rem;
}

.empty-state-desc {
    font-size: 0.85rem;
    color: #94A3B8;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Section Subheader */
.section-headline {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: #F8FAFC;
    margin: 1.5rem 0 0.35rem 0;
}

.section-sub {
    font-size: 0.82rem;
    color: #94A3B8;
    margin-bottom: 1rem;
}

/* Podiums for Top 3 Popular */
.podium-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.podium-card {
    background: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.25rem;
    position: relative;
    transition: transform 0.2s ease;
}

.podium-card:hover {
    transform: translateY(-2px);
}

.podium-rank-1 {
    border-color: rgba(245, 158, 11, 0.4);
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(20, 26, 42, 0.8) 100%);
}

.podium-rank-2 {
    border-color: rgba(148, 163, 184, 0.3);
}

.podium-rank-3 {
    border-color: rgba(217, 119, 6, 0.3);
}

.podium-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    margin-bottom: 0.6rem;
}

.badge-gold {
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid rgba(245, 158, 11, 0.5);
    color: #FCD34D;
}

.badge-silver {
    background: rgba(148, 163, 184, 0.2);
    border: 1px solid rgba(148, 163, 184, 0.4);
    color: #E2E8F0;
}

.badge-bronze {
    background: rgba(180, 83, 9, 0.2);
    border: 1px solid rgba(180, 83, 9, 0.4);
    color: #FDBA74;
}

.podium-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #F8FAFC;
    line-height: 1.35;
    margin-bottom: 0.6rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 2.7rem;
}

.podium-stats {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #94A3B8;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 0.5rem;
}

/* User Segment Cards */
.segment-card {
    background: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.segment-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 0.35rem;
}

.segment-range {
    font-size: 0.75rem;
    color: #818CF8;
    margin-bottom: 0.85rem;
    font-weight: 500;
}

.segment-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
}

.seg-metric-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    padding: 0.6rem;
}

.seg-metric-label {
    font-size: 0.68rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.seg-metric-val {
    font-size: 1.1rem;
    font-weight: 700;
    color: #F8FAFC;
}

/* Streamlit Native Overrides */
div[data-testid="stMetricValue"] {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #F8FAFC !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #94A3B8 !important;
}

hr {
    border-color: rgba(255, 255, 255, 0.07) !important;
    margin: 1.5rem 0 !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# DATA INGESTION & CACHED RESOURCES
# ============================================================

@st.cache_data
def load_application_data():
    """
    Loads catalog products, ranked popular items, user segment tertiles,
    and verified user directory from authentic processed artifacts.
    """
    products = pd.read_csv(
        "data/processed/products.csv",
        dtype={"product_id": str}
    )
    products["product_name"] = products["product_name"].fillna("Unknown Product")

    popular_products = pd.read_csv(
        "data/processed/popular_products.csv",
        dtype={"product_id": str}
    )

    users = pd.read_csv(
        "data/processed/users.csv",
        dtype={"user_id": str}
    )

    user_segment_summary = pd.read_csv(
        "data/processed/user_segment_summary.csv"
    )

    return products, popular_products, users, user_segment_summary


@st.cache_data
def load_historical_ratings_distribution():
    """
    Computes exact authentic rating distribution and statistics
    across all 745,889 verified training interactions.
    """
    t1 = pd.read_csv("data/raw/train_part1.csv", usecols=["rating"])
    t2 = pd.read_csv("data/raw/train_part2.csv", usecols=["rating"])
    ratings_series = pd.concat([t1["rating"], t2["rating"]], ignore_index=True)

    counts = ratings_series.value_counts().sort_index().reset_index()
    counts.columns = ["Rating", "Count"]
    counts["Stars"] = counts["Rating"].astype(str) + " ★"
    counts["Percentage"] = (counts["Count"] / len(ratings_series) * 100).round(2)

    stats = {
        "total_interactions": int(len(ratings_series)),
        "mean_rating": float(ratings_series.mean()),
        "min_rating": float(ratings_series.min()),
        "max_rating": float(ratings_series.max())
    }
    return counts, stats


products_df, popular_df, users_df, segment_df = load_application_data()
rating_dist_df, rating_stats = load_historical_ratings_distribution()

# ============================================================
# CANONICAL RECOMMENDATION ENGINE INTEGRATION
# ============================================================

@st.cache_resource
def get_recommendation_engine():
    """Initializes and caches the canonical backend RecommendationEngine."""
    return RecommendationEngine()

engine = get_recommendation_engine()

# Model descriptions for UI selector
MODEL_OPTIONS = {
    "Hybrid": "Balanced multi-signal ranking (50% CF + 30% Content + 20% Popularity)",
    "Collaborative Filtering": "User similarity via sparse cosine kNN",
    "Matrix Factorization": "Latent preference factors via TruncatedSVD",
    "Content-Based": "Product title semantic similarity via TF-IDF",
    "Popularity Baseline": "Global engagement and rating product ranking"
}

def generate_recommendations(user_id: str, n: int, model_name: str):
    """
    Executes inference via the backend RecommendationEngine.
    Preserves exact ML algorithm behavior and cold-start fallback.
    """
    user_id = str(user_id).strip()
    is_new_user = user_id not in engine.user_to_index

    if "Collaborative" in model_name:
        rec_df = engine.recommend_collaborative(user_id, n=n)
    elif "Matrix Factorization" in model_name or "SVD" in model_name:
        rec_df = engine.recommend_matrix_factorization(user_id, n=n)
    elif "Content" in model_name:
        rec_df = engine.recommend_content(user_id, n=n)
    elif "Popularity" in model_name:
        rec_df = engine.recommend_popularity(user_id, n=n)
    else:
        rec_df = engine.recommend_hybrid(user_id, n=n)

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
# SIDEBAR CONTROL PANEL
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-header">RECOMMENDATION CONTROLS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-note">Choose a model and generate a personalized ranking.</div>', unsafe_allow_html=True)

    input_user_id = st.text_input(
        "User ID",
        value="1813",
        help="Enter an active shopper ID (e.g., 1813) or arbitrary ID for cold-start fallback."
    )

    input_n = st.slider(
        "Number of Recommendations",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )

    selected_model = st.selectbox(
        "Recommendation Model",
        options=list(MODEL_OPTIONS.keys()),
        index=0
    )

    st.markdown(
        f'<div class="model-desc-badge"><strong>{selected_model}:</strong><br>{MODEL_OPTIONS[selected_model]}</div>',
        unsafe_allow_html=True
    )

    generate_btn = st.button(
        "Generate Recommendations",
        type="primary",
        use_container_width=True
    )

    st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">SYSTEM ARCHITECTURE</div>', unsafe_allow_html=True)
    st.caption("• 20 Latent SVD Factor Components\n• 30,000 TF-IDF Metadata Features\n• 50/30/20 Hybrid Blend\n• Deterministic Cold-Start Fallback")

# ============================================================
# HERO HEADER SECTION
# ============================================================

hero_html = f"""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div class="hero-eyebrow">✦ RECOMMENDATION INTELLIGENCE</div>
            <h1 class="hero-title">Personalized Product<br>Recommendation System</h1>
            <p class="hero-subtitle">
                Discover relevant products through collaborative intelligence, semantic similarity, and popularity-aware ranking.
            </p>
        </div>
        <div style="padding-top: 0.5rem;">
            <div class="status-indicator">
                <span class="pulse-dot"></span> SYSTEM OPERATIONAL
            </div>
        </div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# ============================================================
# HEADLINE KPI SECTION (Consistent Active Dataset Values)
# ============================================================

kpi_html = f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Users</span>
            <span class="kpi-icon">👥</span>
        </div>
        <div class="kpi-value">{len(users_df):,}</div>
        <div class="kpi-sub">Active Shopper Profiles</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Products</span>
            <span class="kpi-icon">🛍️</span>
        </div>
        <div class="kpi-value">{len(products_df):,}</div>
        <div class="kpi-sub">Total Catalog Items</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Training Interactions</span>
            <span class="kpi-icon">🔄</span>
        </div>
        <div class="kpi-value">{rating_stats['total_interactions']:,}</div>
        <div class="kpi-sub">Authentic Review Records</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Models</span>
            <span class="kpi-icon">⚙️</span>
        </div>
        <div class="kpi-value">5</div>
        <div class="kpi-sub">Hybrid & Single-Signal Engines</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# ============================================================
# MAIN APPLICATION WORKSPACE
# ============================================================

# If user clicked generate, present the recommendation experience prominently
if generate_btn:
    user_id_clean = str(input_user_id).strip()
    
    try:
        recommendations, is_new_user = generate_recommendations(
            user_id_clean,
            input_n,
            selected_model
        )

        # Retrieve authentic historical profile from users directory
        matched_user = users_df[users_df["user_id"] == user_id_clean]
        if not matched_user.empty:
            past_interactions = int(matched_user.iloc[0]["interaction_count"])
            products_interacted = int(matched_user.iloc[0]["unique_products"])
            avg_user_rating = f"{float(matched_user.iloc[0]['average_rating']):.2f} ★"
        else:
            past_interactions = 0
            products_interacted = 0
            avg_user_rating = "N/A (Cold-Start)"

        status_badge_html = (
            '<span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #34D399; padding: 0.3rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">● Personalized ranking generated</span>'
            if not is_new_user
            else '<span style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.35); color: #FBBF24; padding: 0.3rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">○ New user detected — showing popularity-based recommendations</span>'
        )

        # User profile summary block
        user_summary_html = f"""
        <div class="user-profile-card">
            <div class="user-profile-header">
                <div>
                    <div style="font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #818CF8; font-weight: 600; margin-bottom: 0.2rem;">TARGET PROFILE</div>
                    <div class="user-profile-title">Personalized for User {user_id_clean}</div>
                </div>
                <div>{status_badge_html}</div>
            </div>
            <div class="user-stats-grid">
                <div class="user-stat-box">
                    <div class="user-stat-label">Past Interactions</div>
                    <div class="user-stat-val">{past_interactions:,}</div>
                </div>
                <div class="user-stat-box">
                    <div class="user-stat-label">Products Interacted</div>
                    <div class="user-stat-val">{products_interacted:,}</div>
                </div>
                <div class="user-stat-box">
                    <div class="user-stat-label">Historical Average Rating</div>
                    <div class="user-stat-val">{avg_user_rating}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(user_summary_html, unsafe_allow_html=True)

        st.markdown('<div class="section-headline">Recommended for You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-sub">Top {len(recommendations)} candidate products scored via {selected_model}</div>', unsafe_allow_html=True)

        if recommendations:
            rec_df = pd.DataFrame(recommendations)
            rec_df.index = rec_df.index + 1
            rec_df.index.name = "Rank"

            # Render top recommendation spotlight cards
            for idx, rec in enumerate(recommendations, start=1):
                is_top1 = (idx == 1)
                card_class = "rec-card rec-card-top1" if is_top1 else "rec-card"
                rank_class = "rank-badge rank-badge-top1" if is_top1 else "rank-badge"
                score_str = f"{rec['score']:.4f}" if rec['score'] <= 1.0 else f"{rec['score']:.1f}"

                rec_card_html = f"""
                <div class="{card_class}">
                    <div class="{rank_class}">#{idx}</div>
                    <div class="rec-info">
                        <div class="rec-title" title="{rec['product_name']}">{rec['product_name']}</div>
                        <div class="rec-meta">
                            <span class="rec-reason">{rec['reason']}</span>
                            <span class="rec-id">ID: {rec['product_id']}</span>
                        </div>
                    </div>
                    <div class="rec-score-box">
                        <div class="rec-score-val">{score_str}</div>
                        <div class="rec-score-label">Ranking Score</div>
                    </div>
                </div>
                """
                st.markdown(rec_card_html, unsafe_allow_html=True)

            # Ranking Visualization
            st.markdown('<div class="section-headline" style="margin-top: 2rem;">Recommendation Ranking Distribution</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Relative score strengths across ranked recommendation positions</div>', unsafe_allow_html=True)

            chart_data = rec_df.reset_index()[["Rank", "product_name", "score"]].copy()
            chart_data["Rank_Label"] = "#" + chart_data["Rank"].astype(str) + " " + chart_data["product_name"].str[:32] + "..."
            chart_data["is_top"] = chart_data["Rank"] == 1

            rank_chart = (
                alt.Chart(chart_data)
                .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, height=22)
                .encode(
                    y=alt.Y("Rank_Label:N", sort=None, title="", axis=alt.Axis(labelColor="#94A3B8", labelFontSize=11)),
                    x=alt.X("score:Q", title="Recommendation Score", axis=alt.Axis(labelColor="#94A3B8", titleColor="#818CF8")),
                    color=alt.condition(
                        alt.datum.is_top,
                        alt.value("#F59E0B"), # Highlight Top 1 with Amber Gold
                        alt.value("#6366F1")  # Standard Indigo for others
                    ),
                    tooltip=[
                        alt.Tooltip("Rank:O", title="Rank"),
                        alt.Tooltip("product_name:N", title="Product"),
                        alt.Tooltip("score:Q", title="Score", format=".4f")
                    ]
                )
                .properties(height=max(220, len(chart_data) * 28))
                .configure_view(strokeWidth=0)
                .configure_axis(grid=False, domain=False)
            )
            st.altair_chart(rank_chart, use_container_width=True)

            # Complete Interactive Table
            with st.expander("View Tabular Recommendation Dataset"):
                st.dataframe(
                    rec_df[["product_id", "product_name", "score", "reason"]],
                    use_container_width=True
                )

        else:
            st.warning("No recommendations returned for the selected configuration.")

    except Exception as e:
        st.error(f"Inference error: {str(e)}")

else:
    # Premium Empty State
    empty_html = """
    <div class="empty-state-card">
        <div class="empty-state-icon">✦</div>
        <div class="empty-state-title">Ready to Personalize</div>
        <div class="empty-state-desc">
            Enter a user ID and choose a recommendation model in the control panel to generate a ranked product list.
        </div>
    </div>
    """
    st.markdown(empty_html, unsafe_allow_html=True)

st.markdown("<hr style='margin: 2.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)

# ============================================================
# ANALYTICS WORKSPACE (3 TAB INTELLIGENCE DASHBOARD)
# ============================================================

st.markdown('<div class="section-headline">Recommendation Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Empirical data foundations, user behavioral segments, and catalog dynamics</div>', unsafe_allow_html=True)

tab_overview, tab_segments, tab_popular = st.tabs(
    [
        "⭐ Overview",
        "👥 User Segments",
        "🔥 Popular Products"
    ]
)

# ------------------------------------------------------------
# TAB 1: OVERVIEW (RATING INTELLIGENCE)
# ------------------------------------------------------------
with tab_overview:
    st.markdown('<div class="section-headline">Rating Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Distribution of historical product ratings across 745,889 authentic interactions</div>', unsafe_allow_html=True)

    # Altair rating distribution chart
    rating_chart = (
        alt.Chart(rating_dist_df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Stars:N", title="Rating Tier", sort=None, axis=alt.Axis(labelColor="#CBD5E1", labelFontSize=12)),
            y=alt.Y("Count:Q", title="Interaction Volume", axis=alt.Axis(labelColor="#94A3B8", titleColor="#818CF8")),
            color=alt.Color(
                "Count:Q",
                scale=alt.Scale(scheme="purples"),
                legend=None
            ),
            tooltip=[
                alt.Tooltip("Stars:N", title="Tier"),
                alt.Tooltip("Count:Q", title="Total Reviews", format=","),
                alt.Tooltip("Percentage:Q", title="Share (%)", format=".2f")
            ]
        )
        .properties(height=280)
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domain=False)
    )
    st.altair_chart(rating_chart, use_container_width=True)

    # 3 Statistics Cards
    st.markdown('<div class="section-headline" style="margin-top: 1rem;">Rating Statistics</div>', unsafe_allow_html=True)
    r_col1, r_col2, r_col3 = st.columns(3)

    with r_col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Rating</div>
            <div class="kpi-value">{rating_stats['mean_rating']:.2f} ★</div>
            <div class="kpi-sub">Across 745,889 authentic reviews</div>
        </div>
        """, unsafe_allow_html=True)

    with r_col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Highest Rating</div>
            <div class="kpi-value">{rating_stats['max_rating']:.1f} ★</div>
            <div class="kpi-sub">Maximum score bound</div>
        </div>
        """, unsafe_allow_html=True)

    with r_col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Lowest Rating</div>
            <div class="kpi-value">{rating_stats['min_rating']:.1f} ★</div>
            <div class="kpi-sub">Minimum score bound</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------
# TAB 2: USER SEGMENTS (EMPIRICAL TERTILES)
# ------------------------------------------------------------
with tab_segments:
    st.markdown('<div class="section-headline">User Activity Segments</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Balanced empirical interaction tertiles derived from active customer distributions</div>', unsafe_allow_html=True)

    seg_col1, seg_col2, seg_col3 = st.columns(3)

    # Low Activity: <= 146
    low_seg = segment_df[segment_df["segment"] == "Low Activity"].iloc[0]
    with seg_col1:
        st.markdown(f"""
        <div class="segment-card">
            <div class="segment-name">Low Activity</div>
            <div class="segment-range">≤ 146 Interactions</div>
            <div class="segment-metrics">
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Users</div>
                    <div class="seg-metric-val">{int(low_seg['users']):,}</div>
                </div>
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Avg Reviews</div>
                    <div class="seg-metric-val">{float(low_seg['average_interactions']):.1f}</div>
                </div>
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Avg Rating</div>
                    <div class="seg-metric-val">{float(low_seg['average_rating']):.2f} ★</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Medium Activity: 147 - 224
    med_seg = segment_df[segment_df["segment"] == "Medium Activity"].iloc[0]
    with seg_col2:
        st.markdown(f"""
        <div class="segment-card">
            <div class="segment-name">Medium Activity</div>
            <div class="segment-range">147 – 224 Interactions</div>
            <div class="segment-metrics">
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Users</div>
                    <div class="seg-metric-val">{int(med_seg['users']):,}</div>
                </div>
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Avg Reviews</div>
                    <div class="seg-metric-val">{float(med_seg['average_interactions']):.1f}</div>
                </div>
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Avg Rating</div>
                    <div class="seg-metric-val">{float(med_seg['average_rating']):.2f} ★</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # High Activity: > 224
    high_seg = segment_df[segment_df["segment"] == "High Activity"].iloc[0]
    with seg_col3:
        st.markdown(f"""
        <div class="segment-card">
            <div class="segment-name">High Activity</div>
            <div class="segment-range">> 224 Interactions</div>
            <div class="segment-metrics">
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Users</div>
                    <div class="seg-metric-val">{int(high_seg['users']):,}</div>
                </div>
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Avg Reviews</div>
                    <div class="seg-metric-val">{float(high_seg['average_interactions']):.1f}</div>
                </div>
                <div class="seg-metric-box">
                    <div class="seg-metric-label">Avg Rating</div>
                    <div class="seg-metric-val">{float(high_seg['average_rating']):.2f} ★</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Segment Visualization
    st.markdown('<div class="section-headline">Activity Comparison</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        user_cnt_chart = (
            alt.Chart(segment_df)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("segment:N", title="Segment", sort=None, axis=alt.Axis(labelColor="#CBD5E1")),
                y=alt.Y("users:Q", title="Shopper Count", axis=alt.Axis(labelColor="#94A3B8")),
                color=alt.value("#6366F1"),
                tooltip=["segment", "users", "average_interactions"]
            )
            .properties(height=220)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(user_cnt_chart, use_container_width=True)

    with c2:
        avg_act_chart = (
            alt.Chart(segment_df)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("segment:N", title="Segment", sort=None, axis=alt.Axis(labelColor="#CBD5E1")),
                y=alt.Y("average_interactions:Q", title="Average Interactions", axis=alt.Axis(labelColor="#94A3B8")),
                color=alt.value("#818CF8"),
                tooltip=["segment", "average_interactions", "average_rating"]
            )
            .properties(height=220)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(avg_act_chart, use_container_width=True)

    # Segment Summary Table
    st.markdown('<div class="section-headline">Segment Intelligence Summary</div>', unsafe_allow_html=True)
    display_seg = segment_df.copy()
    display_seg = display_seg.rename(columns={
        "segment": "Segment",
        "users": "Shoppers",
        "min_interactions": "Min Interactions",
        "max_interactions": "Max Interactions",
        "average_interactions": "Avg Interactions",
        "average_rating": "Avg Rating",
        "average_votes": "Avg Votes"
    })
    st.dataframe(
        display_seg[["Segment", "Shoppers", "Min Interactions", "Max Interactions", "Avg Interactions", "Avg Rating", "Avg Votes"]],
        use_container_width=True
    )

# ------------------------------------------------------------
# TAB 3: POPULAR PRODUCTS (DISCOVERY PODIUM & RANKINGS)
# ------------------------------------------------------------
with tab_popular:
    st.markdown('<div class="section-headline">Top Products Discovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Highest performing catalog items by interaction volume and weighted rating score</div>', unsafe_allow_html=True)

    top10 = popular_df.head(10).copy()

    # Podium cards for top 3
    if len(top10) >= 3:
        p1 = top10.iloc[0]
        p2 = top10.iloc[1]
        p3 = top10.iloc[2]

        podium_html = f"""
        <div class="podium-grid">
            <div class="podium-card podium-rank-1">
                <span class="podium-badge badge-gold">★ Rank #1 Champion</span>
                <div class="podium-title" title="{p1['product_name']}">{p1['product_name']}</div>
                <div class="podium-stats">
                    <span>{p1['average_rating']:.2f} ★ ({int(p1['interaction_count']):,} reviews)</span>
                    <strong style="color: #FCD34D;">Score: {p1['popularity_score']:.1f}</strong>
                </div>
            </div>
            <div class="podium-card podium-rank-2">
                <span class="podium-badge badge-silver">Rank #2 Runner-Up</span>
                <div class="podium-title" title="{p2['product_name']}">{p2['product_name']}</div>
                <div class="podium-stats">
                    <span>{p2['average_rating']:.2f} ★ ({int(p2['interaction_count']):,} reviews)</span>
                    <strong style="color: #E2E8F0;">Score: {p2['popularity_score']:.1f}</strong>
                </div>
            </div>
            <div class="podium-card podium-rank-3">
                <span class="podium-badge badge-bronze">Rank #3 Third Place</span>
                <div class="podium-title" title="{p3['product_name']}">{p3['product_name']}</div>
                <div class="podium-stats">
                    <span>{p3['average_rating']:.2f} ★ ({int(p3['interaction_count']):,} reviews)</span>
                    <strong style="color: #FDBA74;">Score: {p3['popularity_score']:.1f}</strong>
                </div>
            </div>
        </div>
        """
        st.markdown(podium_html, unsafe_allow_html=True)

    # Altair Popularity Score Bar Chart
    top10_chart_data = top10.copy()
    top10_chart_data["short_name"] = "#" + top10_chart_data["rank"].astype(str) + " " + top10_chart_data["product_name"].str[:32] + "..."

    pop_chart = (
        alt.Chart(top10_chart_data)
        .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, height=22)
        .encode(
            y=alt.Y("short_name:N", sort=None, title="", axis=alt.Axis(labelColor="#94A3B8", labelFontSize=11)),
            x=alt.X("popularity_score:Q", title="Popularity Score (Avg Rating × Interactions)", axis=alt.Axis(labelColor="#94A3B8", titleColor="#818CF8")),
            color=alt.value("#6366F1"),
            tooltip=[
                alt.Tooltip("rank:O", title="Rank"),
                alt.Tooltip("product_name:N", title="Product"),
                alt.Tooltip("average_rating:Q", title="Avg Rating", format=".2f"),
                alt.Tooltip("interaction_count:Q", title="Reviews", format=","),
                alt.Tooltip("popularity_score:Q", title="Score", format=".1f")
            ]
        )
        .properties(height=320)
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domain=False)
    )
    st.altair_chart(pop_chart, use_container_width=True)

    # Popular Products Table
    st.markdown('<div class="section-headline">Catalog Popularity Leaderboard</div>', unsafe_allow_html=True)
    table_df = top10[["rank", "product_id", "product_name", "average_rating", "interaction_count", "popularity_score"]].copy()
    table_df["average_rating"] = table_df["average_rating"].round(2)
    table_df["popularity_score"] = table_df["popularity_score"].round(2)
    table_df.columns = ["Rank", "Product ID", "Product Name", "Average Rating", "Reviews Count", "Popularity Score"]

    st.dataframe(
        table_df,
        use_container_width=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("<hr style='margin: 3rem 0 1rem 0;'>", unsafe_allow_html=True)
footer_html = """
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; color: #64748B; font-size: 0.78rem; padding-bottom: 2rem;">
    <div>Personalized Product Recommendation System • Monash FIT5212 Capstone</div>
    <div>Python • Scikit-learn • Streamlit • Fast Inference</div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)