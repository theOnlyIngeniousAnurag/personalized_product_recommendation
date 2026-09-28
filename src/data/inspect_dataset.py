import pandas as pd
import os

# File paths
train_path = "data/raw/train.csv"
test_path = "data/raw/test.csv"

# Check whether files exist
print("=" * 60)
print("CHECKING DATASET FILES")
print("=" * 60)

if not os.path.exists(train_path):
    print("ERROR: train.csv not found!")
    exit()

if not os.path.exists(test_path):
    print("ERROR: test.csv not found!")
    exit()

print("train.csv found")
print("test.csv found")

# --------------------------------------------------
# Load only a small sample to protect RAM
# --------------------------------------------------

print("\n" + "=" * 60)
print("LOADING SAMPLE DATA")
print("=" * 60)

train = pd.read_csv(train_path, nrows=5000)
test = pd.read_csv(test_path, nrows=5000)

# --------------------------------------------------
# Basic information
# --------------------------------------------------

print("\n" + "=" * 60)
print("TRAIN DATA")
print("=" * 60)

print("Sample rows:", len(train))
print("Columns:", len(train.columns))

print("\nColumn names:")
print(train.columns.tolist())

print("\nFirst 5 rows:")
print(train.head())

print("\nData types:")
print(train.dtypes)

print("\nMissing values:")
print(train.isnull().sum())

# --------------------------------------------------
# Test data
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST DATA")
print("=" * 60)

print("Sample rows:", len(test))
print("Columns:", len(test.columns))

print("\nColumn names:")
print(test.columns.tolist())

print("\nFirst 5 rows:")
print(test.head())

print("\nData types:")
print(test.dtypes)

print("\nMissing values:")
print(test.isnull().sum())

# --------------------------------------------------
# File sizes
# --------------------------------------------------

print("\n" + "=" * 60)
print("FILE SIZES")
print("=" * 60)

train_size = os.path.getsize(train_path) / (1024 * 1024)
test_size = os.path.getsize(test_path) / (1024 * 1024)

print(f"train.csv: {train_size:.2f} MB")
print(f"test.csv:  {test_size:.2f} MB")

print("\n" + "=" * 60)
print("DATASET INSPECTION COMPLETED")
print("=" * 60)