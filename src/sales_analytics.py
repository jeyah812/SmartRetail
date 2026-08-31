import os

import pandas as pd


# ============================================================
# SALES ANALYTICS
# ============================================================


REQUIRED_COLUMNS = [
    "Sales",
    "Profit",
    "Quantity",
    "Discount",
    "Category",
    "Product Type",
    "Date"
]


def load_sales_data(sales_file):

    if not os.path.exists(sales_file):

        raise FileNotFoundError(
            f"Sales dataset not found: {sales_file}"
        )

    sales = pd.read_csv(
        sales_file
    )

    # --------------------------------------------------------
    # Clean column names
    # --------------------------------------------------------

    sales.columns = (
        sales.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in sales.columns
    ]

    if missing_columns:

        raise ValueError(
            "Sales dataset is missing required columns: "
            +
            ", ".join(
                missing_columns
            )
        )

    # --------------------------------------------------------
    # Convert numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "Sales",
        "Profit",
        "Quantity",
        "Discount"
    ]

    for column in numeric_columns:

        sales[column] = pd.to_numeric(
            sales[column],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    sales["Date"] = pd.to_datetime(
        sales["Date"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Remove rows with invalid essential data
    # --------------------------------------------------------

    sales = sales.dropna(
        subset=[
            "Sales",
            "Profit",
            "Quantity"
        ]
    )

    return sales


# ============================================================
# MAIN ANALYTICS FUNCTION
# ============================================================


def get_sales_analytics(sales_file):

    sales = load_sales_data(
        sales_file
    )

    # --------------------------------------------------------
    # BASIC KPIs
    # --------------------------------------------------------

    total_sales = sales[
        "Sales"
    ].sum()

    total_profit = sales[
        "Profit"
    ].sum()

    total_quantity = sales[
        "Quantity"
    ].sum()

    total_records = len(
        sales
    )

    average_sale = (
        total_sales
        / total_records
        if total_records > 0
        else 0
    )

    profit_margin = (
        (
            total_profit
            / total_sales
        )
        * 100
        if total_sales != 0
        else 0
    )

    average_discount = (
        sales["Discount"].mean()
        if len(sales) > 0
        else 0
    )


    # ========================================================
    # SALES BY CATEGORY
    # ========================================================

    category_sales = (
        sales
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    category_sales_data = [
        {
            "category": str(
                category
            ),
            "sales": round(
                float(value),
                2
            )
        }

        for category, value
        in category_sales.items()
    ]


    # ========================================================
    # PROFIT BY CATEGORY
    # ========================================================

    category_profit = (
        sales
        .groupby("Category")["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    category_profit_data = [
        {
            "category": str(
                category
            ),
            "profit": round(
                float(value),
                2
            )
        }

        for category, value
        in category_profit.items()
    ]


    # ========================================================
    # QUANTITY BY CATEGORY
    # ========================================================

    category_quantity = (
        sales
        .groupby("Category")["Quantity"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    category_quantity_data = [
        {
            "category": str(
                category
            ),
            "quantity": int(
                value
            )
        }

        for category, value
        in category_quantity.items()
    ]


    # ========================================================
    # SALES TREND
    # ========================================================

    valid_dates = sales[
        sales["Date"].notna()
    ].copy()

    if len(valid_dates) > 0:

        sales_trend = (
            valid_dates
            .groupby(
                valid_dates["Date"]
                .dt.strftime("%Y-%m-%d")
            )["Sales"]
            .sum()
        )

        sales_trend = (
            sales_trend
            .sort_index()
        )

    else:

        sales_trend = pd.Series(
            dtype=float
        )


    sales_trend_data = [
        {
            "date": str(
                date
            ),
            "sales": round(
                float(value),
                2
            )
        }

        for date, value
        in sales_trend.items()
    ]


    # ========================================================
    # PROFIT TREND
    # ========================================================

    if len(valid_dates) > 0:

        profit_trend = (
            valid_dates
            .groupby(
                valid_dates["Date"]
                .dt.strftime("%Y-%m-%d")
            )["Profit"]
            .sum()
        )

        profit_trend = (
            profit_trend
            .sort_index()
        )

    else:

        profit_trend = pd.Series(
            dtype=float
        )


    profit_trend_data = [
        {
            "date": str(
                date
            ),
            "profit": round(
                float(value),
                2
            )
        }

        for date, value
        in profit_trend.items()
    ]


    # ========================================================
    # PRODUCT PERFORMANCE
    # ========================================================

    product_performance = (
        sales
        .groupby("Product Type")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    product_performance_data = []

    for product, row in (
        product_performance
        .head(10)
        .iterrows()
    ):

        product_performance_data.append(
            {
                "product": str(
                    product
                ),
                "sales": round(
                    float(
                        row["Sales"]
                    ),
                    2
                ),
                "profit": round(
                    float(
                        row["Profit"]
                    ),
                    2
                ),
                "quantity": int(
                    row["Quantity"]
                )
            }
        )


    # ========================================================
    # TOP PERFORMERS
    # ========================================================

    if len(category_sales) > 0:

        best_sales_category = str(
            category_sales
            .index[0]
        )

        best_sales_value = round(
            float(
                category_sales.iloc[0]
            ),
            2
        )

    else:

        best_sales_category = "N/A"
        best_sales_value = 0


    if len(category_profit) > 0:

        best_profit_category = str(
            category_profit
            .index[0]
        )

        best_profit_value = round(
            float(
                category_profit.iloc[0]
            ),
            2
        )

    else:

        best_profit_category = "N/A"
        best_profit_value = 0


    if len(product_performance) > 0:

        top_product = str(
            product_performance
            .index[0]
        )

        top_product_sales = round(
            float(
                product_performance.iloc[0][
                    "Sales"
                ]
            ),
            2
        )

    else:

        top_product = "N/A"
        top_product_sales = 0


    # ========================================================
    # BUSINESS INSIGHTS
    # ========================================================

    insights = []


    if best_sales_category != "N/A":

        insights.append(
            f"{best_sales_category} "
            f"generated the highest sales "
            f"of ₹{best_sales_value:,.2f}."
        )


    if best_profit_category != "N/A":

        insights.append(
            f"{best_profit_category} "
            f"generated the highest profit "
            f"of ₹{best_profit_value:,.2f}."
        )


    if top_product != "N/A":

        insights.append(
            f"{top_product} "
            f"is the top-performing product "
            f"by sales with ₹{top_product_sales:,.2f}."
        )


    insights.append(
        f"The average sale value is "
        f"₹{average_sale:,.2f}."
    )


    if profit_margin >= 20:

        insights.append(
            f"Overall profit margin is "
            f"{profit_margin:.1f}%, indicating "
            "strong profitability."
        )

    elif profit_margin >= 10:

        insights.append(
            f"Overall profit margin is "
            f"{profit_margin:.1f}%, indicating "
            "moderate profitability."
        )

    else:

        insights.append(
            f"Overall profit margin is "
            f"{profit_margin:.1f}%. "
            "Profitability should be monitored."
        )


    # ========================================================
    # RETURN ANALYTICS
    # ========================================================

    return {

        # Basic KPIs
        "total_sales":
            round(
                float(total_sales),
                2
            ),

        "total_profit":
            round(
                float(total_profit),
                2
            ),

        "total_quantity":
            int(
                total_quantity
            ),

        "total_records":
            int(
                total_records
            ),

        "average_sale":
            round(
                float(average_sale),
                2
            ),

        "profit_margin":
            round(
                float(profit_margin),
                2
            ),

        "average_discount":
            round(
                float(average_discount),
                4
            ),

        # Category analytics
        "category_sales":
            category_sales_data,

        "category_profit":
            category_profit_data,

        "category_quantity":
            category_quantity_data,

        # Trends
        "sales_trend":
            sales_trend_data,

        "profit_trend":
            profit_trend_data,

        # Product analytics
        "product_performance":
            product_performance_data,

        # Top performers
        "best_sales_category":
            best_sales_category,

        "best_sales_value":
            best_sales_value,

        "best_profit_category":
            best_profit_category,

        "best_profit_value":
            best_profit_value,

        "top_product":
            top_product,

        "top_product_sales":
            top_product_sales,

        # Insights
        "insights":
            insights
    }