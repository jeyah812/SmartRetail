import pandas as pd


def add_features(df):
    """
    Add business and time-based features
    required by the SmartRetail ML model.
    """

    # ========================================================
    # DATE FEATURES
    # ========================================================

    df["Order Year"] = (
        df["Order Date"].dt.year
    )

    df["Order Month"] = (
        df["Order Date"].dt.month_name()
    )

    df["Order Quarter"] = (
        df["Order Date"].dt.quarter
    )

    # ========================================================
    # SHIPPING DURATION
    # ========================================================

    df["Shipping Days"] = (
        df["Ship Date"]
        - df["Order Date"]
    ).dt.days

    # ========================================================
    # PROFIT MARGIN
    # ========================================================

    # This is useful for analysis,
    # but is NOT used as an ML feature
    # because Profit is the prediction target.

    df["Profit Margin"] = (
        (
            df["Profit"]
            / df["Sales"].replace(0, pd.NA)
        ) * 100
    ).round(2)

    # ========================================================
    # DISCOUNT IMPACT
    # ========================================================

    df["Discount Impact"] = (
        df["Sales"]
        * df["Discount"]
    )

    # ========================================================
    # NET SALES
    # ========================================================

    df["Net Sales"] = (
        df["Sales"]
        - df["Discount Impact"]
    )

    # ========================================================
    # SALES PER UNIT
    # ========================================================

    df["Sales Per Unit"] = (
        df["Sales"]
        /
        df["Quantity"].replace(0, 1)
    )

    return df