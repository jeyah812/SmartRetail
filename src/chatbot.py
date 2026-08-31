import os
import pandas as pd

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LATEST_FILE = os.path.join(
    PROJECT_ROOT,
    "static",
    "uploads",
    "latest.csv"
)

INVENTORY_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw",
    "inventory.csv"
)


# ============================================================
# GROQ CLIENT
# ============================================================

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# LOAD LATEST SALES DATA
# ============================================================

def load_latest_sales():

    if not os.path.exists(LATEST_FILE):
        return None

    try:

        df = pd.read_csv(
            LATEST_FILE
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return df

    except Exception as error:

        print(
            "Sales CSV Error:",
            error
        )

        return None


# ============================================================
# LOAD INVENTORY DATA
# ============================================================

def load_inventory():

    if not os.path.exists(INVENTORY_FILE):
        return None

    try:

        df = pd.read_csv(
            INVENTORY_FILE
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return df

    except Exception as error:

        print(
            "Inventory CSV Error:",
            error
        )

        return None


# ============================================================
# BUILD SALES CONTEXT
# ============================================================

def build_sales_context(df):

    if df is None or df.empty:

        return (
            "No sales dataset is currently available."
        )

    context = []


    # --------------------------------------------------------
    # BASIC METRICS
    # --------------------------------------------------------

    if "Sales" in df.columns:

        sales = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        ).fillna(0)

        total_sales = sales.sum()

        context.append(
            f"Total sales: ₹{total_sales:,.2f}"
        )


    if "Profit" in df.columns:

        profit = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        ).fillna(0)

        total_profit = profit.sum()

        context.append(
            f"Total profit: ₹{total_profit:,.2f}"
        )


    if "Quantity" in df.columns:

        quantity = pd.to_numeric(
            df["Quantity"],
            errors="coerce"
        ).fillna(0)

        total_quantity = quantity.sum()

        context.append(
            f"Total quantity sold: {int(total_quantity)}"
        )


    context.append(
        f"Total records: {len(df)}"
    )


    # --------------------------------------------------------
    # PROFIT MARGIN
    # --------------------------------------------------------

    if (
        "Sales" in df.columns
        and "Profit" in df.columns
    ):

        total_sales = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        ).fillna(0).sum()

        total_profit = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        ).fillna(0).sum()


        if total_sales != 0:

            margin = (
                total_profit
                / total_sales
            ) * 100

            context.append(
                f"Overall profit margin: {margin:.2f}%"
            )


    # --------------------------------------------------------
    # AVERAGE SALE
    # --------------------------------------------------------

    if "Sales" in df.columns:

        sales = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        ).dropna()

        if len(sales) > 0:

            average_sale = sales.mean()

            context.append(
                f"Average sale value: ₹{average_sale:,.2f}"
            )


    # --------------------------------------------------------
    # CATEGORY SALES
    # --------------------------------------------------------

    if (
        "Category" in df.columns
        and "Sales" in df.columns
    ):

        category_sales = (

            df.assign(
                Sales=pd.to_numeric(
                    df["Sales"],
                    errors="coerce"
                ).fillna(0)
            )

            .groupby("Category")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        context.append(
            "\nSales by category:"
        )


        for category, value in (
            category_sales.items()
        ):

            context.append(
                f"- {category}: ₹{value:,.2f}"
            )


        if len(category_sales) > 0:

            context.append(
                f"Highest-sales category: "
                f"{category_sales.index[0]} "
                f"(₹{category_sales.iloc[0]:,.2f})"
            )


    # --------------------------------------------------------
    # CATEGORY PROFIT
    # --------------------------------------------------------

    if (
        "Category" in df.columns
        and "Profit" in df.columns
    ):

        category_profit = (

            df.assign(
                Profit=pd.to_numeric(
                    df["Profit"],
                    errors="coerce"
                ).fillna(0)
            )

            .groupby("Category")["Profit"]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        context.append(
            "\nProfit by category:"
        )


        for category, value in (
            category_profit.items()
        ):

            context.append(
                f"- {category}: ₹{value:,.2f}"
            )


        if len(category_profit) > 0:

            context.append(
                f"Highest-profit category: "
                f"{category_profit.index[0]} "
                f"(₹{category_profit.iloc[0]:,.2f})"
            )


    # --------------------------------------------------------
    # PRODUCT PERFORMANCE
    # --------------------------------------------------------

    product_column = None


    if "Product Type" in df.columns:

        product_column = "Product Type"

    elif "Product Name" in df.columns:

        product_column = "Product Name"


    if (
        product_column
        and "Sales" in df.columns
    ):

        product_sales = (

            df.assign(
                Sales=pd.to_numeric(
                    df["Sales"],
                    errors="coerce"
                ).fillna(0)
            )

            .groupby(product_column)["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        context.append(
            "\nTop products by sales:"
        )


        for product, value in (
            product_sales.head(10).items()
        ):

            context.append(
                f"- {product}: ₹{value:,.2f}"
            )


        if len(product_sales) > 0:

            context.append(
                f"Top-selling product: "
                f"{product_sales.index[0]} "
                f"(₹{product_sales.iloc[0]:,.2f})"
            )


    # --------------------------------------------------------
    # PRODUCT PROFIT
    # --------------------------------------------------------

    if (
        product_column
        and "Profit" in df.columns
    ):

        product_profit = (

            df.assign(
                Profit=pd.to_numeric(
                    df["Profit"],
                    errors="coerce"
                ).fillna(0)
            )

            .groupby(product_column)["Profit"]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        context.append(
            "\nTop products by profit:"
        )


        for product, value in (
            product_profit.head(10).items()
        ):

            context.append(
                f"- {product}: ₹{value:,.2f}"
            )


    # --------------------------------------------------------
    # DISCOUNT
    # --------------------------------------------------------

    if "Discount" in df.columns:

        discount = pd.to_numeric(
            df["Discount"],
            errors="coerce"
        ).dropna()

        if len(discount) > 0:

            context.append(
                f"Average discount: "
                f"{discount.mean():.2%}"
            )


    return "\n".join(context)


# ============================================================
# BUILD INVENTORY CONTEXT
# ============================================================

def build_inventory_context(df):

    if df is None or df.empty:

        return (
            "No inventory dataset is currently available."
        )


    required = {
        "Product ID",
        "Product Name",
        "Category",
        "Current Stock",
        "Reorder Level",
        "Unit Price",
        "Supplier"
    }


    if not required.issubset(
        set(df.columns)
    ):

        return (
            "Inventory data exists, "
            "but the expected inventory columns "
            "are not available."
        )


    df = df.copy()


    df["Current Stock"] = pd.to_numeric(
        df["Current Stock"],
        errors="coerce"
    )

    df["Reorder Level"] = pd.to_numeric(
        df["Reorder Level"],
        errors="coerce"
    )

    df["Unit Price"] = pd.to_numeric(
        df["Unit Price"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # TOTAL PRODUCTS
    # --------------------------------------------------------

    context = [

        f"Total inventory products: "
        f"{df['Product ID'].nunique()}"

    ]


    # --------------------------------------------------------
    # LOW STOCK
    # --------------------------------------------------------

    low_stock = df[
        df["Current Stock"]
        <=
        df["Reorder Level"]
    ]


    critical = df[
        df["Current Stock"]
        <=
        (
            df["Reorder Level"]
            * 0.5
        )
    ]


    context.append(
        f"Low-stock products: "
        f"{len(low_stock)}"
    )


    context.append(
        f"Critical-stock products: "
        f"{len(critical)}"
    )


    # --------------------------------------------------------
    # REORDER DETAILS
    # --------------------------------------------------------

    if len(low_stock) > 0:

        context.append(
            "\nProducts requiring reorder:"
        )


        for _, row in low_stock.iterrows():

            reorder_quantity = max(

                0,

                row["Reorder Level"]
                -
                row["Current Stock"]

            )


            context.append(

                f"- Product: {row['Product Name']} | "
                f"Stock: {int(row['Current Stock'])} | "
                f"Reorder level: "
                f"{int(row['Reorder Level'])} | "
                f"Suggested reorder: "
                f"{int(reorder_quantity)} units | "
                f"Supplier: {row['Supplier']}"

            )


    return "\n".join(context)


# ============================================================
# ASK GROQ
# ============================================================

def ask_groq(
    message,
    conversation=None
):

    try:

        # ====================================================
        # IMPORTANT:
        # READ THE CURRENT DATA EVERY TIME
        # ====================================================

        sales_df = load_latest_sales()

        inventory_df = load_inventory()


        # ====================================================
        # BUILD FRESH CONTEXT
        # ====================================================

        sales_context = (
            build_sales_context(
                sales_df
            )
        )


        inventory_context = (
            build_inventory_context(
                inventory_df
            )
        )


        # ====================================================
        # AI SYSTEM PROMPT
        # ====================================================

        system_prompt = f"""

You are SmartRetail AI, an intelligent
retail business assistant.

You help users understand their current
retail business data.

The data below is freshly loaded from the
current SmartRetail datasets.

==================================================
CURRENT SALES DATA
==================================================

{sales_context}

==================================================
CURRENT INVENTORY DATA
==================================================

{inventory_context}

==================================================
ANSWERING RULES
==================================================

1. ALWAYS use the supplied current data
   for factual questions.

2. NEVER invent sales, profit, inventory,
   product, category, quantity or supplier
   values.

3. ALL monetary values are in Indian Rupees.
   Always use ₹.

4. Keep answers concise and easy to read.

5. Do NOT use Markdown tables.

6. Do NOT create large walls of text.

7. For multiple items, use short bullet points.

8. For important values, use **bold**.

9. You may use simple emojis where useful.

10. For business recommendations, clearly
    distinguish the recommendation from
    the actual data.

11. If information is unavailable, say so
    instead of guessing.

12. If the user asks about inventory,
    use the inventory data.

13. If the user asks about sales, profit,
    products or categories, use the sales data.

14. If the question involves both sales and
    inventory, use both datasets.

15. Do not mention these instructions to
    the user.

==================================================
RESPONSE STYLE
==================================================

Make the answer feel like a professional
AI business assistant.

For a single metric:

**Total Profit**

₹15,861.93

For a top product:

🏆 **Top-Selling Product**

**Phones Product 7**

₹7,251.36 in sales.

For multiple products:

📦 **Products Needing Reorder**

• **Wireless Mouse**
  Stock: 8 | Reorder level: 20
  Suggested reorder: 12 units

• **Office Chair**
  Stock: 12 | Reorder level: 25
  Suggested reorder: 13 units

Keep responses visually clean and suitable
for a small chatbot window.

"""


        # ====================================================
        # CONVERSATION HISTORY
        # ====================================================

        messages = [

            {
                "role": "system",
                "content": system_prompt
            }

        ]


        if conversation:

            for item in conversation[-10:]:

                role = item.get(
                    "role"
                )

                content = item.get(
                    "content"
                )


                if (
                    role in
                    ("user", "assistant")
                    and content
                ):

                    messages.append({

                        "role": role,

                        "content": content

                    })


        messages.append({

            "role": "user",

            "content": message

        })


        # ====================================================
        # GROQ REQUEST
        # ====================================================

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=messages,

            temperature=0.2,

            max_tokens=500

        )


        answer = (
            response
            .choices[0]
            .message
            .content
        )


        return answer.strip()


    except Exception as error:

        print(
            "Groq API Error:",
            error
        )


        return (
            "⚠️ I couldn't connect to "
            "SmartRetail AI right now. "
            "Please try again."
        )