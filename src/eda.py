import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from feature_engineering import add_features
df = pd.read_csv(
    "data/raw/Sample - Superstore.csv",
    encoding="latin1"
)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Add new features
df = add_features(df)
sales_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

sales_category.plot(
    kind="bar",
    color=["steelblue","orange","green"]
)

plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.tight_layout()
import os

os.makedirs("outputs/charts", exist_ok=True)

plt.savefig("outputs/charts/sales_by_category.png", dpi=300, bbox_inches="tight")
plt.show()
# -----------------------------
# Profit by Category
# -----------------------------

profit_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

profit_category.plot(
    kind="bar",
    color=["green", "royalblue", "tomato"]
)

plt.title("Total Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")

plt.tight_layout()

plt.savefig("outputs/charts/profit_by_category.png",
            dpi=300,
            bbox_inches="tight")

plt.show()
# -----------------------------
# Sales by Region
# -----------------------------

sales_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

sales_region.plot(
    kind="bar",
    color="steelblue"
)

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig("outputs/charts/sales_by_region.png",
            dpi=300,
            bbox_inches="tight")

plt.show()
# -----------------------------
# Profit by Region
# -----------------------------

profit_region = (
    df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

profit_region.plot(
    kind="bar",
    color="darkgreen"
)

plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")

plt.tight_layout()

plt.savefig("outputs/charts/profit_by_region.png",
            dpi=300,
            bbox_inches="tight")

plt.show()
# -----------------------------
# Monthly Sales Trend
# -----------------------------

monthly_sales = (
    df.groupby("Order Month")["Sales"]
    .sum()
    .reindex([
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ])
)

plt.figure(figsize=(10,5))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=2
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Monthly Profit Trend
# -----------------------------

monthly_profit = (
    df.groupby("Order Month")["Profit"]
    .sum()
    .reindex([
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ])
)

plt.figure(figsize=(10,5))

plt.plot(
    monthly_profit.index,
    monthly_profit.values,
    marker="o",
    linewidth=2
)

plt.title("Monthly Profit Trend")
plt.xlabel("Month")
plt.ylabel("Total Profit")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_profit_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Sales by Segment
# -----------------------------

sales_segment = (
    df.groupby("Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

sales_segment.plot(
    kind="bar",
    color="purple"
)

plt.title("Sales by Segment")
plt.xlabel("Segment")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "outputs/charts/sales_by_segment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Top 10 Products by Sales
# -----------------------------

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

top_products.plot(
    kind="barh",
    color="teal"
)

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top10_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Top 10 Customers by Sales
# -----------------------------

top_customers = (
    df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

top_customers.plot(
    kind="barh",
    color="orange"
)

plt.title("Top 10 Customers by Sales")
plt.xlabel("Sales")
plt.ylabel("Customer")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top10_customers.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Discount vs Profit
# -----------------------------

plt.figure(figsize=(8,5))

plt.scatter(
    df["Discount"],
    df["Profit"],
    alpha=0.5
)

plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "outputs/charts/discount_vs_profit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Correlation Heatmap
# -----------------------------

numeric_df = df.select_dtypes(include=["number"])

plt.figure(figsize=(10,8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "outputs/charts/correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Shipping Days Distribution
# -----------------------------

plt.figure(figsize=(8,5))

plt.hist(
    df["Shipping Days"],
    bins=10
)

plt.title("Shipping Days Distribution")
plt.xlabel("Shipping Days")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "outputs/charts/shipping_days_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Sales Distribution
# -----------------------------

plt.figure(figsize=(8,5))

plt.hist(
    df["Sales"],
    bins=30
)

plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "outputs/charts/sales_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Profit Distribution
# -----------------------------

plt.figure(figsize=(8,5))

plt.hist(
    df["Profit"],
    bins=30
)

plt.title("Profit Distribution")
plt.xlabel("Profit")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "outputs/charts/profit_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Top 10 States by Sales
# -----------------------------

top_states = (
    df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))

top_states.plot(
    kind="bar",
    color="dodgerblue"
)

plt.title("Top 10 States by Sales")
plt.xlabel("State")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_states_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# -----------------------------
# Top 10 Sub-Categories by Profit
# -----------------------------

top_sub = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))

top_sub.plot(
    kind="barh",
    color="green"
)

plt.title("Top 10 Sub-Categories by Profit")
plt.xlabel("Profit")
plt.ylabel("Sub-Category")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_subcategory_profit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()