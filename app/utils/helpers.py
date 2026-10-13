"""
Reusable helper functions for the Pharma Inventory Analytics Platform.
"""

import re

import pandas as pd


# ============================================================
# NUMBER FORMATTING
# ============================================================

def format_number(value):
    """Format a numeric value using K, M and B notation."""

    if value is None or pd.isna(value):
        return "0"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "0"

    absolute_value = abs(value)

    if absolute_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    if absolute_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if absolute_value >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


# ============================================================
# CURRENCY FORMATTING
# ============================================================

def format_currency(value):
    """Format values as Indian Rupees."""

    if value is None or pd.isna(value):
        return "₹0"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "₹0"

    absolute_value = abs(value)

    if absolute_value >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"

    if absolute_value >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"

    if absolute_value >= 1_000:
        return f"₹{value / 1_000:.1f}K"

    return f"₹{value:,.0f}"


# ============================================================
# PERCENTAGE
# ============================================================

def calculate_percentage(part, total):
    """Calculate percentage safely."""

    try:
        if total == 0:
            return 0.0

        return (float(part) / float(total)) * 100

    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


# ============================================================
# STATUS CLASS
# ============================================================

def get_status_class(status):
    """Return CSS status class based on inventory status."""

    if status is None or pd.isna(status):
        return "normal"

    status = str(status).strip().lower()

    if "stockout" in status or "critical" in status:
        return "critical"

    if "low" in status or "reorder" in status:
        return "warning"

    if "overstock" in status:
        return "info"

    if "healthy" in status or "sufficient" in status:
        return "success"

    return "normal"


# ============================================================
# COLUMN CLEANING
# ============================================================

def clean_column_names(df):
    """
    Standardize DataFrame column names.

    Example:
        Order Date -> order_date
        Medicine Name -> medicine_name
    """

    df = df.copy()

    cleaned_columns = []

    for column in df.columns:

        column = str(column).strip().lower()

        column = re.sub(
            r"[^a-z0-9]+",
            "_",
            column
        )

        column = re.sub(
            r"_+",
            "_",
            column
        )

        column = column.strip("_")

        cleaned_columns.append(column)

    df.columns = cleaned_columns

    return df


# ============================================================
# NUMERIC CONVERSION
# ============================================================

def to_numeric(series, default=0):
    """Safely convert a pandas Series to numeric."""

    return (
        pd.to_numeric(
            series,
            errors="coerce"
        )
        .fillna(default)
    )


# ============================================================
# COLUMN FINDER
# ============================================================

def find_column(df, possible_columns):
    """Return the first matching column."""

    if df is None or df.empty:
        return None

    for column in possible_columns:

        if column in df.columns:
            return column

    return None