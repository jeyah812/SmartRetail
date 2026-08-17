import pandas as pd
import matplotlib

# IMPORTANT:
# Use a non-GUI backend because Flask runs the chart generation
# on the server and does not need to display Matplotlib windows.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


# ============================================================
# CHART FOLDER
# ============================================================

CHART_FOLDER = "static/images"


# ============================================================
# HELPER: READ DATASET
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

    return df


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_stats(file_path):

    df = load_dataset(file_path)

    stats = {}

    # --------------------------------------------------------
    # TOTAL SALES
    # --------------------------------------------------------

    if "Sales" in df.columns:

        sales = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        )

        stats["total_sales"] = round(
            sales.sum(),
            2
        )

    else:

        stats["total_sales"] = 0


    # --------------------------------------------------------
    # TOTAL PROFIT
    # --------------------------------------------------------

    if "Profit" in df.columns:

        profit = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        )

        stats["total_profit"] = round(
            profit.sum(),
            2
        )

    else:

        stats["total_profit"] = 0


    # --------------------------------------------------------
    # TOTAL RECORDS
    # --------------------------------------------------------

    stats["total_orders"] = len(df)


    return stats


# ============================================================
# FIND DATE COLUMNS
# ============================================================

def find_date_columns(df):

    date_columns = []

    for column in df.columns:

        # Only try object/string columns.
        # Numeric columns should not be interpreted as dates.
        if (
            df[column].dtype == "object"
            or str(df[column].dtype) == "category"
        ):

            try:

                converted = pd.to_datetime(
                    df[column],
                    errors="coerce",
                    format="mixed"
                )

                valid_ratio = converted.notna().mean()

                # Consider it a date column only when
                # at least 70% of the values are valid dates.
                if valid_ratio >= 0.70:

                    date_columns.append(column)

            except Exception:

                pass

    return date_columns


# ============================================================
# GENERATE DASHBOARD CHARTS
# ============================================================

def generate_dashboard_charts(file_path):

    df = load_dataset(file_path)

    os.makedirs(
        CHART_FOLDER,
        exist_ok=True
    )

    charts = []


    # ========================================================
    # REMOVE OLD GENERATED CHARTS
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
                os.remove(filepath)

            except Exception:
                pass


    # ========================================================
    # IDENTIFY NUMERIC COLUMNS
    # ========================================================

    numeric_columns = (
        df
        .select_dtypes(include=["number"])
        .columns
        .tolist()
    )


    # ========================================================
    # IDENTIFY CATEGORICAL COLUMNS
    # ========================================================

    categorical_columns = (
        df
        .select_dtypes(
            include=["object", "category"]
        )
        .columns
        .tolist()
    )


    # ========================================================
    # IDENTIFY DATE COLUMNS
    # ========================================================

    date_columns = find_date_columns(df)


    # ========================================================
    # CHART 1
    # DATE + NUMERIC
    # TIME SERIES
    # ========================================================

    if date_columns and numeric_columns:

        date_col = date_columns[0]

        value_col = numeric_columns[0]


        # ----------------------------------------------------
        # IMPORTANT:
        # Convert the date column ONCE and store the result.
        # We then use this converted Series instead of
        # calling .dt on the original DataFrame column.
        # ----------------------------------------------------

        date_series = pd.to_datetime(
            df[date_col],
            errors="coerce",
            format="mixed"
        )


        value_series = pd.to_numeric(
            df[value_col],
            errors="coerce"
        )


        temp = pd.DataFrame({

            "date": date_series,

            "value": value_series

        })


        temp = temp.dropna(
            subset=["date", "value"]
        )


        # Only continue if there is usable data.

        if not temp.empty:

            # ------------------------------------------------
            # MONTHLY AGGREGATION
            # ------------------------------------------------

            monthly = (
                temp
                .groupby(
                    temp["date"].dt.to_period("M")
                )["value"]
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
                    f"{value_col} Over Time"
                )


                plt.xlabel(
                    "Month"
                )


                plt.ylabel(
                    value_col
                )


                plt.xticks(
                    rotation=45
                )


                plt.grid(
                    True,
                    alpha=0.3
                )


                plt.tight_layout()


                filename = "time_series.png"


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
                        f"{value_col} Over Time",

                    "image":
                        filename

                })


    # ========================================================
    # CHART 2
    # CATEGORICAL + NUMERIC
    # ========================================================

    if categorical_columns and numeric_columns:

        # Try to choose a useful categorical column.
        # Product / Category / Region / Segment etc.
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


        category_col = None


        for preferred in preferred_categories:

            if preferred in categorical_columns:

                category_col = preferred

                break


        # If none of the preferred columns exist,
        # use the first categorical column.

        if category_col is None:

            category_col = categorical_columns[0]


        # Prefer Sales if available.

        if "Sales" in numeric_columns:

            value_col = "Sales"

        elif "Profit" in numeric_columns:

            value_col = "Profit"

        else:

            value_col = numeric_columns[0]


        temp = df.copy()


        temp[value_col] = pd.to_numeric(
            temp[value_col],
            errors="coerce"
        )


        temp = temp.dropna(
            subset=[
                category_col,
                value_col
            ]
        )


        grouped = (

            temp
            .groupby(category_col)[value_col]
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
                f"{value_col} by {category_col}"
            )


            plt.xlabel(
                category_col
            )


            plt.ylabel(
                value_col
            )


            plt.xticks(
                rotation=45,
                ha="right"
            )


            plt.tight_layout()


            filename = "category_chart.png"


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
                    f"{value_col} by {category_col}",

                "image":
                    filename

            })


    # ========================================================
    # CHART 3
    # CATEGORICAL DISTRIBUTION
    # ========================================================

    if categorical_columns:

        category_col = None


        preferred_categories = [
            "Category",
            "Sub-Category",
            "Region",
            "Segment",
            "State",
            "Country"
        ]


        for preferred in preferred_categories:

            if preferred in categorical_columns:

                category_col = preferred

                break


        if category_col is None:

            category_col = categorical_columns[0]


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


            filename = "distribution_chart.png"


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
    # CHART 4
    # NUMERIC DISTRIBUTION
    # ========================================================

    if numeric_columns:

        # Prefer Sales for retail datasets.

        if "Sales" in numeric_columns:

            value_col = "Sales"

        elif "Profit" in numeric_columns:

            value_col = "Profit"

        else:

            value_col = numeric_columns[0]


        values = pd.to_numeric(
            df[value_col],
            errors="coerce"
        ).dropna()


        if not values.empty:

            plt.figure(
                figsize=(9, 4.5)
            )


            values.plot(
                kind="hist",
                bins=20
            )


            plt.title(
                f"{value_col} Distribution"
            )


            plt.xlabel(
                value_col
            )


            plt.ylabel(
                "Frequency"
            )


            plt.tight_layout()


            filename = "numeric_distribution.png"


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
                    f"{value_col} Distribution",

                "image":
                    filename

            })


    # ========================================================
    # RETURN ALL GENERATED CHARTS
    # ========================================================

    return charts