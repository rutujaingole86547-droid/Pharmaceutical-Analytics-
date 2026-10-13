"""
Main application for the Pharma Inventory Analytics Platform.
"""

import streamlit as st

from components.ui import (
    inject_custom_css,
    render_header,
    render_kpi,
    render_section_title,
    render_welcome,
    render_home_card,
    render_footer,
    render_app_title,
    render_home_welcome,
    render_ai_card,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Pharma Inventory Analytics Platform",
    page_icon="💊",
    layout="wide",
)


# ============================================================
# GLOBAL CSS
# ============================================================

inject_custom_css()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
<div style="
    font-size:1.35rem;
    font-weight:750;
    margin-bottom:0.25rem;
">
    💊 Pharma Analytics
</div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "AI-Powered Inventory & Demand Intelligence"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📊 Analytics Dashboard",
            "📈 Demand Forecasting",
            "🤖 AI Recommendations",
            "💊 Medicine Details",
        ],
    )

    st.divider()

    st.caption(
        "Pharma Inventory Analytics Platform"
    )

    st.caption(
        "Data Analyst Internship Project"
    )


# ============================================================
# HOME
# ============================================================
# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    render_header(
        "Pharma Inventory Analytics Platform",
        "AI-powered pharmaceutical sales, inventory, "
        "demand forecasting and decision intelligence"
    )


    # --------------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------------

    render_welcome(
        "Welcome to the Pharma Inventory Analytics Platform.",
        "This platform combines pharmaceutical sales analytics, "
        "inventory intelligence, machine-learning demand forecasting "
        "and AI-assisted inventory recommendations into a single "
        "decision-support application."
    )


    # --------------------------------------------------------
    # MODULES
    # --------------------------------------------------------

    render_section_title("Platform Modules")


    col1, col2 = st.columns(2)

    with col1:

        render_home_card(
            "📊 Analytics Dashboard",
            "Explore revenue, profit, orders, customers, products, "
            "categories, cities, sales channels and inventory performance."
        )

    with col2:

        render_home_card(
            "📈 Demand Forecasting",
            "Analyze machine-learning based medicine demand forecasts "
            "and understand expected future demand."
        )


    col3, col4 = st.columns(2)

    with col3:

        render_home_card(
            "🤖 AI Recommendations",
            "Identify inventory risks, reorder requirements, priority "
            "medicines and estimated reorder costs."
        )

    with col4:

        render_home_card(
            "💊 Medicine Details",
            "Explore medicine-level information including categories, "
            "manufacturers, inventory and demand."
        )


    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    render_section_title("Platform Workflow")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.info(
            "📁\n\n"
            "**Cleaned Data**\n\n"
            "Sales, inventory and product data"
        )


    with col2:

        st.info(
            "📊\n\n"
            "**Analytics**\n\n"
            "Business performance analysis"
        )


    with col3:

        st.info(
            "🧠\n\n"
            "**ML Forecasting**\n\n"
            "Future medicine demand"
        )


    with col4:

        st.info(
            "🤖\n\n"
            "**AI Decisions**\n\n"
            "Inventory recommendations"
        )
# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

elif page == "📊 Analytics Dashboard":

    try:

        from modules.dashboard import show_dashboard

        show_dashboard()

    except Exception as error:

        st.error(
            "Analytics Dashboard could not be loaded."
        )

        st.exception(error)


# ============================================================
# DEMAND FORECASTING
# ============================================================

elif page == "📈 Demand Forecasting":

    try:

        from modules.forecasting import show_forecasting

        show_forecasting()

    except Exception as error:

        st.error(
            "Demand Forecasting could not be loaded."
        )

        st.exception(error)


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

elif page == "🤖 AI Recommendations":

    try:

        from modules.recommendations import show_recommendations

        show_recommendations()

    except Exception as error:

        st.error(
            "AI Recommendations could not be loaded."
        )

        st.exception(error)


# ============================================================
# MEDICINE DETAILS
# ============================================================

elif page == "💊 Medicine Details":

    try:

        from modules.medicine_details import show_medicine_details

        show_medicine_details()

    except Exception as error:

        st.error(
            "Medicine Details could not be loaded."
        )

        st.exception(error)


# ============================================================
# FOOTER
# ============================================================

render_footer()