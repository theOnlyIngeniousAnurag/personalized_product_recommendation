# Project Architecture

## 1. Project Overview

The Personalized Product Recommendation System is a machine learning based recommendation project developed using Python.

The system uses user-product interaction data to generate personalized product recommendations. It combines popularity-based recommendation, collaborative filtering, matrix factorization, content-based recommendation, and hybrid recommendation techniques.

The project also provides a Streamlit interface for interacting with the recommendation system and a FastAPI-based recommendation API.

---

## 2. Project Structure

```text
personalized-product-recommendation/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── train.csv
│   │   └── test.csv
│   ├── processed/
│   │   └── interactions.csv
│   └── sample/
│
├── notebooks/
│
├── src/
│   ├── data/
│   ├── models/
│   ├── evaluation/
│   ├── recommendation/
│   ├── analysis/
│   └── utils/
│
├── models/
│
├── api/
│   └── recommendation_api.py
│
├── app/
│   └── streamlit_app.py
│
├── tests/
│
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── reports/
│
├── config/
│   └── config.py
│
└── docs/
    ├── project_architecture.md
    ├── methodology.md
    └── api.md