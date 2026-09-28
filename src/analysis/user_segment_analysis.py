import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATA
# ============================================================

interactions = pd.read_csv(
    "data/processed/interactions.csv"
)

users = pd.read_csv(
    "data/processed/users.csv"
)

print("=" * 60)
print("USER SEGMENT ANALYSIS")
print("=" * 60)


# ============================================================
# 2. CREATE USER SEGMENTS
# ============================================================

def create_segment(count):

    if count < 3:
        return "Low Activity"

    elif count <= 10:
        return "Medium Activity"

    else:
        return "High Activity"


users["segment"] = users[
    "interaction_count"
].apply(create_segment)


# ============================================================
# 3. SEGMENT SUMMARY
# ============================================================

segment_summary = (
    users
    .groupby("segment")
    .agg(
        users=("user_id", "count"),
        average_interactions=(
            "interaction_count",
            "mean"
        ),
        average_rating=(
            "average_rating",
            "mean"
        ),
        average_products=(
            "unique_products",
            "mean"
        ),
        average_votes=(
            "total_votes",
            "mean"
        )
    )
    .reset_index()
)


# ============================================================
# 4. DISPLAY RESULTS
# ============================================================

print("\nUser Segment Summary:")
print("-" * 60)

print(
    segment_summary.to_string(
        index=False
    )
)


# ============================================================
# 5. SAVE RESULTS
# ============================================================

segment_summary.to_csv(
    "data/processed/user_segment_summary.csv",
    index=False
)


# ============================================================
# 6. CREATE INTERACTION CHART
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    segment_summary["segment"],
    segment_summary["average_interactions"]
)

plt.xlabel("User Segment")
plt.ylabel("Average Number of Interactions")
plt.title("Average Interactions by User Segment")

plt.tight_layout()

plt.savefig(
    "data/processed/user_segment_interactions.png",
    dpi=300
)

plt.show()


# ============================================================
# 7. CREATE RATING CHART
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    segment_summary["segment"],
    segment_summary["average_rating"]
)

plt.xlabel("User Segment")
plt.ylabel("Average Rating")
plt.title("Average Rating by User Segment")

plt.tight_layout()

plt.savefig(
    "data/processed/user_segment_ratings.png",
    dpi=300
)

plt.show()


# ============================================================
# 8. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("USER SEGMENT ANALYSIS COMPLETED")
print("=" * 60)