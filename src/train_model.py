import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np
import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from src.feature_engineering import add_features

df = pd.read_csv(
    "data/raw/Sample - Superstore.csv",
    encoding="latin1"
)

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df = add_features(df)

#select features
features = [
    "Sales",
    "Quantity",
    "Discount",
    "Category",
    "Sub-Category",
    "Region",
    "Segment",
    "Shipping Days",
    "Order Year",
    "Order Quarter"
]

X = df[features].copy()
y = df["Profit"]

print("Features Shape:", X.shape)
print("Target Shape:", y.shape)

print(X.head())
# -----------------------------
# Encode Categorical Features
# -----------------------------

encoders = {}

categorical_columns = [
    "Category",
    "Sub-Category",
    "Region",
    "Segment"
]

for column in categorical_columns:

    encoder = LabelEncoder()

    X[column] = encoder.fit_transform(X[column])

    encoders[column] = encoder

print("\nEncoded Dataset:")
print(X.head())
# -----------------------------
# Split Dataset
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape :", X_test.shape)
# -----------------------------
# Linear Regression
# -----------------------------

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

print("\nLinear Regression Model Trained Successfully!")

#PREDICT!!!!!

y_pred = linear_model.predict(X_test)

print("\nFirst 10 Predictions:")

print(y_pred[:10])

# -----------------------------
# Evaluate Linear Regression
# -----------------------------

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, y_pred)

print("\n========== Linear Regression ==========")
print("Mean Absolute Error :", mae)
print("Mean Squared Error  :", mse)
print("Root Mean Squared Error :", rmse)
print("R² Score :", r2)

#DECISION TREE REGRESSOR
# -----------------------------
# Decision Tree Regressor
# -----------------------------

decision_tree = DecisionTreeRegressor(random_state=42)
decision_tree.fit(X_train, y_train)

print("\nDecision Tree Model Trained Successfully!")
dt_predictions = decision_tree.predict(X_test)
dt_mae = mean_absolute_error(y_test, dt_predictions)
dt_mse = mean_squared_error(y_test, dt_predictions)
dt_rmse = np.sqrt(dt_mse)
dt_r2 = r2_score(y_test, dt_predictions)

print("\n========== Decision Tree ==========")
print("Mean Absolute Error :", dt_mae)
print("Mean Squared Error  :", dt_mse)
print("Root Mean Squared Error :", dt_rmse)
print("R² Score :", dt_r2)

# -----------------------------
# Random Forest Regressor
# -----------------------------

random_forest = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
random_forest.fit(X_train, y_train)

print("\nRandom Forest Model Trained Successfully!")
rf_predictions = random_forest.predict(X_test)
rf_mae = mean_absolute_error(y_test, rf_predictions)
rf_mse = mean_squared_error(y_test, rf_predictions)
rf_rmse = np.sqrt(rf_mse)
rf_r2 = r2_score(y_test, rf_predictions)

print("\n========== Random Forest ==========")
print("Mean Absolute Error :", rf_mae)
print("Mean Squared Error  :", rf_mse)
print("Root Mean Squared Error :", rf_rmse)
print("R² Score :", rf_r2)

# -----------------------------
# Save Best Model
# -----------------------------

joblib.dump(random_forest, "models/best_model.pkl")
joblib.dump(encoders, "models/encoders.pkl")

print("\nBest model saved successfully!")