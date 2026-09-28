import pandas as pd

TRAIN_PATH = "data/raw/train.csv"
TEST_PATH = "data/raw/test.csv"

print("=" * 60)
print("LOADING DATA")
print("=" * 60)

train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)

print(f"\nTrain shape: {train.shape}")
print(f"Test shape:  {test.shape}")

# --------------------------------------------------
# TRAIN COLUMNS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TRAIN COLUMNS")
print("=" * 60)

for column in train.columns:
    print(f"- {column}")

# --------------------------------------------------
# TEST COLUMNS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST COLUMNS")
print("=" * 60)

for column in test.columns:
    print(f"- {column}")

# --------------------------------------------------
# DATA TYPES
# --------------------------------------------------

print("\n" + "=" * 60)
print("TRAIN DATA TYPES")
print("=" * 60)

print(train.dtypes)

# --------------------------------------------------
# MISSING VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES - TRAIN")
print("=" * 60)

print(train.isnull().sum())

print("\n" + "=" * 60)
print("MISSING VALUES - TEST")
print("=" * 60)

print(test.isnull().sum())

# --------------------------------------------------
# FIRST 5 ROWS
# --------------------------------------------------

print("\n" + "=" * 60)
print("FIRST 5 TRAIN ROWS")
print("=" * 60)

print(train.head())

print("\n" + "=" * 60)
print("FIRST 5 TEST ROWS")
print("=" * 60)

print(test.head())

# --------------------------------------------------
# UNIQUE VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("UNIQUE VALUES IN TRAIN")
print("=" * 60)

for column in train.columns:
    print(f"{column}: {train[column].nunique():,} unique values")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED")
print("=" * 60)