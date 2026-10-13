"""
Configuration module for the Pharma Inventory Analytics Platform.

Contains all project paths used by the application.
"""

from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# MAIN DIRECTORIES
# ============================================================

DATA_DIR = BASE_DIR / "Data"

CLEANED_DATA_DIR = DATA_DIR / "Cleaned"

ML_OUTPUT_DIR = DATA_DIR / "ML Outputs"

MODELS_DIR = BASE_DIR / "Models"


# ============================================================
# CLEANED DATASETS
# ============================================================

SALES_FILE = CLEANED_DATA_DIR / "sales_transactions_clean.csv"

INVENTORY_FILE = CLEANED_DATA_DIR / "inventory_clean.csv"

PRODUCTS_FILE = CLEANED_DATA_DIR / "products_clean.csv"

SUPPLIERS_FILE = CLEANED_DATA_DIR / "suppliers_clean.csv"

CUSTOMERS_FILE = CLEANED_DATA_DIR / "customers_clean.csv"


# ============================================================
# ML OUTPUT FILES
# ============================================================

FORECAST_FILE = (
    ML_OUTPUT_DIR / "medicine_demand_forecast_2026.csv"
)

RECOMMENDATION_FILE = (
    ML_OUTPUT_DIR / "ai_inventory_recommendations.csv"
)

MANAGEMENT_SUMMARY_FILE = (
    ML_OUTPUT_DIR / "ai_management_summary.csv"
)

RECOMMENDATION_SUMMARY_FILE = (
    ML_OUTPUT_DIR / "ai_recommendation_summary.csv"
)

HIGH_PRIORITY_FILE = (
    ML_OUTPUT_DIR / "high_priority_inventory_actions.csv"
)

MODEL_COMPARISON_FILE = (
    ML_OUTPUT_DIR / "forecast_model_comparison.csv"
)


# ============================================================
# TRAINED MODEL
# ============================================================

FORECAST_MODEL = (
    MODELS_DIR / "gradient_boosting_demand_model.pkl"
)