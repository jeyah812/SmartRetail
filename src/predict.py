import os
import json

import pandas as pd
import joblib

from src.feature_engineering import add_features


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "best_model.pkl"
)

ENCODER_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "encoders.pkl"
)

METRICS_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "model_metrics.json"
)


# ============================================================
# METRIC VALUE
# ============================================================

def metric_value(metrics, key, decimal_places):

    value = metrics.get(key)

    if value is None:

        return None

    try:

        return round(
            float(value),
            decimal_places
        )

    except (TypeError, ValueError):

        return None


# ============================================================
# PREDICT PROFIT
# ============================================================

def predict_profit(file_path):

    # ========================================================
    # LOAD MODEL
    # ========================================================

    model = joblib.load(
        MODEL_PATH
    )

    encoders = joblib.load(
        ENCODER_PATH
    )

    # ========================================================
    # LOAD METRICS
    # ========================================================

    try:

        with open(
            METRICS_PATH,
            "r"
        ) as f:

            metrics = json.load(
                f
            )

    except (FileNotFoundError, json.JSONDecodeError):

        metrics = {}

    # ========================================================
    # LOAD DATASET
    # ========================================================

    df = pd.read_csv(
        file_path,
        encoding="latin1"
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # ========================================================
    # REQUIRED COLUMNS
    # ========================================================

    required_columns = [

        "Sales",

        "Profit",

        "Quantity",

        "Discount",

        "Category"

    ]

    missing_columns = [

        column

        for column
        in required_columns

        if column not in df.columns

    ]

    if missing_columns:

        raise ValueError(

            "Missing required columns: "
            + ", ".join(
                missing_columns
            )

        )

    # ========================================================
    # NUMERIC CONVERSION
    # ========================================================

    for column in [

        "Sales",

        "Profit",

        "Quantity",

        "Discount"

    ]:

        df[column] = pd.to_numeric(

            df[column],

            errors="coerce"

        )

    # ========================================================
    # REMOVE INVALID ROWS
    # ========================================================

    df = df.dropna(

        subset=[

            "Sales",

            "Profit",

            "Quantity",

            "Discount"

        ]

    )

    if df.empty:

        raise ValueError(
            "No valid data remains after cleaning."
        )

    # ========================================================
    # NORMALIZE DISCOUNT
    # ========================================================

    if df["Discount"].max() > 1:

        df["Discount"] = (
            df["Discount"] / 100
        )

    # ========================================================
    # ACTUAL PROFIT
    # ========================================================

    actual_profit = (
        df["Profit"].sum()
    )

    # ========================================================
    # OPTIONAL COLUMNS
    # ========================================================

    optional_defaults = {

        "Sub-Category":
            "Sub-Category",

        "Region":
            "Region",

        "Segment":
            "Segment"

    }

    for column, encoder_key in (
        optional_defaults.items()
    ):

        if column not in df.columns:

            df[column] = (
                encoders[
                    encoder_key
                ].classes_[0]
            )

    # ========================================================
    # DATE COLUMNS
    # ========================================================

    if "Order Date" not in df.columns:

        df["Order Date"] = (
            "2026-01-01"
        )

    if "Ship Date" not in df.columns:

        df["Ship Date"] = (
            "2026-01-01"
        )

    df["Order Date"] = pd.to_datetime(

        df["Order Date"],

        errors="coerce"

    )

    df["Ship Date"] = pd.to_datetime(

        df["Ship Date"],

        errors="coerce"

    )

    df["Order Date"] = (
        df["Order Date"]
        .fillna(
            pd.Timestamp(
                "2026-01-01"
            )
        )
    )

    df["Ship Date"] = (
        df["Ship Date"]
        .fillna(
            pd.Timestamp(
                "2026-01-01"
            )
        )
    )

    # ========================================================
    # FEATURE ENGINEERING
    # ========================================================

    df = add_features(
        df
    )

    # ========================================================
    # FEATURES
    # ========================================================

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

    X = df[
        features
    ].copy()

    # ========================================================
    # ENCODE CATEGORICAL FEATURES
    # ========================================================

    categorical_columns = [

        "Category",

        "Sub-Category",

        "Region",

        "Segment"

    ]

    for column in categorical_columns:

        encoder = encoders[
            column
        ]

        X[column] = (
            X[column]
            .astype(str)
        )

        known_classes = set(
            encoder.classes_
        )

        X[column] = X[column].apply(

            lambda value:

            value
            if value in known_classes
            else encoder.classes_[0]

        )

        X[column] = (
            encoder.transform(
                X[column]
            )
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    predictions = model.predict(
        X
    )

    predicted_profit = (
        predictions.sum()
    )

    # ========================================================
    # COMPARISON
    # ========================================================

    difference = (
        predicted_profit
        - actual_profit
    )

    if actual_profit != 0:

        deviation_percentage = (

            abs(difference)
            / abs(actual_profit)

        ) * 100

    else:

        deviation_percentage = 0

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "actual_profit":
            round(
                float(
                    actual_profit
                ),
                2
            ),

        "predicted_profit":
            round(
                float(
                    predicted_profit
                ),
                2
            ),

        "difference":
            round(
                float(
                    difference
                ),
                2
            ),

        "deviation_percentage":
            round(
                float(
                    deviation_percentage
                ),
                2
            ),

        "model":
            metrics.get(
                "best_model",
                "Unknown"
            ),

        "r2_score":
            metric_value(
                metrics,
                "r2_score",
                4
            ),

        "r2_percentage":
            metric_value(
                metrics,
                "r2_percentage",
                2
            ),

        "mae":
            metric_value(
                metrics,
                "mae",
                2
            ),

        "rmse":
            metric_value(
                metrics,
                "rmse",
                2
            )
    }


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    dataset_path = os.path.join(

        PROJECT_ROOT,

        "static",

        "uploads",

        "latest.csv"

    )

    result = predict_profit(
        dataset_path
    )

    print()
    print("=" * 60)
    print("SMARTRETAIL PROFIT PREDICTION")
    print("=" * 60)

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )

    print("=" * 60)
