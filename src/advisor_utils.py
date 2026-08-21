from advisor import get_business_advice


# ============================================================
# AI BUSINESS ADVISOR
# ============================================================

def generate_ai_advice(stats):

    total_sales = stats.get(
        "total_sales",
        0
    )

    total_profit = stats.get(
        "total_profit",
        0
    )

    total_orders = stats.get(
        "total_orders",
        0
    )

    profit_margin = stats.get(
        "profit_margin",
        0
    )

    average_order_value = stats.get(
        "average_order_value",
        0
    )

    average_discount = stats.get(
        "average_discount",
        0
    )

    top_sales_category = stats.get(
        "top_sales_category",
        "Not available"
    )

    top_profit_category = stats.get(
        "top_profit_category",
        "Not available"
    )

    highest_quantity_category = stats.get(
        "highest_quantity_category",
        "Not available"
    )

    top_sales_product = stats.get(
        "top_sales_product",
        "Not available"
    )

    top_profit_product = stats.get(
        "top_profit_product",
        "Not available"
    )

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are SmartRetail AI Advisor.

Analyze the following retail business data.

BUSINESS METRICS
----------------

Total Sales:
${total_sales:,.2f}

Total Profit:
${total_profit:,.2f}

Total Orders:
{total_orders}

Profit Margin:
{profit_margin:.2f}%

Average Order Value:
${average_order_value:,.2f}

Average Discount:
{average_discount:.2f}%

Top Sales Category:
{top_sales_category}

Top Profit Category:
{top_profit_category}

Highest Quantity Category:
{highest_quantity_category}

Top Sales Product/Sub-Category:
{top_sales_product}

Top Profit Product/Sub-Category:
{top_profit_product}


IMPORTANT INSTRUCTIONS
----------------------

Give practical business recommendations based ONLY
on the available metrics.

Do NOT invent product, customer, inventory,
or category information that is not provided.

If a metric says "Not available", clearly mention
that the dataset does not contain enough information.

Structure the response exactly like this:

BUSINESS SUMMARY

• Give 2-3 concise observations about the business.

SALES RECOMMENDATIONS

• Give 2-3 practical sales recommendations.

INVENTORY RECOMMENDATIONS

• Give 2-3 practical inventory recommendations.

PROFIT IMPROVEMENT

• Give 2-3 practical profit improvement recommendations.

PRIORITY ACTIONS

1. Give the most important immediate action.
2. Give the second most important action.
3. Give the third most important action.

Keep the response professional and concise.
"""

    # ========================================================
    # CALL AI
    # ========================================================

    try:

        response = get_business_advice(
            prompt
        )

        if not response:

            return (
                "AI Advisor could not generate "
                "business advice."
            )

        return response

    except Exception as e:

        print(
            "AI Advisor exception:",
            e
        )

        return (
            "AI Advisor is currently unavailable."
        )