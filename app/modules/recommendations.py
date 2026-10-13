"""
AI Inventory Recommendations module.

Displays AI-generated inventory recommendations,
priority levels, reorder quantities and estimated costs.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from components.ui import (
    render_header,
    render_kpi,
    render_section_title,
)

from utils.data_loader import (
    load_recommendation_data,
)

from utils.helpers import (
    format_currency,
    format_number,
)


# ============================================================
# CHART STYLE
# ============================================================

def style_chart(fig):

    fig.update_layout(
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20,
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


# ============================================================
# MAIN PAGE
# ============================================================

def show_recommendations():

    render_header(
        "AI Inventory Recommendations",
        "AI-assisted inventory risk detection and reorder decision intelligence",
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    df = load_recommendation_data()

    if df.empty:

        st.error(
            "AI recommendation data is not available."
        )

        st.info(
            "Please generate "
            "ai_inventory_recommendations.csv "
            "before using this module."
        )

        return

    # ========================================================
    # NUMERIC COLUMNS
    # ========================================================

    numeric_columns = [
        "current_stock",
        "forecast_2026_demand",
        "forecast_reorder_quantity",
        "forecast_reorder_cost",
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            ).fillna(0)

    # ========================================================
    # FILTERS
    # ========================================================

    st.sidebar.markdown(
        "### Recommendation Filters"
    )

    filtered_df = df.copy()

    if "forecast_priority" in df.columns:

        priorities = sorted(
            df[
                "forecast_priority"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_priority = st.sidebar.selectbox(
            "Priority",
            ["All"] + priorities,
        )

        if selected_priority != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "forecast_priority"
                ].astype(str)
                == selected_priority
            ]

    if "inventory_status" in df.columns:

        statuses = sorted(
            df[
                "inventory_status"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_status = st.sidebar.selectbox(
            "Inventory Status",
            ["All"] + statuses,
        )

        if selected_status != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "inventory_status"
                ].astype(str)
                == selected_status
            ]

    if "category" in df.columns:

        categories = sorted(
            df[
                "category"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_category = st.sidebar.selectbox(
            "Category",
            ["All"] + categories,
        )

        if selected_category != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "category"
                ].astype(str)
                == selected_category
            ]

    # ========================================================
    # KPI
    # ========================================================

    total_records = len(filtered_df)

    high_priority = 0

    if "forecast_priority" in filtered_df.columns:

        high_priority = int(
            filtered_df[
                "forecast_priority"
            ]
            .astype(str)
            .str.lower()
            .str.contains(
                "high|critical|urgent",
                regex=True,
            )
            .sum()
        )

    total_reorder = (
        filtered_df[
            "forecast_reorder_quantity"
        ].sum()
        if "forecast_reorder_quantity"
        in filtered_df.columns
        else 0
    )

    total_cost = (
        filtered_df[
            "forecast_reorder_cost"
        ].sum()
        if "forecast_reorder_cost"
        in filtered_df.columns
        else 0
    )

    render_section_title(
        "Inventory Decision Overview"
    )

    cols = st.columns(4)

    with cols[0]:

        render_kpi(
            "Medicines Analyzed",
            format_number(total_records),
            "Current filtered records",
        )

    with cols[1]:

        render_kpi(
            "High Priority",
            format_number(high_priority),
            "Urgent inventory actions",
        )

    with cols[2]:

        render_kpi(
            "Reorder Quantity",
            format_number(total_reorder),
            "Units recommended",
        )

    with cols[3]:

        render_kpi(
            "Estimated Reorder Cost",
            format_currency(total_cost),
            "Estimated procurement cost",
        )

    # ========================================================
    # ALERT
    # ========================================================

    if high_priority > 0:

        st.warning(
            f"⚠️ {high_priority:,} medicine(s) "
            "require high-priority inventory attention."
        )

    else:

        st.success(
            "✓ No high-priority inventory actions "
            "were identified in the current filter."
        )

    # ========================================================
    # PRIORITY + INVENTORY STATUS
    # ========================================================

    left, right = st.columns(2)

    with left:

        render_section_title(
            "Priority Distribution"
        )

        if "forecast_priority" in filtered_df.columns:

            priority_data = (
                filtered_df[
                    "forecast_priority"
                ]
                .value_counts()
                .reset_index()
            )

            priority_data.columns = [
                "priority",
                "count",
            ]

            fig = px.bar(
                priority_data,
                x="priority",
                y="count",
                title="Inventory Priority Levels",
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    with right:

        render_section_title(
            "Inventory Status"
        )

        if "inventory_status" in filtered_df.columns:

            status_data = (
                filtered_df[
                    "inventory_status"
                ]
                .value_counts()
                .reset_index()
            )

            status_data.columns = [
                "status",
                "count",
            ]

            fig = px.pie(
                status_data,
                names="status",
                values="count",
                hole=0.55,
                title="Inventory Status Distribution",
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    # ========================================================
    # COST BY CATEGORY
    # ========================================================

    if (
        "category" in filtered_df.columns
        and "forecast_reorder_cost"
        in filtered_df.columns
    ):

        render_section_title(
            "Estimated Reorder Cost by Category"
        )

        category_cost = (
            filtered_df
            .groupby(
                "category",
                as_index=False
            )["forecast_reorder_cost"]
            .sum()
            .sort_values(
                "forecast_reorder_cost",
                ascending=False,
            )
        )

        if not category_cost.empty:

            fig = px.bar(
                category_cost,
                x="category",
                y="forecast_reorder_cost",
                title="Reorder Cost by Category",
            )

            fig.update_yaxes(
                tickprefix="₹"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    # ========================================================
    # HIGH PRIORITY ACTIONS
    # ========================================================

    render_section_title(
        "High-Priority Inventory Actions"
    )

    action_columns = [
        "product_id",
        "medicine_name",
        "category",
        "city",
        "current_stock",
        "forecast_2026_demand",
        "forecast_reorder_quantity",
        "forecast_reorder_cost",
        "forecast_recommendation",
        "forecast_priority",
    ]

    available_columns = [
        column
        for column in action_columns
        if column in filtered_df.columns
    ]

    high_priority_df = filtered_df.copy()

    if "forecast_priority" in high_priority_df.columns:

        high_priority_df = high_priority_df[
            high_priority_df[
                "forecast_priority"
            ]
            .astype(str)
            .str.lower()
            .str.contains(
                "high|critical|urgent",
                regex=True,
            )
        ]

    if high_priority_df.empty:

        st.info(
            "No high-priority actions found "
            "for the current filters."
        )

    else:

        st.dataframe(
            high_priority_df[
                available_columns
            ].head(100),
            use_container_width=True,
            hide_index=True,
        )

    # ========================================================
    # RECOMMENDATION DISTRIBUTION
    # ========================================================

    render_section_title(
        "AI Recommendation Summary"
    )

    if (
        "forecast_recommendation"
        in filtered_df.columns
    ):

        recommendation_counts = (
            filtered_df[
                "forecast_recommendation"
            ]
            .value_counts()
            .reset_index()
        )

        recommendation_counts.columns = [
            "recommendation",
            "count",
        ]

        fig = px.bar(
            recommendation_counts,
            x="count",
            y="recommendation",
            orientation="h",
            title="Recommended Inventory Actions",
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

    # ========================================================
    # FULL RECORDS
    # ========================================================

    render_section_title(
        "Detailed Recommendation Records"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

    # ========================================================
    # DOWNLOAD
    # ========================================================

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Recommendations",
        data=csv_data,
        file_name=(
            "filtered_ai_inventory_recommendations.csv"
        ),
        mime="text/csv",
    )