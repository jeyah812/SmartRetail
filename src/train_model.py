import json
import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from src.feature_engineering import add_features


# ============================================================
# 1. LOAD DATASET
# ============================================================

DATASET_PATH = "data/raw/Sample - Superstore.csv"

df = pd.read_csv(
    DATASET_PATH,
    encoding="latin1"
)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()


# ============================================================
# 3. CONVERT DATE COLUMNS
# ============================================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    errors="coerce"
)


# Remove rows where dates could not be converted

df = df.dropna(
    subset=[
        "Order Date",
        "Ship Date"
    ]
)


# ============================================================
# 4. FEATURE ENGINEERING
# ============================================================

df = add_features(df)

print("\nFeature engineering completed!")


# ============================================================
# 5. SELECT FEATURES
# ============================================================

features = [

    "Sales",

    "Quantity",

    "Discount",

    "Discount Impact",

    "Net Sales",

    "Sales Per Unit",

    "Category",

    "Sub-Category",

    "Region",

    "Segment",

    "Shipping Days",

    "Order Year",

    "Order Quarter"

]


X = df[features].copy()

y = df["Profit"].copy()


print("\nFeatures Shape:", X.shape)

print("Target Shape:", y.shape)

print("\nFeature Preview:")

print(
    X.head()
)


# ============================================================
# 6. ENCODE CATEGORICAL FEATURES
# ============================================================

encoders = {}

categorical_columns = [

    "Category",

    "Sub-Category",

    "Region",

    "Segment"

]


for column in categorical_columns:

    encoder = LabelEncoder()

    X[column] = encoder.fit_transform(
        X[column].astype(str)
    )

    encoders[column] = encoder


print("\nCategorical features encoded successfully!")

print("\nEncoded Dataset Preview:")

print(
    X.head()
)


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)


print(
    "\nTraining Data Shape:",
    X_train.shape
)

print(
    "Testing Data Shape :",
    X_test.shape
)


# ============================================================
# 8. LINEAR REGRESSION
# ============================================================

print(
    "\nTraining Linear Regression..."
)


linear_model = LinearRegression()

linear_model.fit(
    X_train,
    y_train
)


linear_predictions = linear_model.predict(
    X_test
)


linear_mae = mean_absolute_error(
    y_test,
    linear_predictions
)


linear_mse = mean_squared_error(
    y_test,
    linear_predictions
)


linear_rmse = np.sqrt(
    linear_mse
)


linear_r2 = r2_score(
    y_test,
    linear_predictions
)


print(
    "\n========== Linear Regression =========="
)

print(
    "Mean Absolute Error :",
    round(linear_mae, 4)
)

print(
    "Mean Squared Error  :",
    round(linear_mse, 4)
)

print(
    "Root Mean Squared Error :",
    round(linear_rmse, 4)
)

print(
    "R² Score :",
    round(linear_r2, 4)
)


# ============================================================
# 9. DECISION TREE
# ============================================================

print(
    "\nTraining Decision Tree..."
)


decision_tree = DecisionTreeRegressor(
    random_state=42
)


decision_tree.fit(
    X_train,
    y_train
)


dt_predictions = decision_tree.predict(
    X_test
)


dt_mae = mean_absolute_error(
    y_test,
    dt_predictions
)


dt_mse = mean_squared_error(
    y_test,
    dt_predictions
)


dt_rmse = np.sqrt(
    dt_mse
)


dt_r2 = r2_score(
    y_test,
    dt_predictions
)


print(
    "\n========== Decision Tree =========="
)

print(
    "Mean Absolute Error :",
    round(dt_mae, 4)
)

print(
    "Mean Squared Error  :",
    round(dt_mse, 4)
)

print(
    "Root Mean Squared Error :",
    round(dt_rmse, 4)
)

print(
    "R² Score :",
    round(dt_r2, 4)
)


# ============================================================
# 10. RANDOM FOREST
# ============================================================

print(
    "\nTraining Random Forest..."
)


random_forest = RandomForestRegressor(

    n_estimators=100,

    random_state=42,

    n_jobs=-1

)


random_forest.fit(
    X_train,
    y_train
)


rf_predictions = random_forest.predict(
    X_test
)


