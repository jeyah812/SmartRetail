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
        )
    }
