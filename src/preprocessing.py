import pandas as pd
import numpy as np
import pandas as pd
from feature_engineering import add_features

# Load dataset
df = pd.read_csv("data/raw/Sample - Superstore.csv", encoding="latin1")
print("=" * 50)
print("SMARTRETAIL DATASET")
print("=" * 50)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nStatistical Summary:")
print(df.describe())
# Convert date columns to datetime format
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print("\nUpdated Data Types:")
print(df.dtypes)
# Extract date features
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month_name()
df["Order Quarter"] = df["Order Date"].dt.quarter

# Calculate shipping duration
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Calculate profit margin
df["Profit Margin"] = (df["Profit"] / df["Sales"]) * 100
# -----------------------------
# Feature Engineering
# -----------------------------

# Extract year, month and quarter
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month_name()
df["Order Quarter"] = df["Order Date"].dt.quarter

# Calculate shipping duration
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Calculate profit margin
df["Profit Margin"] = (
    (df["Profit"] / df["Sales"]) * 100
).round(2)

print("\nNew Features Added Successfully!")

print(df[[
    "Order Date",
    "Ship Date",
    "Order Year",
    "Order Month",
    "Order Quarter",
    "Shipping Days",
    "Profit Margin"
]].head())

# Add engineered features
df = add_features(df)
print("\nFeature Engineering Completed Successfully!")

print("\nNew Columns Added:")

print(df[[
    "Order Year",
    "Order Month",
    "Order Quarter",
    "Shipping Days",
    "Profit Margin"
]].head())