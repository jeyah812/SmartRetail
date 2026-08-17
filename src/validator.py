import pandas as pd

# ==========================
# Required Columns
# ==========================

REQUIRED_COLUMNS = [
    "Sales",
    "Profit",
    "Quantity",
    "Discount",
    "Category"
]

# ==========================
# Optional Columns
# ==========================

OPTIONAL_COLUMNS = [
    "Sub-Category",
    "Region",
    "Segment",
    "Order Date",
    "Ship Date"
]


def validate_dataset(file_path):

    df = pd.read_csv(file_path, encoding="latin1")

    # Remove accidental spaces in column names
    df.columns = df.columns.str.strip()

    missing_required = []
    missing_optional = []

    # Check required columns
    for column in REQUIRED_COLUMNS:

        if column not in df.columns:

            missing_required.append(column)

    # Check optional columns
    for column in OPTIONAL_COLUMNS:

        if column not in df.columns:

            missing_optional.append(column)

    # Stop only if required columns are missing
    if missing_required:

        return False, missing_required, missing_optional

    # Dataset is valid
    return True, df, missing_optional