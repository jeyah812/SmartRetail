from advisor import get_business_advice


def generate_ai_advice(stats):

    prompt = f"""
    Analyze this retail business.

    Total Sales: {stats['total_sales']}
    Total Profit: {stats['total_profit']}
    Total Orders: {stats['total_orders']}

    Give:
    - Sales recommendations
    - Inventory recommendations
    - Profit improvement ideas
    - Customer insights

    Keep the response concise.
    """

    return get_business_advice(prompt)