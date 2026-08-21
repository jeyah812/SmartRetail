import pandas as pd


# ============================================================
# SMARTRETAIL RECOMMENDATION ENGINE
# ============================================================

def generate_recommendations(file_path, predicted_profit=None):
    """
    Generate data-driven retail recommendations.

    The function analyzes:
    - Sales
    - Profit
    - Discount
    - Quantity
    - Category
    - Sub-Category
    - Region
    - Segment

    Returns a dictionary containing:
    - Business status
    - Inventory recommendations
    - Sales recommendations
    - Profit recommendations
    - Key insights
    """


    # ========================================================
    # LOAD DATASET
    # ========================================================

    df = pd.read_csv(
        file_path,
        encoding="latin1"
    )

    df.columns = df.columns.str.strip()


    # ========================================================
    # CONVERT NUMERIC COLUMNS
    # ========================================================

    numeric_columns = [
        "Sales",
        "Profit",
        "Quantity",
        "Discount"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )


    # ========================================================
    # BASIC BUSINESS METRICS
    # ========================================================

    total_sales = (
        df["Sales"].sum()
        if "Sales" in df.columns
        else 0
    )

    total_profit = (
        df["Profit"].sum()
        if "Profit" in df.columns
        else 0
    )

    total_quantity = (
        df["Quantity"].sum()
        if "Quantity" in df.columns
        else 0
    )

    total_orders = len(df)


    # ========================================================
    # PROFIT MARGIN
    # ========================================================

    if total_sales != 0:

        profit_margin = (
            total_profit /
            total_sales
        ) * 100

    else:

        profit_margin = 0


    # ========================================================
    # BUSINESS STATUS
    # ========================================================

    if total_profit < 0:

        business_status = "Loss Risk"

    elif profit_margin < 5:

        business_status = "Low Profitability"

    elif profit_margin < 15:

        business_status = "Moderate Profitability"

    else:

        business_status = "Healthy Profitability"


    # ========================================================
    # KEY INSIGHTS
    # ========================================================

    insights = []


    # --------------------------------------------------------
    # SALES INSIGHT
    # --------------------------------------------------------

    if total_sales > 0:

        insights.append(
            f"Total sales are ${total_sales:,.2f} "
            f"across {total_orders:,} records."
        )


    # --------------------------------------------------------
    # PROFIT INSIGHT
    # --------------------------------------------------------

    insights.append(
        f"Total profit is ${total_profit:,.2f}, "
        f"with an estimated profit margin of "
        f"{profit_margin:.2f}%."
    )


    # ========================================================
    # CATEGORY ANALYSIS
    # ========================================================

    category_analysis = None

    if (
        "Category" in df.columns
        and "Sales" in df.columns
        and "Profit" in df.columns
    ):

        category_analysis = (
            df.groupby("Category")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Quantity=("Quantity", "sum")
                if "Quantity" in df.columns
                else ("Sales", "count")
            )
            .sort_values(
                "Sales",
                ascending=False
            )
        )


        # ----------------------------------------------------
        # BEST CATEGORY
        # ----------------------------------------------------

        if not category_analysis.empty:

            best_category = (
                category_analysis["Sales"]
                .idxmax()
            )

            insights.append(
                f"{best_category} is the highest-sales category."
            )


        # ----------------------------------------------------
        # WORST PROFIT CATEGORY
        # ----------------------------------------------------

        if not category_analysis.empty:

            worst_category = (
                category_analysis["Profit"]
                .idxmin()
            )

            worst_profit = (
                category_analysis.loc[
                    worst_category,
                    "Profit"
                ]
            )

            if worst_profit < 0:

                insights.append(
                    f"{worst_category} is generating "
                    f"a loss of ${abs(worst_profit):,.2f}."
                )


    # ========================================================
    # INVENTORY RECOMMENDATIONS
    # ========================================================

    inventory_recommendations = []


    if category_analysis is not None:

        # ----------------------------------------------------
        # HIGH DEMAND CATEGORIES
        # ----------------------------------------------------

        if "Quantity" in category_analysis.columns:

            high_demand = (
                category_analysis["Quantity"]
                .idxmax()
            )

            inventory_recommendations.append(
                f"Consider maintaining higher stock levels "
                f"for {high_demand}, which has the highest "
                f"recorded quantity."
            )


        # ----------------------------------------------------
        # LOSS-MAKING CATEGORY
        # ----------------------------------------------------

        loss_categories = category_analysis[
            category_analysis["Profit"] < 0
        ]

        if not loss_categories.empty:

            loss_category = (
                loss_categories["Profit"]
                .idxmin()
            )

            inventory_recommendations.append(
                f"Review inventory levels for "
                f"{loss_category} before increasing stock, "
                f"as it currently generates negative profit."
            )


        # ----------------------------------------------------
        # PROFITABLE CATEGORY
        # ----------------------------------------------------

        profitable_categories = category_analysis[
            category_analysis["Profit"] > 0
        ]

        if not profitable_categories.empty:

            profitable_category = (
                profitable_categories["Profit"]
                .idxmax()
            )

            inventory_recommendations.append(
                f"Prioritize stock availability for "
                f"{profitable_category}, which generates "
                f"the highest category profit."
            )


    # ========================================================
    # FALLBACK INVENTORY MESSAGE
    # ========================================================

    if not inventory_recommendations:

        inventory_recommendations.append(
            "Insufficient category information "
            "is available for detailed inventory recommendations."
        )


    # ========================================================
    # DISCOUNT ANALYSIS
    # ========================================================

    sales_recommendations = []


    if (
        "Discount" in df.columns
        and "Profit" in df.columns
    ):

        average_discount = (
            df["Discount"]
            .mean()
        )

        average_profit = (
            df["Profit"]
            .mean()
        )


        # ----------------------------------------------------
        # HANDLE PERCENTAGE DISCOUNTS
        # ----------------------------------------------------

        if average_discount > 1:

            average_discount = (
                average_discount / 100
            )


        if average_discount >= 0.30:

            sales_recommendations.append(
                f"Average discount is approximately "
                f"{average_discount * 100:.1f}%. "
                f"Review high-discount products because "
                f"excessive discounts may reduce profitability."
            )

        elif average_discount >= 0.15:

            sales_recommendations.append(
                f"Average discount is approximately "
                f"{average_discount * 100:.1f}%. "
                f"Monitor discount-heavy products for "
                f"profit erosion."
            )

        else:

            sales_recommendations.append(
                f"Average discount is approximately "
                f"{average_discount * 100:.1f}%. "
                f"Current discount levels appear relatively moderate."
            )


    # ========================================================
    # PROFIT RECOMMENDATIONS
    # ========================================================

    profit_recommendations = []


    if total_profit < 0:

        profit_recommendations.append(
            "Prioritize loss reduction by reviewing "
            "pricing, discounts and loss-making products."
        )

    elif profit_margin < 5:

        profit_recommendations.append(
            "Profit margin is low. Review pricing and "
            "discount strategies before increasing sales volume."
        )

    elif profit_margin < 15:

        profit_recommendations.append(
            "Look for opportunities to improve margins "
            "through better pricing and product mix."
        )

    else:

        profit_recommendations.append(
            "Profitability is relatively healthy. "
            "Focus on scaling high-performing products "
            "without significantly increasing discounts."
        )


    # ========================================================
    # ML PREDICTION INSIGHT
    # ========================================================

    prediction_status = None


    if predicted_profit is not None:

        if predicted_profit < 0:

            prediction_status = (
                "The ML model indicates a potential loss. "
                "Review pricing, discounts and inventory decisions."
            )

        elif predicted_profit > total_profit:

            prediction_status = (
                "The ML model predicts profit above the "
                "current recorded profit. Treat this as a "
                "potential opportunity rather than a guarantee."
            )

        else:

            prediction_status = (
                "The ML model predicts profit below the "
                "current recorded profit. Review factors "
                "that may be affecting profitability."
            )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "business_status":
            business_status,

        "total_sales":
            round(float(total_sales), 2),

        "total_profit":
            round(float(total_profit), 2),

        "profit_margin":
            round(float(profit_margin), 2),

        "total_orders":
            int(total_orders),

        "total_quantity":
            int(total_quantity),

        "insights":
            insights,

        "inventory_recommendations":
            inventory_recommendations,

        "sales_recommendations":
            sales_recommendations,

        "profit_recommendations":
            profit_recommendations,

        "prediction_status":
            prediction_status

    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = generate_recommendations(
        "static/uploads/latest.csv",
        predicted_profit=8981.21
    )

    print("\n")
    print("=" * 60)
    print("SMARTRETAIL RECOMMENDATION ENGINE")
    print("=" * 60)

    print("\nBusiness Status:")
    print(result["business_status"])

    print("\nKey Insights:")

    for insight in result["insights"]:
        print("-", insight)

    print("\nInventory Recommendations:")

    for recommendation in result[
        "inventory_recommendations"
    ]:
        print("-", recommendation)

    print("\nSales Recommendations:")

    for recommendation in result[
        "sales_recommendations"
    ]:
        print("-", recommendation)

    print("\nProfit Recommendations:")

    for recommendation in result[
        "profit_recommendations"
    ]:
        print("-", recommendation)

    print("\nML Prediction:")

    print(
        result["prediction_status"]
    )