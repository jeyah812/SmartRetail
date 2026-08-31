import os

import pandas as pd


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

INVENTORY_DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw",
    "inventory.csv"
)

REQUIRED_COLUMNS = [
    "Product ID",
    "Product Name",
    "Category",
    "Current Stock",
    "Reorder Level",
    "Unit Price",
    "Supplier",
    "Last Updated"
]


def load_inventory_data():

    inventory = pd.read_csv(
        INVENTORY_DATA_PATH
    )

    inventory.columns = (
        inventory.columns
        .astype(str)
        .str.strip()
    )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in inventory.columns
    ]

    if missing_columns:

        raise ValueError(
            "Inventory data is missing required columns: "
            + ", ".join(missing_columns)
        )

    for column in (
        "Current Stock",
        "Reorder Level",
        "Unit Price"
    ):

        inventory[column] = pd.to_numeric(
            inventory[column],
            errors="coerce"
        )

    return inventory


def get_inventory_stats():

    inventory = load_inventory_data()

    stock = inventory["Current Stock"]
    reorder_level = inventory["Reorder Level"]

    low_stock_items = (
        stock <= reorder_level
    ).fillna(False).sum()

    critical_alerts = (
        stock <= (reorder_level * 0.5)
    ).fillna(False).sum()

    return {
        "total_products": int(
            inventory["Product ID"].nunique()
        ),
        "low_stock_items": int(
            low_stock_items
        ),
        "critical_alerts": int(
            critical_alerts
        ),
        "total_categories": int(
            inventory["Category"]
            .dropna()
            .nunique()
        )
    }


def get_reorder_alerts():

    inventory = load_inventory_data()

    stock = inventory["Current Stock"]
    reorder_level = inventory["Reorder Level"]

    alerts = inventory[
        (
            stock <= reorder_level
        )
        &
        stock.notna()
        &
        reorder_level.notna()
    ].copy()

    alerts["Status"] = "Low Stock"

    critical_mask = (
        alerts["Current Stock"]
        <=
        (
            alerts["Reorder Level"]
            * 0.5
        )
    )

    alerts.loc[
        critical_mask,
        "Status"
    ] = "Critical"

    alerts["Suggested Reorder"] = (
        alerts["Reorder Level"]
        -
        alerts["Current Stock"]
    ).clip(
        lower=0
    )

    return alerts.to_dict(
        orient="records"
    )


def get_product_movement(sales_file_path):

    if not sales_file_path:
        return {
            "fast_moving_products": 0,
            "slow_moving_products": 0
        }

    if not os.path.exists(sales_file_path):
        return {
            "fast_moving_products": 0,
            "slow_moving_products": 0
        }

    sales = pd.read_csv(
        sales_file_path
    )

    sales.columns = (
        sales.columns
        .astype(str)
        .str.strip()
    )

    required_sales_columns = [
        "Product Type",
        "Quantity"
    ]

    missing_columns = [
        column
        for column in required_sales_columns
        if column not in sales.columns
    ]

    if missing_columns:
        return {
            "fast_moving_products": 0,
            "slow_moving_products": 0
        }

    sales["Quantity"] = pd.to_numeric(
        sales["Quantity"],
        errors="coerce"
    )

    sales = sales.dropna(
        subset=[
            "Product Type",
            "Quantity"
        ]
    )

    if sales.empty:
        return {
            "fast_moving_products": 0,
            "slow_moving_products": 0
        }

    product_sales = (
        sales
        .groupby("Product Type")["Quantity"]
        .sum()
    )

    if product_sales.empty:
        return {
            "fast_moving_products": 0,
            "slow_moving_products": 0
        }

    median_quantity = product_sales.median()

    fast_moving_products = int(
        (
            product_sales
            >= median_quantity
        ).sum()
    )

    slow_moving_products = int(
        (
            product_sales
            < median_quantity
        ).sum()
    )

    return {
        "fast_moving_products": fast_moving_products,
        "slow_moving_products": slow_moving_products
    }


def get_inventory_chart_data():

    inventory = load_inventory_data()

    stock = inventory["Current Stock"]
    reorder_level = inventory["Reorder Level"]

    valid_inventory = inventory[
        stock.notna()
        &
        reorder_level.notna()
    ].copy()

    stock_values = valid_inventory["Current Stock"]
    reorder_values = valid_inventory["Reorder Level"]

    critical_mask = (
        stock_values
        <=
        (
            reorder_values * 0.5
        )
    )

    low_stock_mask = (
        stock_values <= reorder_values
    ) & ~critical_mask

    healthy_mask = (
        stock_values > reorder_values
    )

    critical_count = int(
        critical_mask.sum()
    )

    low_stock_count = int(
        low_stock_mask.sum()
    )

    healthy_count = int(
        healthy_mask.sum()
    )

    category_counts = (
        inventory["Category"]
        .dropna()
        .value_counts()
    )

    return {
        "status_labels": [
            "Healthy",
            "Low Stock",
            "Critical"
        ],
        "status_values": [
            healthy_count,
            low_stock_count,
            critical_count
        ],
        "category_labels": [
            str(category)
            for category in category_counts.index
        ],
        "category_values": [
            int(value)
            for value in category_counts.values
        ]
    }