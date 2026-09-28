# Personalized Product Recommendation System

A machine learning-based product recommendation system that recommends products to users using their previous product interactions and product information.

## Project Overview

The system combines multiple recommendation approaches:

- Popularity-based recommendation
- Collaborative filtering
- Matrix factorization
- Content-based recommendation
- Hybrid recommendation

The final hybrid recommendation combines collaborative, content-based, and popularity signals.

## Dataset

The project uses the FIT5212 S1 2025 Recommender System Challenge dataset.

The dataset contains user-product rating interactions and product information.

### Dataset Files

```text
data/
└── raw/
    ├── train.csv
    └── test.csv