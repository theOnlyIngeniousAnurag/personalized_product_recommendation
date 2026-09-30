"""
User Segment Analysis & Segment-Level Recommendation Evaluation
Project 3: Personalized Product Recommendation Model
Defines meaningful, non-collapsed user segments based on empirical interaction tertiles.
Evaluates recommendation behavior, coverage, and metrics across user activity segments.
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TRAIN_PATH = BASE_DIR / "data" / "interim" / "train_interactions.csv"
VAL_PATH = BASE_DIR / "data" / "interim" / "val_interactions.csv"
POPULAR_PATH = BASE_DIR / "data" / "processed" / "popular_products.csv"
EVAL_RESULTS_PATH = BASE_DIR / "outputs" / "reports" / "evaluation_results.json"

PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
TABLES_DIR = BASE_DIR / "outputs" / "tables"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)


def precision_at_k(recommended: list[str], relevant: set[str], k: int = 10) -> float:
    rec_k = recommended[:k]
    if not rec_k:
        return 0.0
    return len(set(rec_k) & relevant) / k


def recall_at_k(recommended: list[str], relevant: set[str], k: int = 10) -> float:
    rec_k = recommended[:k]
    if not relevant:
        return 0.0
    return len(set(rec_k) & relevant) / len(relevant)


def ndcg_at_k(recommended: list[str], relevant: set[str], k: int = 10) -> float:
    rec_k = recommended[:k]
    if not rec_k or not relevant:
        return 0.0
    dcg = sum(1.0 / np.log2(r + 1) for r, item in enumerate(rec_k, start=1) if item in relevant)
    ideal_hits = min(len(relevant), k)
    if ideal_hits == 0:
        return 0.0
    idcg = sum(1.0 / np.log2(r + 1) for r in range(1, ideal_hits + 1))
    return dcg / idcg


def run_user_segment_analysis():
    print("=" * 60)
    print("EMPIRICAL USER SEGMENT ANALYSIS & EVALUATION")
    print("=" * 60)

    train_df = pd.read_csv(TRAIN_PATH, dtype={"user_id": str, "product_id": str})
    val_df = pd.read_csv(VAL_PATH, dtype={"user_id": str, "product_id": str})
    popular_df = pd.read_csv(POPULAR_PATH, dtype={"product_id": str})
    global_popular_pids = popular_df["product_id"].tolist()

    # 1. Compute user interaction statistics on training data
    user_stats = train_df.groupby("user_id").agg(
        interaction_count=("rating", "count"),
        average_rating=("rating", "mean"),
        unique_products=("product_id", "nunique"),
        total_votes=("votes", "sum")
    ).reset_index()

    # 2. Derive deterministic empirical tertile thresholds
    q33 = float(user_stats["interaction_count"].quantile(0.333))
    q67 = float(user_stats["interaction_count"].quantile(0.667))

    print(f"Total training users: {len(user_stats):,}")
    print(f"Empirical 33.3% cutoff: {q33:.1f} interactions")
    print(f"Empirical 66.7% cutoff: {q67:.1f} interactions")

    def assign_segment(count):
        if count <= q33:
            return "Low Activity"
        elif count <= q67:
            return "Medium Activity"
        else:
            return "High Activity"

    user_stats["segment"] = user_stats["interaction_count"].apply(assign_segment)

    # 3. Base segment summary
    segment_order = ["Low Activity", "Medium Activity", "High Activity"]
    segment_summary = user_stats.groupby("segment").agg(
        users=("user_id", "count"),
        min_interactions=("interaction_count", "min"),
        max_interactions=("interaction_count", "max"),
        average_interactions=("interaction_count", "mean"),
        average_rating=("average_rating", "mean"),
        average_products=("unique_products", "mean"),
        average_votes=("total_votes", "mean")
    ).reindex(segment_order).reset_index()

    segment_summary["average_interactions"] = segment_summary["average_interactions"].round(2)
    segment_summary["average_rating"] = segment_summary["average_rating"].round(2)
    segment_summary["average_products"] = segment_summary["average_products"].round(2)
    segment_summary["average_votes"] = segment_summary["average_votes"].round(2)

    print("\n" + "=" * 60)
    print("USER SEGMENT POPULATION & BEHAVIOR SUMMARY")
    print("=" * 60)
    print(segment_summary.to_string(index=False))

    # 4. Evaluate Recommendation Performance Per Segment
    val_relevant = val_df[val_df["rating"] >= 4].groupby("user_id")["product_id"].apply(set).to_dict()
    train_seen = train_df.groupby("user_id")["product_id"].apply(set).to_dict()

    user_to_segment = dict(zip(user_stats["user_id"], user_stats["segment"]))

    # Fast evaluation of Popularity and Hybrid for each segment
    segment_metrics = {
        seg: {
            "Popularity": {"p10": [], "r10": [], "ndcg10": [], "items": set()},
            "Hybrid": {"p10": [], "r10": [], "ndcg10": [], "items": set()}
        }
        for seg in segment_order
    }

    # Prepare User-kNN for Hybrid
    user_ids = train_df["user_id"].unique()
    product_ids = train_df["product_id"].unique()
    u2idx = {u: i for i, u in enumerate(user_ids)}
    p2idx = {p: i for i, p in enumerate(product_ids)}
    idx2p = {i: p for i, p in enumerate(product_ids)}

    rows = train_df["user_id"].map(u2idx)
    cols = train_df["product_id"].map(p2idx)
    ratings = train_df["rating"].astype(np.float32)
    R = pd.Series()  # placeholder

    from scipy.sparse import csr_matrix
    R_mat = csr_matrix((ratings, (rows, cols)), shape=(len(user_ids), len(product_ids)))
    user_norms = np.sqrt(np.array(R_mat.multiply(R_mat).sum(axis=1)).flatten())
    user_norms[user_norms == 0] = 1.0
    R_norm = R_mat.multiply(1.0 / user_norms[:, None])
    user_sim = R_norm.dot(R_norm.T).tocsr()
    user_sim.setdiag(0)

    sim_data, sim_rows, sim_cols = [], [], []
    for u_i in range(len(user_ids)):
        row = user_sim.getrow(u_i)
        if row.nnz > 0:
            top_i = np.argsort(row.data)[::-1][:10]
            for ti in top_i:
                sim_rows.append(u_i)
                sim_cols.append(row.indices[ti])
                sim_data.append(row.data[ti])
    S_top = csr_matrix((sim_data, (sim_rows, sim_cols)), shape=user_sim.shape)
    CF_mat = S_top.dot(R_mat)

    for u, relevant in val_relevant.items():
        if u not in user_to_segment:
            continue
        seg = user_to_segment[u]
        seen = train_seen.get(u, set())

        # Popularity recs
        pop_recs = [p for p in global_popular_pids if p not in seen][:10]
        segment_metrics[seg]["Popularity"]["p10"].append(precision_at_k(pop_recs, relevant, 10))
        segment_metrics[seg]["Popularity"]["r10"].append(recall_at_k(pop_recs, relevant, 10))
        segment_metrics[seg]["Popularity"]["ndcg10"].append(ndcg_at_k(pop_recs, relevant, 10))
        segment_metrics[seg]["Popularity"]["items"].update(pop_recs)

        # CF/Hybrid recs
        u_idx = u2idx[u]
        row = CF_mat.getrow(u_idx)
        if row.nnz > 0:
            top_p = np.argsort(row.data)[::-1][:50]
            cf_recs = [idx2p[row.indices[i]] for i in top_p if idx2p[row.indices[i]] not in seen]
        else:
            cf_recs = pop_recs

        scores = {}
        for r, p in enumerate(cf_recs[:20], 1):
            scores[p] = scores.get(p, 0.0) + 0.70 * (1.0 / (60 + r))
        for r, p in enumerate(pop_recs[:20], 1):
            scores[p] = scores.get(p, 0.0) + 0.30 * (1.0 / (60 + r))
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        hybrid_recs = [p for p, _ in ranked if p not in seen][:10]

        segment_metrics[seg]["Hybrid"]["p10"].append(precision_at_k(hybrid_recs, relevant, 10))
        segment_metrics[seg]["Hybrid"]["r10"].append(recall_at_k(hybrid_recs, relevant, 10))
        segment_metrics[seg]["Hybrid"]["ndcg10"].append(ndcg_at_k(hybrid_recs, relevant, 10))
        segment_metrics[seg]["Hybrid"]["items"].update(hybrid_recs)

    # Compile segment evaluation results
    seg_eval_rows = []
    seg_json_data = {}

    for seg in segment_order:
        pop_res = segment_metrics[seg]["Popularity"]
        hyb_res = segment_metrics[seg]["Hybrid"]
        user_cnt = len(hyb_res["p10"])

        row = {
            "Segment": seg,
            "Users Evaluated": user_cnt,
            "Pop P@10": float(round(np.mean(pop_res["p10"]), 4)),
            "Pop R@10": float(round(np.mean(pop_res["r10"]), 4)),
            "Pop NDCG@10": float(round(np.mean(pop_res["ndcg10"]), 4)),
            "Pop Catalog Coverage": len(pop_res["items"]),
            "Hybrid P@10": float(round(np.mean(hyb_res["p10"]), 4)),
            "Hybrid R@10": float(round(np.mean(hyb_res["r10"]), 4)),
            "Hybrid NDCG@10": float(round(np.mean(hyb_res["ndcg10"]), 4)),
            "Hybrid Catalog Coverage": len(hyb_res["items"])
        }
        seg_eval_rows.append(row)
        seg_json_data[seg] = row

    seg_eval_df = pd.DataFrame(seg_eval_rows)
    print("\n" + "=" * 60)
    print("SEGMENT-LEVEL RECOMMENDATION PERFORMANCE")
    print("=" * 60)
    print(seg_eval_df.to_string(index=False))

    # 5. Save Artifacts
    # Save CSVs
    segment_summary.to_csv(PROCESSED_DIR / "user_segment_summary.csv", index=False)
    segment_summary.to_csv(TABLES_DIR / "user_segment_summary.csv", index=False)
    seg_eval_df.to_csv(TABLES_DIR / "user_segment_evaluation.csv", index=False)

    # Save JSON report
    with open(REPORTS_DIR / "user_segment_evaluation.json", "w", encoding="utf-8") as f:
        json.dump(seg_json_data, f, indent=2)

    # 6. Generate Charts
    try:
        plt.figure(figsize=(7, 4))
        plt.bar(segment_summary["segment"], segment_summary["average_interactions"], color=["#4285F4", "#34A853", "#FBBC05"])
        plt.xlabel("User Activity Segment")
        plt.ylabel("Average Interactions")
        plt.title("Interaction Count by Empirical User Segment")
        plt.tight_layout()
        plt.savefig(PROCESSED_DIR / "user_segment_interactions.png", dpi=150)
        plt.close()

        plt.figure(figsize=(7, 4))
        plt.bar(segment_summary["segment"], segment_summary["average_rating"], color=["#4285F4", "#34A853", "#FBBC05"])
        plt.xlabel("User Activity Segment")
        plt.ylabel("Average Rating")
        plt.ylim(1.0, 5.0)
        plt.title("Average Rating by Empirical User Segment")
        plt.tight_layout()
        plt.savefig(PROCESSED_DIR / "user_segment_ratings.png", dpi=150)
        plt.close()
        print("\nUpdated charts saved to data/processed/.")
    except Exception as e:
        print(f"Chart generation note: {e}")

    print("\nUser segment analysis completed successfully.")
    return segment_summary, seg_eval_df


if __name__ == "__main__":
    run_user_segment_analysis()