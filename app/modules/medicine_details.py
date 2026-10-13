"""
Medicine Details module.

Allows users to search individual medicines and view
product, inventory, forecast and AI recommendation information.
"""

import html

import pandas as pd
import streamlit as st

from components.ui import (
    render_header,
    render_kpi,
    render_section_title,
)

from utils.data_loader import (
    load_inventory_data,
    load_products_data,
    load_recommendation_data,
)

from utils.helpers import (
    format_currency,
    format_number,
)


# ============================================================
# MAIN PAGE
# ============================================================

def show_medicine_details():

    render_header(
        "Medicine Details",
        "Search medicines and understand their product, inventory and AI insights",
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    products = load_products_data()

    inventory = load_inventory_data()

    recommendations = load_recommendation_data()

    if products.empty:

        st.error(
            "Product data could not be loaded."
        )

        return

    # ========================================================
    # MEDICINE COLUMN
    # ========================================================

    if "medicine_name" not in products.columns:

        st.error(
            "The products dataset does not contain "
            "'medicine_name'."
        )

        st.write(
            "Available columns:",
            list(products.columns),
        )

        return

    # ========================================================
    # MEDICINE LIST
    # ========================================================

    medicine_list = sorted(
        products[
            "medicine_name"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if not medicine_list:

        st.warning(
            "No medicines are available."
        )

        return

    # ========================================================
    # SEARCH
    # ========================================================

    st.sidebar.markdown(
        "### Medicine Search"
    )

    search_text = st.sidebar.text_input(
        "Search medicine",
        placeholder="Type medicine name...",
    ).strip().lower()

    filtered_medicines = medicine_list

    if search_text:

        filtered_medicines = [
            medicine
            for medicine in medicine_list
            if search_text in medicine.lower()
        ]

    if not filtered_medicines:

        st.warning(
            "No medicine matched your search."
        )

        return

    selected_medicine = st.selectbox(
        "💊 Select Medicine",
        filtered_medicines,
    )

    # ========================================================
    # PRODUCT INFORMATION
    # ========================================================

    product_rows = products[
        products[
            "medicine_name"
        ].astype(str)
        == selected_medicine
    ]

    if product_rows.empty:

        st.warning(
            "Product information is not available."
        )

        return

    product = product_rows.iloc[0]

    render_section_title(
        "Product Information"
    )

    cols = st.columns(4)

    with cols[0]:

        render_kpi(
            "Product ID",
            str(
                product.get(
                    "product_id",
                    "N/A",
                )
            ),
            "Product identifier",
        )

    with cols[1]:

        render_kpi(
            "Category",
            str(
                product.get(
                    "category",
                    "N/A",
                )
            ),
            "Product category",
        )

    with cols[2]:

        render_kpi(
            "Manufacturer",
            str(
                product.get(
                    "manufacturer",
                    "N/A",
                )
            ),
            "Manufacturer",
        )

    with cols[3]:

        price = numeric_value(
            product.get(
                "selling_price",
                0,
            )
        )

        render_kpi(
            "Selling Price",
            format_currency(price),
            "Current selling price",
        )

    # ========================================================
    # INVENTORY + FORECAST
    # ========================================================

    render_section_title(
        "Inventory & Forecast Intelligence"
    )

    recommendation_row = pd.DataFrame()

    if not recommendations.empty:

        if "medicine_name" in recommendations.columns:

            recommendation_row = recommendations[
                recommendations[
                    "medicine_name"
                ].astype(str)
                == selected_medicine
            ]

    if not recommendation_row.empty:

        row = recommendation_row.iloc[0]

        current_stock = numeric_value(
            row.get(
                "current_stock",
                0,
            )
        )

        forecast_demand = numeric_value(
            row.get(
                "forecast_2026_demand",
                0,
            )
        )

        reorder_quantity = numeric_value(
            row.get(
                "forecast_reorder_quantity",
                0,
            )
        )

        reorder_cost = numeric_value(
            row.get(
                "forecast_reorder_cost",
                0,
            )
        )

        priority = row.get(
            "forecast_priority",
            "N/A",
        )

        recommendation = row.get(
            "forecast_recommendation",
            "N/A",
        )

        cols = st.columns(4)

        with cols[0]:

            render_kpi(
                "Current Stock",
                format_number(
                    current_stock
                ),
                "Available inventory",
            )

        with cols[1]:

            render_kpi(
                "Forecast Demand",
                format_number(
                    forecast_demand
                ),
                "Expected 2026 demand",
            )

        with cols[2]:

            render_kpi(
                "Reorder Quantity",
                format_number(
                    reorder_quantity
                ),
                "AI suggested reorder",
            )

        with cols[3]:

            render_kpi(
                "Reorder Cost",
                format_currency(
                    reorder_cost
                ),
                "Estimated procurement cost",
            )

        # ----------------------------------------------------
        # AI RECOMMENDATION
        # ----------------------------------------------------

        safe_recommendation = html.escape(
            str(recommendation)
        )

        safe_priority = html.escape(
            str(priority)
        )

        st.markdown(
            f"""
            <div class="info-panel">

                <b>🤖 AI Inventory Recommendation</b>

                <br><br>

                {safe_recommendation}

                <br><br>

                <b>Priority:</b>
                {safe_priority}

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "AI recommendation data is not available "
            "for this medicine."
        )

    # ========================================================
    # INVENTORY RECORD
    # ========================================================

    if not inventory.empty:

        inventory_row = pd.DataFrame()

        if "medicine_name" in inventory.columns:

            inventory_row = inventory[
                inventory[
                    "medicine_name"
                ].astype(str)
                == selected_medicine
            ]

        elif "product_id" in inventory.columns:

            product_id = product.get(
                "product_id"
            )

            if product_id is not None:

                inventory_row = inventory[
                    inventory[
                        "product_id"
                    ].astype(str)
                    == str(product_id)
                ]

        if not inventory_row.empty:

            render_section_title(
                "Inventory Record"
            )

            st.dataframe(
                inventory_row,
                use_container_width=True,
                hide_index=True,
            )

    # ========================================================
    # PRODUCT RECORD
    # ========================================================

    render_section_title(
        "Product Record"
    )

    st.dataframe(
        product_rows,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# HELPER
# ============================================================

def numeric_value(value):

    try:

        value = pd.to_numeric(
            value,
            errors="coerce",
        )

        if pd.isna(value):
            return 0.0

        return float(value)

    except Exception:

        return 0.0