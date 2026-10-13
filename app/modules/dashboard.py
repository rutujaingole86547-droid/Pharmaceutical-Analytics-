"""
Analytics Dashboard.

Provides an executive overview of pharmaceutical sales,
profitability and inventory performance.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.ui import (
    render_header,
    render_kpi,
    render_section_title,
)

from utils.data_loader import (
    load_inventory_data,
    load_products_data,
    load_sales_data,
)

from utils.helpers import (
    calculate_percentage,
    format_currency,
    format_number,
)


# ============================================================
# CHART STYLING
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
        font=dict(
            family="Arial",
            size=12,
        ),
    )

    return fig


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_dashboard():

    render_header(
        "Pharmaceutical Analytics Dashboard",
        "Executive overview of sales, profitability and inventory performance",
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    sales = load_sales_data()

    inventory = load_inventory_data()

    products = load_products_data()

    if sales.empty:

        st.error(
            "Sales data could not be loaded."
        )

        st.info(
            "Please verify the cleaned sales dataset."
        )

        return

    # ========================================================
    # DATE CONVERSION
    # ========================================================

    if "order_date" in sales.columns:

        sales["order_date"] = pd.to_datetime(
            sales["order_date"],
            errors="coerce",
        )

    # ========================================================
    # MERGE PRODUCT INFORMATION
    # ========================================================

    if (
        not products.empty
        and "product_id" in sales.columns
        and "product_id" in products.columns
    ):

        product_columns = ["product_id"]

        for column in [
            "medicine_name",
            "category",
            "manufacturer",
        ]:

            if column in products.columns:
                product_columns.append(column)

        product_info = (
            products[product_columns]
            .drop_duplicates(
                subset=["product_id"]
            )
        )

        sales = sales.merge(
            product_info,
            on="product_id",
            how="left",
        )

    # ========================================================
    # SIDEBAR FILTERS
    # ========================================================

    st.sidebar.markdown(
        "### Dashboard Filters"
    )

    filtered_sales = sales.copy()

    filtered_inventory = inventory.copy()

    # --------------------------------------------------------
    # YEAR
    # --------------------------------------------------------

    if "order_date" in filtered_sales.columns:

        years = sorted(
            filtered_sales[
                "order_date"
            ]
            .dropna()
            .dt.year
            .unique()
            .tolist()
        )

        if years:

            selected_year = st.sidebar.selectbox(
                "Year",
                ["All"] + years,
            )

            if selected_year != "All":

                filtered_sales = filtered_sales[
                    filtered_sales[
                        "order_date"
                    ].dt.year
                    == selected_year
                ]

    # --------------------------------------------------------
    # CITY
    # --------------------------------------------------------

    if "city" in filtered_sales.columns:

        cities = sorted(
            filtered_sales[
                "city"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_city = st.sidebar.selectbox(
            "City",
            ["All"] + cities,
        )

        if selected_city != "All":

            filtered_sales = filtered_sales[
                filtered_sales["city"]
                .astype(str)
                == selected_city
            ]

            if "city" in filtered_inventory.columns:

                filtered_inventory = filtered_inventory[
                    filtered_inventory["city"]
                    .astype(str)
                    == selected_city
                ]

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    if "category" in filtered_sales.columns:

        categories = sorted(
            filtered_sales[
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

            filtered_sales = filtered_sales[
                filtered_sales["category"]
                .astype(str)
                == selected_category
            ]

    # --------------------------------------------------------
    # INVENTORY STATUS
    # --------------------------------------------------------

    if "inventory_status" in filtered_inventory.columns:

        statuses = sorted(
            filtered_inventory[
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

            filtered_inventory = filtered_inventory[
                filtered_inventory[
                    "inventory_status"
                ].astype(str)
                == selected_status
            ]

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    revenue = numeric_sum(
        filtered_sales,
        "revenue",
    )

    profit = numeric_sum(
        filtered_sales,
        "profit",
    )

    quantity = numeric_sum(
        filtered_sales,
        "quantity",
    )

    orders = unique_count(
        filtered_sales,
        "order_id",
    )

    customers = unique_count(
        filtered_sales,
        "customer_id",
    )

    current_stock = numeric_sum(
        filtered_inventory,
        "current_stock",
    )

    profit_margin = calculate_percentage(
        profit,
        revenue,
    )

    average_order_value = (
        revenue / orders
        if orders > 0
        else 0
    )

    stockout_count = 0

    if "inventory_status" in filtered_inventory.columns:

        stockout_count = int(
            filtered_inventory[
                "inventory_status"
            ]
            .astype(str)
            .str.lower()
            .str.contains("stockout")
            .sum()
        )

    # ========================================================
    # BUSINESS KPIs
    # ========================================================

    render_section_title(
        "Business Performance"
    )

    cols = st.columns(4)

    with cols[0]:

        render_kpi(
            "Total Revenue",
            format_currency(revenue),
            "Filtered sales revenue",
        )

    with cols[1]:

        render_kpi(
            "Total Profit",
            format_currency(profit),
            "Total realized profit",
        )

    with cols[2]:

        render_kpi(
            "Orders",
            format_number(orders),
            "Unique orders",
        )

    with cols[3]:

        render_kpi(
            "Profit Margin",
            f"{profit_margin:.1f}%",
            "Profit as percentage of revenue",
        )

    st.write("")

    cols = st.columns(4)

    with cols[0]:

        render_kpi(
            "Quantity Sold",
            format_number(quantity),
            "Units sold",
        )

    with cols[1]:

        render_kpi(
            "Customers",
            format_number(customers),
            "Unique customers",
        )

    with cols[2]:

        render_kpi(
            "Average Order Value",
            format_currency(
                average_order_value
            ),
            "Revenue per order",
        )

    with cols[3]:

        render_kpi(
            "Current Stock",
            format_number(current_stock),
            "Inventory units",
        )

    # ========================================================
    # INVENTORY ALERT
    # ========================================================

    if stockout_count > 0:

        st.warning(
            f"⚠️ {stockout_count:,} inventory record(s) "
            "are currently marked as stockout."
        )

    # ========================================================
    # MONTHLY REVENUE
    # ========================================================

    render_section_title(
        "Revenue Trend"
    )

    if (
        "order_date" in filtered_sales.columns
        and "revenue" in filtered_sales.columns
    ):

        monthly = (
            filtered_sales
            .dropna(
                subset=["order_date"]
            )
            .assign(
                month=lambda x:
                x["order_date"]
                .dt.to_period("M")
                .astype(str)
            )
            .groupby(
                "month",
                as_index=False
            )["revenue"]
            .sum()
        )

        if not monthly.empty:

            fig = px.line(
                monthly,
                x="month",
                y="revenue",
                markers=True,
                title="Monthly Revenue",
            )

            fig.update_traces(
                line_width=3
            )

            fig.update_yaxes(
                tickprefix="₹"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    # ========================================================
    # REVENUE VS PROFIT
    # ========================================================

    render_section_title(
        "Revenue vs Profit"
    )

    if (
        "order_date" in filtered_sales.columns
        and "revenue" in filtered_sales.columns
        and "profit" in filtered_sales.columns
    ):

        monthly = (
            filtered_sales
            .dropna(
                subset=["order_date"]
            )
            .assign(
                month=lambda x:
                x["order_date"]
                .dt.to_period("M")
                .astype(str)
            )
            .groupby(
                "month",
                as_index=False
            )[
                ["revenue", "profit"]
            ]
            .sum()
        )

        if not monthly.empty:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=monthly["month"],
                    y=monthly["revenue"],
                    name="Revenue",
                )
            )

            fig.add_trace(
                go.Bar(
                    x=monthly["month"],
                    y=monthly["profit"],
                    name="Profit",
                )
            )

            fig.update_layout(
                barmode="group",
                title="Monthly Revenue vs Profit",
            )

            fig.update_yaxes(
                tickprefix="₹"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    # ========================================================
    # MEDICINES + CATEGORY
    # ========================================================

    left, right = st.columns(2)

    with left:

        render_section_title(
            "Top Medicines by Revenue"
        )

        if (
            "medicine_name"
            in filtered_sales.columns
            and "revenue"
            in filtered_sales.columns
        ):

            top_medicines = (
                filtered_sales
                .groupby(
                    "medicine_name",
                    as_index=False
                )["revenue"]
                .sum()
                .sort_values(
                    "revenue",
                    ascending=False,
                )
                .head(10)
            )

            if not top_medicines.empty:

                fig = px.bar(
                    top_medicines.sort_values(
                        "revenue"
                    ),
                    x="revenue",
                    y="medicine_name",
                    orientation="h",
                    title="Top 10 Medicines",
                )

                fig.update_xaxes(
                    tickprefix="₹"
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )

    with right:

        render_section_title(
            "Revenue by Category"
        )

        if (
            "category"
            in filtered_sales.columns
            and "revenue"
            in filtered_sales.columns
        ):

            category_data = (
                filtered_sales
                .groupby(
                    "category",
                    as_index=False
                )["revenue"]
                .sum()
                .sort_values(
                    "revenue",
                    ascending=False,
                )
            )

            if not category_data.empty:

                fig = px.bar(
                    category_data,
                    x="category",
                    y="revenue",
                    title="Revenue by Category",
                )

                fig.update_yaxes(
                    tickprefix="₹"
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )

    # ========================================================
    # CITY + CHANNEL
    # ========================================================

    left, right = st.columns(2)

    with left:

        render_section_title(
            "Sales by City"
        )

        if (
            "city" in filtered_sales.columns
            and "revenue" in filtered_sales.columns
        ):

            city_data = (
                filtered_sales
                .groupby(
                    "city",
                    as_index=False
                )["revenue"]
                .sum()
                .sort_values(
                    "revenue",
                    ascending=False,
                )
                .head(10)
            )

            if not city_data.empty:

                fig = px.bar(
                    city_data,
                    x="city",
                    y="revenue",
                    title="Top Cities",
                )

                fig.update_yaxes(
                    tickprefix="₹"
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )

    with right:

        render_section_title(
            "Sales Channel"
        )

        if "channel" in filtered_sales.columns:

            channel_data = (
                filtered_sales[
                    "channel"
                ]
                .value_counts()
                .reset_index()
            )

            channel_data.columns = [
                "channel",
                "count",
            ]

            fig = px.pie(
                channel_data,
                names="channel",
                values="count",
                hole=0.55,
                title="Orders by Channel",
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    # ========================================================
    # PAYMENT + INVENTORY
    # ========================================================

    left, right = st.columns(2)

    with left:

        render_section_title(
            "Payment Methods"
        )

        if "payment_method" in filtered_sales.columns:

            payment_data = (
                filtered_sales[
                    "payment_method"
                ]
                .value_counts()
                .reset_index()
            )

            payment_data.columns = [
                "payment_method",
                "count",
            ]

            fig = px.pie(
                payment_data,
                names="payment_method",
                values="count",
                hole=0.55,
                title="Orders by Payment Method",
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    with right:

        render_section_title(
            "Inventory Status"
        )

        if "inventory_status" in filtered_inventory.columns:

            inventory_data = (
                filtered_inventory[
                    "inventory_status"
                ]
                .value_counts()
                .reset_index()
            )

            inventory_data.columns = [
                "inventory_status",
                "count",
            ]

            fig = px.pie(
                inventory_data,
                names="inventory_status",
                values="count",
                hole=0.55,
                title="Inventory Status Distribution",
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

    # ========================================================
    # SUMMARY
    # ========================================================

    render_section_title(
        "Filtered Dataset Summary"
    )

    st.caption(
        f"Showing {len(filtered_sales):,} sales records "
        f"and {len(filtered_inventory):,} inventory records."
    )


# ============================================================
# HELPERS
# ============================================================

def numeric_sum(df, column):

    if df.empty or column not in df.columns:
        return 0.0

    return pd.to_numeric(
        df[column],
        errors="coerce",
    ).fillna(0).sum()


def unique_count(df, column):

    if df.empty or column not in df.columns:
        return 0

    return df[column].nunique(
        dropna=True
    )