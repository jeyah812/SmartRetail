import pandas as pd
import joblib

from src.feature_engineering import add_features
def predict_profit(file_path):

    model = joblib.load("models/best_model.pkl")
    encoders = joblib.load("models/encoders.pkl")

    df = pd.read_csv(file_path, encoding="latin1")

    # Fill missing optional columns

    # Fill missing optional columns using known values from the trained encoders

    if "Sub-Category" not in df.columns:
        df["Sub-Category"] = encoders["Sub-Category"].classes_[0]

    if "Region" not in df.columns:
        df["Region"] = encoders["Region"].classes_[0]

    if "Segment" not in df.columns:
        df["Segment"] = encoders["Segment"].classes_[0]

    if "Order Date" not in df.columns:
        df["Order Date"] = "2026-01-01"

    if "Ship Date" not in df.columns:
        df["Ship Date"] = "2026-01-01"

    # Convert dates
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    df = add_features(df)

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

    categorical_columns = [
        "Category",
        "Sub-Category",
        "Region",
        "Segment"
    ]

    for column in categorical_columns:

        encoder = encoders[column]

        # Replace unseen values with the encoder's first known class
        X[column] = X[column].apply(
            lambda x: x if x in encoder.classes_ else encoder.classes_[0]
        )

        X[column] = encoder.transform(X[column])

    predictions = model.predict(X)

    predicted_profit = predictions.sum()

    return round(predicted_profit, 2)