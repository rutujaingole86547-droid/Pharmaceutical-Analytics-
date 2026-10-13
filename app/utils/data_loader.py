"""
Centralized data loading module.

All application modules use this file for loading datasets.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from config import (
    SALES_FILE,
    INVENTORY_FILE,
    PRODUCTS_FILE,
    FORECAST_FILE,
    RECOMMENDATION_FILE,
    MANAGEMENT_SUMMARY_FILE,
    RECOMMENDATION_SUMMARY_FILE,
    HIGH_PRIORITY_FILE,
    MODEL_COMPARISON_FILE,
)

from utils.helpers import clean_column_names


# ============================================================
# GENERIC CSV LOADER
# ============================================================

@st.cache_data(show_spinner=False)
def _load_csv(file_path):
    """Load and standardize a CSV file."""

    file_path = Path(file_path)

    if not file_path.exists():
        return pd.DataFrame()

    try:

        df = pd.read_csv(file_path)

        return clean_column_names(df)

    except Exception:
        return pd.DataFrame()


# ============================================================
# SALES
# ============================================================

def load_sales_data():
    return _load_csv(SALES_FILE)


# ============================================================
# INVENTORY
# ============================================================

def load_inventory_data():
    return _load_csv(INVENTORY_FILE)


# ============================================================
# PRODUCTS
# ============================================================

def load_products_data():
    return _load_csv(PRODUCTS_FILE)


# ============================================================
# FORECAST
# ============================================================

def load_forecast_data():
    return _load_csv(FORECAST_FILE)


# ============================================================
# RECOMMENDATIONS
# ============================================================

def load_recommendation_data():
    return _load_csv(RECOMMENDATION_FILE)


# ============================================================
# MANAGEMENT SUMMARY
# ============================================================

def load_management_summary():
    return _load_csv(MANAGEMENT_SUMMARY_FILE)


# ============================================================
# RECOMMENDATION SUMMARY
# ============================================================

def load_recommendation_summary():
    return _load_csv(RECOMMENDATION_SUMMARY_FILE)


# ============================================================
# HIGH PRIORITY ACTIONS
# ============================================================

def load_high_priority_actions():
    return _load_csv(HIGH_PRIORITY_FILE)


# ============================================================
# MODEL COMPARISON
# ============================================================

def load_model_comparison():
    return _load_csv(MODEL_COMPARISON_FILE)