rf_mae = mean_absolute_error(
    y_test,
    rf_predictions
)


rf_mse = mean_squared_error(
    y_test,
    rf_predictions
)


rf_rmse = np.sqrt(
    rf_mse
)


rf_r2 = r2_score(
    y_test,
    rf_predictions
)


print(
    "\n========== Random Forest =========="
)

print(
    "Mean Absolute Error :",
    round(rf_mae, 4)
)

print(
    "Mean Squared Error  :",
    round(rf_mse, 4)
)

print(
    "Root Mean Squared Error :",
    round(rf_rmse, 4)
)

print(
    "R² Score :",
    round(rf_r2, 4)
)


# ============================================================
# 11. STORE MODEL RESULTS
# ============================================================

models = {

    "Linear Regression": {

        "model": linear_model,

        "r2": linear_r2,

        "mae": linear_mae,

        "rmse": linear_rmse,

        "mse": linear_mse

    },

    "Decision Tree": {

        "model": decision_tree,

        "r2": dt_r2,

        "mae": dt_mae,

        "rmse": dt_rmse,

        "mse": dt_mse

    },

    "Random Forest": {

        "model": random_forest,

        "r2": rf_r2,

        "mae": rf_mae,

        "rmse": rf_rmse,

        "mse": rf_mse

    }

}


# ============================================================
# 12. SELECT BEST MODEL
# ============================================================

best_model_name = max(

    models,

    key=lambda name:
    models[name]["r2"]

)


best_model_info = models[
    best_model_name
]


best_model = best_model_info[
    "model"
]


print(
    "\n"
)

print(
    "=" * 60
)

print(
    "BEST MODEL"
)

print(
    "=" * 60
)

print(
    "Model:",
    best_model_name
)

print(
    "R² Score:",
    round(
        best_model_info["r2"],
        4
    )
)

print(
    "R² Percentage:",
    round(
        best_model_info["r2"] * 100,
        2
    ),
    "%"
)

print(
    "MAE:",
    round(
        best_model_info["mae"],
        4
    )
)

print(
    "RMSE:",
    round(
        best_model_info["rmse"],
        4
    )
)


# ============================================================
# 13. SAVE BEST MODEL
# ============================================================

joblib.dump(

    best_model,

    "models/best_model.pkl"

)


# ============================================================
# 14. SAVE ENCODERS
# ============================================================

joblib.dump(

    encoders,

    "models/encoders.pkl"

)


# ============================================================
# 15. SAVE MODEL METRICS
# ============================================================

metrics = {

    "best_model": best_model_name,

    "r2_score": float(
        best_model_info["r2"]
    ),

    "r2_percentage": float(
        best_model_info["r2"] * 100
    ),

    "mae": float(
        best_model_info["mae"]
    ),

    "rmse": float(
        best_model_info["rmse"]
    ),

    "mse": float(
        best_model_info["mse"]
    ),

    "models": {

        "Linear Regression": {

            "r2_score": float(
                linear_r2
            ),

            "mae": float(
                linear_mae
            ),

            "rmse": float(
                linear_rmse
            ),

            "mse": float(
                linear_mse
            )

        },

        "Decision Tree": {

            "r2_score": float(
                dt_r2
            ),

            "mae": float(
                dt_mae
            ),

            "rmse": float(
                dt_rmse
            ),

            "mse": float(
                dt_mse
            )

        },

        "Random Forest": {

            "r2_score": float(
                rf_r2
            ),

            "mae": float(
                rf_mae
            ),

            "rmse": float(
                rf_rmse
            ),

            "mse": float(
                rf_mse
            )

        }

    }

}


with open(

    "models/model_metrics.json",

    "w"

) as f:

    json.dump(

        metrics,

        f,

        indent=4

    )


# ============================================================
# 16. FINAL MESSAGE
# ============================================================

print(
    "\n"
)

print(
    "=" * 60
)

print(
    "MODEL TRAINING COMPLETED"
)

print(
    "=" * 60
)

print(
    "Best Model:",
    best_model_name
)

print(
    "Saved:",
    "models/best_model.pkl"
)

print(
    "Saved:",
    "models/encoders.pkl"
)

print(
    "Saved:",
    "models/model_metrics.json"
)

print(
    "=" * 60
)