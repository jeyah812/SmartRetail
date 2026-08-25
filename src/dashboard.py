import json
import os

import pandas as pd
import matplotlib

# ============================================================
# MATPLOTLIB BACKEND
# ============================================================

matplotlib.use("Agg")

import matplotlib.pyplot as plt

# ============================================================
# CHART FOLDER
# ============================================================

CHART_FOLDER = "static/images"

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

METRICS_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "model_metrics.json"
)


# ============================================================
# MODEL METRICS
# ============================================================

def load_model_metrics():

    try:

        with open(
            METRICS_PATH,
            "r"
        ) as f:

            metrics = json.load(
                f
            )

        if isinstance(
            metrics,
            dict
        ):

            return metrics

    except (OSError, json.JSONDecodeError):

        pass

    return {}


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(file_path):

    try:

        df = pd.read_csv(
            file_path,
            encoding="latin1"
        )

    except UnicodeDecodeError:

        df = pd.read_csv(
            file_path,
            encoding="utf-8"
        )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


# ============================================================
# SAFE NUMERIC CONVERSION
# ============================================================

def numeric_series(df, column):

    if column not in df.columns:

        return pd.Series(
            dtype="float64"
        )

    return pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_stats(file_path):

    df = load_dataset(
        file_path
    )

    stats = {}

    metrics = load_model_metrics()

    stats["r2_score"] = metrics.get(
        "r2_score"
    )

    stats["r2_percentage"] = metrics.get(
        "r2_percentage"
    )

    stats["model_name"] = metrics.get(
        "best_model"
    )

    # ========================================================
    # SALES
    # ========================================================

    sales = numeric_series(
        df,
        "Sales"
    )

    total_sales = sales.sum()

    stats["total_sales"] = round(
        float(total_sales),
        2
    )

    # ========================================================
    # PROFIT
    # ========================================================

    profit = numeric_series(
        df,
        "Profit"
    )

    total_profit = profit.sum()

    stats["total_profit"] = round(
        float(total_profit),
        2
    )

    # ========================================================
    # ORDERS
    # ========================================================

    if "Order ID" in df.columns:

        orders = (
            df["Order ID"]
            .dropna()
            .astype(str)
            .nunique()
        )

    else:

        orders = len(df)

    stats["total_orders"] = int(
        orders
    )

    # ========================================================
    # PROFIT MARGIN
    # ========================================================

    if total_sales != 0:

        profit_margin = (
            total_profit
            / total_sales
        ) * 100

    else:

        profit_margin = 0

    stats["profit_margin"] = round(
        float(profit_margin),
        2
    )

    # ========================================================
    # AVERAGE ORDER VALUE
    # ========================================================

    if orders > 0:

        average_order_value = (
            total_sales
            / orders
        )

    else:

        average_order_value = 0

    stats[
        "average_order_value"
    ] = round(
        float(average_order_value),
        2
    )

    # ========================================================
    # AVERAGE DISCOUNT
    # ========================================================

    discount = numeric_series(
        df,
        "Discount"
    ).dropna()

    if not discount.empty:

        average_discount = (
            discount.mean()
        )

        # Convert 0.10 → 10%
        if average_discount <= 1:

            average_discount *= 100

    else:

        average_discount = 0

    stats[
        "average_discount"
    ] = round(
        float(average_discount),
        2
    )

    # ========================================================
    # TOP SALES CATEGORY
    # ========================================================

    stats[
        "top_sales_category"
    ] = "Not available"

    if (
        "Category" in df.columns
        and "Sales" in df.columns
    ):

        temp = df.copy()

        temp["Sales"] = pd.to_numeric(
            temp["Sales"],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[
                "Category",
                "Sales"
            ]
        )

        if not temp.empty:

            category_sales = (
                temp
                .groupby("Category")[
                    "Sales"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if not category_sales.empty:

                stats[
                    "top_sales_category"
                ] = str(
                    category_sales.index[0]
                )

    # ========================================================
    # TOP PROFIT CATEGORY
    # ========================================================

    stats[
        "top_profit_category"
    ] = "Not available"

    if (
        "Category" in df.columns
        and "Profit" in df.columns
    ):

        temp = df.copy()

        temp["Profit"] = pd.to_numeric(
            temp["Profit"],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[
                "Category",
                "Profit"
            ]
        )

        if not temp.empty:

            category_profit = (
                temp
                .groupby("Category")[
                    "Profit"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if not category_profit.empty:

                stats[
                    "top_profit_category"
                ] = str(
                    category_profit.index[0]
                )

    # ========================================================
    # HIGHEST QUANTITY CATEGORY
    # ========================================================

    stats[
        "highest_quantity_category"
    ] = "Not available"

    if (
        "Category" in df.columns
        and "Quantity" in df.columns
    ):

        temp = df.copy()

        temp["Quantity"] = pd.to_numeric(
            temp["Quantity"],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[
                "Category",
                "Quantity"
            ]
        )

        if not temp.empty:

            category_quantity = (
                temp
                .groupby("Category")[
                    "Quantity"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if not category_quantity.empty:

                stats[
                    "highest_quantity_category"
                ] = str(
                    category_quantity.index[0]
                )

    # ========================================================
    # TOP SALES PRODUCT / SUB-CATEGORY
    # ========================================================

    stats[
        "top_sales_product"
    ] = "Not available"

    product_column = None

    if "Product Name" in df.columns:

        product_column = "Product Name"

    elif "Sub-Category" in df.columns:

        product_column = "Sub-Category"

    if (
        product_column
        and "Sales" in df.columns
    ):

        temp = df.copy()

        temp["Sales"] = pd.to_numeric(
            temp["Sales"],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[
                product_column,
                "Sales"
            ]
        )

        if not temp.empty:

            grouped = (
                temp
                .groupby(product_column)[
                    "Sales"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if not grouped.empty:

                stats[
                    "top_sales_product"
                ] = str(
                    grouped.index[0]
                )

    # ========================================================
    # TOP PROFIT PRODUCT / SUB-CATEGORY
    # ========================================================

    stats[
        "top_profit_product"
    ] = "Not available"

    if (
        product_column
        and "Profit" in df.columns
    ):

        temp = df.copy()

        temp["Profit"] = pd.to_numeric(
            temp["Profit"],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[
                product_column,
                "Profit"
            ]
        )

        if not temp.empty:

            grouped = (
                temp
                .groupby(product_column)[
                    "Profit"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if not grouped.empty:

                stats[
                    "top_profit_product"
                ] = str(
                    grouped.index[0]
                )

    return stats


# ============================================================
# FIND DATE COLUMNS
# ============================================================

def find_date_columns(df):

    date_columns = []

    for column in df.columns:

        if (
            df[column].dtype == "object"
            or str(
                df[column].dtype
            ) == "category"
        ):

            try:

                converted = pd.to_datetime(
                    df[column],
                    errors="coerce",
                    format="mixed"
                )

                valid_ratio = (
                    converted.notna().mean()
                )

                if valid_ratio >= 0.70:

                    date_columns.append(
                        column
                    )

            except Exception:

                pass

    return date_columns


# ============================================================
# GENERATE DASHBOARD CHARTS
# ============================================================

def generate_dashboard_charts(file_path):

    df = load_dataset(
        file_path
    )

    os.makedirs(
        CHART_FOLDER,
        exist_ok=True
    )

    charts = []

    # ========================================================
    # REMOVE OLD CHARTS
    # ========================================================

    old_charts = [
        "time_series.png",
        "category_chart.png",
        "distribution_chart.png",
        "numeric_distribution.png"
    ]

    for filename in old_charts:

        filepath = os.path.join(
            CHART_FOLDER,
            filename
        )

        if os.path.exists(filepath):

            try:

                os.remove(
                    filepath
                )

            except Exception:

                pass

    # ========================================================
    # NUMERIC COLUMNS
    # ========================================================

    numeric_columns = (
        df
        .select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    # ========================================================
    # CATEGORICAL COLUMNS
    # ========================================================

    categorical_columns = (
        df
        .select_dtypes(
            include=[
                "object",
                "category"
            ]
        )
        .columns
        .tolist()
    )

    # ========================================================
    # DATE COLUMNS
    # ========================================================

    date_columns = (
        find_date_columns(df)
    )

    # ========================================================
    # CHART 1 — SALES OVER TIME
    # ========================================================

    if (
        date_columns
        and "Sales" in df.columns
    ):

        date_col = (
            "Order Date"
            if "Order Date"
            in date_columns
            else date_columns[0]
        )

        date_series = pd.to_datetime(
            df[date_col],
            errors="coerce",
            format="mixed"
        )

        sales_series = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        )

        temp = pd.DataFrame({

            "date": date_series,

            "sales": sales_series

        })

        temp = temp.dropna(
            subset=[
                "date",
                "sales"
            ]
        )

        if not temp.empty:

            monthly = (
                temp
                .groupby(
                    temp["date"]
                    .dt
                    .to_period("M")
                )["sales"]
                .sum()
            )

            if not monthly.empty:

                plt.figure(
                    figsize=(9, 4.5)
                )

                plt.plot(
                    monthly.index.astype(str),
                    monthly.values,
                    marker="o",
                    linewidth=3
                )

                plt.title(
                    "Sales Over Time"
                )

                plt.xlabel(
                    "Month"
                )

                plt.ylabel(
                    "Sales"
                )

                plt.xticks(
                    rotation=45
                )

                plt.grid(
                    True,
                    alpha=0.3
                )

                plt.tight_layout()

                filename = (
                    "time_series.png"
                )

                plt.savefig(
                    os.path.join(
                        CHART_FOLDER,
                        filename
                    ),
                    bbox_inches="tight"
                )

                plt.close()

                charts.append({

                    "title":
                        "Sales Over Time",

                    "image":
                        filename

                })

    # ========================================================
    # CHART 2 — SALES BY CATEGORY
    # ========================================================

    category_col = None

    preferred_categories = [

        "Category",

        "Sub-Category",

        "Product Name",

        "Region",

        "Segment",

        "City",

        "State",

        "Country"

    ]

    for preferred in preferred_categories:

        if preferred in categorical_columns:

            category_col = preferred

            break

    if category_col is None:

        if categorical_columns:

            category_col = (
                categorical_columns[0]
            )

    if (
        category_col
        and "Sales" in df.columns
    ):

        temp = df.copy()

        temp["Sales"] = pd.to_numeric(
            temp["Sales"],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[
                category_col,
                "Sales"
            ]
        )

        grouped = (
            temp
            .groupby(category_col)[
                "Sales"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
        )

        if not grouped.empty:

            plt.figure(
                figsize=(9, 4.5)
            )

            grouped.plot(
                kind="bar"
            )

            plt.title(
                f"Sales by {category_col}"
            )

            plt.xlabel(
                category_col
            )

            plt.ylabel(
                "Sales"
            )

            plt.xticks(
                rotation=45,
                ha="right"
            )

            plt.tight_layout()

            filename = (
                "category_chart.png"
            )

            plt.savefig(
                os.path.join(
                    CHART_FOLDER,
                    filename
                ),
                bbox_inches="tight"
            )

            plt.close()

            charts.append({

                "title":
                    f"Sales by {category_col}",

                "image":
                    filename

            })

    # ========================================================
    # CHART 3 — CATEGORY DISTRIBUTION
    # ========================================================

    if category_col:

        counts = (
            df[category_col]
            .dropna()
            .value_counts()
            .head(10)
        )

        if not counts.empty:

            plt.figure(
                figsize=(9, 4.5)
            )

            counts.plot(
                kind="bar"
            )

            plt.title(
                f"{category_col} Distribution"
            )

            plt.xlabel(
                category_col
            )

            plt.ylabel(
                "Count"
            )

            plt.xticks(
                rotation=45,
                ha="right"
            )

            plt.tight_layout()

            filename = (
                "distribution_chart.png"
            )

            plt.savefig(
                os.path.join(
                    CHART_FOLDER,
                    filename
                ),
                bbox_inches="tight"
            )

            plt.close()

            charts.append({

                "title":
                    f"{category_col} Distribution",

                "image":
                    filename

            })

    # ========================================================
    # CHART 4 — SALES DISTRIBUTION
    # ========================================================

    if "Sales" in df.columns:

        values = (
            pd.to_numeric(
                df["Sales"],
                errors="coerce"
            )
            .dropna()
        )

        if not values.empty:

            plt.figure(
                figsize=(9, 4.5)
            )

            values.plot(
                kind="hist",
                bins=20
            )

            plt.title(
                "Sales Distribution"
            )

            plt.xlabel(
                "Sales"
            )

            plt.ylabel(
                "Frequency"
            )

            plt.tight_layout()

            filename = (
                "numeric_distribution.png"
            )

            plt.savefig(
                os.path.join(
                    CHART_FOLDER,
                    filename
                ),
                bbox_inches="tight"
            )

            plt.close()

            charts.append({

                "title":
                    "Sales Distribution",

                "image":
                    filename

            })

    return charts
