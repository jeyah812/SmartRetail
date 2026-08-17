import pandas as pd


def add_features(df):
    """
    Adds new business features to the dataset.
    """

    # -------------------------
    # Date Features
    # -------------------------
    df["Order Year"] = df["Order Date"].dt.year
    df["Order Month"] = df["Order Date"].dt.month_name()
    df["Order Quarter"] = df["Order Date"].dt.quarter

    # -------------------------
    # Shipping Duration
    # -------------------------
    df["Shipping Days"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    # -------------------------
    # Profit Margin
    # -------------------------
    df["Profit Margin"] = (
        (df["Profit"] / df["Sales"]) * 100
    ).round(2)

    return df