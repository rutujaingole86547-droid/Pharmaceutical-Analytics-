"""
Demand Forecasting module.

Displays pre-generated machine-learning demand forecasts
and model comparison results.
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
    load_forecast_data,
    load_model_comparison,
)

from utils.helpers import format_number


# ============================================================
# CHART STYLE
# ============================================================

def style_chart(fig):

    fig.update_layout(
        height=380,
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

def show_forecasting():

    render_header(
        "Medicine Demand Forecasting",
        "Machine-learning based demand intelligence for pharmaceutical inventory planning",
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    forecast_df = load_forecast_data()

    model_df = load_model_comparison()

    if forecast_df.empty:

        st.error(
            "Forecast data is not available."
        )

        st.info(
            "Please generate "
            "medicine_demand_forecast_2026.csv "
            "before using this module."
        )

        return

    # ========================================================
    # REQUIRED COLUMN
    # ========================================================

    if "forecast_demand" not in forecast_df.columns:

        st.error(
            "The forecast file does not contain "
            "'forecast_demand'."
        )

        return

    forecast_df["forecast_demand"] = (
        pd.to_numeric(
            forecast_df["forecast_demand"],
            errors="coerce",
        )
        .fillna(0)
    )

    # ========================================================
    # FILTER
    # ========================================================

    st.sidebar.markdown(
        "### Forecast Filters"
    )

    filtered_df = forecast_df.copy()

    if "medicine_name" in filtered_df.columns:

        medicines = sorted(
            filtered_df[
                "medicine_name"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_medicine = st.sidebar.selectbox(
            "Medicine",
            ["All"] + medicines,
        )

        if selected_medicine != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "medicine_name"
                ].astype(str)
                == selected_medicine
            ]

    # ========================================================
    # KPI
    # ========================================================

    total_forecast = filtered_df[
        "forecast_demand"
    ].sum()

    average_forecast = filtered_df[
        "forecast_demand"
    ].mean()

    peak_forecast = filtered_df[
        "forecast_demand"
    ].max()

    unique_products = (
        filtered_df[
            "product_id"
        ].nunique()
        if "product_id"
        in filtered_df.columns
        else 0
    )

    render_section_title(
        "Forecast Overview"
    )

    cols = st.columns(4)

    with cols[0]:

        render_kpi(
            "Forecast Demand",
            format_number(total_forecast),
            "Total predicted demand",
        )

    with cols[1]:

        render_kpi(
            "Average Forecast",
            format_number(average_forecast),
            "Average forecast value",
        )

    with cols[2]:

        render_kpi(
            "Peak Forecast",
            format_number(peak_forecast),
            "Highest forecast value",
        )

    with cols[3]:

        render_kpi(
            "Medicines",
            format_number(unique_products),
            "Products covered",
        )

    # ========================================================
    # TREND
    # ========================================================

    render_section_title(
        "Forecast Demand Trend"
    )

    date_column = None

    for column in filtered_df.columns:

        if (
            "month" in column.lower()
            or "date" in column.lower()
        ):

            date_column = column
            break

    if date_column is not None:

        temp = filtered_df.copy()

        temp["_date"] = pd.to_datetime(
            temp[date_column],
            errors="coerce",
        )

        temp = temp.dropna(
            subset=["_date"]
        )

        if not temp.empty:

            monthly = (
                temp
                .groupby(
                    "_date",
                    as_index=False
                )["forecast_demand"]
                .sum()
                .sort_values("_date")
            )

            fig = px.line(
                monthly,
                x="_date",
                y="forecast_demand",
                markers=True,
                title="Forecast Demand Over Time",
            )

            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Forecast Demand",
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

        else:

            st.info(
                "No valid forecast date/month values were found."
            )

    else:

        st.info(
            "A month/date column was not found "
            "in the forecast file."
        )

    # ========================================================
    # TOP MEDICINES
    # ========================================================

    render_section_title(
        "Top Forecasted Medicines"
    )

    if "medicine_name" in filtered_df.columns:

        top_medicines = (
            filtered_df
            .groupby(
                "medicine_name",
                as_index=False
            )["forecast_demand"]
            .sum()
            .sort_values(
                "forecast_demand",
                ascending=False,
            )
            .head(10)
        )

        name_column = "medicine_name"

    elif "product_id" in filtered_df.columns:

        top_medicines = (
            filtered_df
            .groupby(
                "product_id",
                as_index=False
            )["forecast_demand"]
            .sum()
            .sort_values(
                "forecast_demand",
                ascending=False,
            )
            .head(10)
        )

        name_column = "product_id"

    else:

        top_medicines = pd.DataFrame()

        name_column = None

    if not top_medicines.empty:

        fig = px.bar(
            top_medicines.sort_values(
                "forecast_demand"
            ),
            x="forecast_demand",
            y=name_column,
            orientation="h",
            title="Top 10 Medicines by Forecast Demand",
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

    # ========================================================
    # MODEL COMPARISON
    # ========================================================

    render_section_title(
        "Forecast Model Comparison"
    )

    if not model_df.empty:

        st.dataframe(
            model_df,
            use_container_width=True,
            hide_index=True,
        )

        mae_column = None

        for column in model_df.columns:

            if column.lower() == "mae":
                mae_column = column
                break

        if mae_column:

            model_df[mae_column] = pd.to_numeric(
                model_df[mae_column],
                errors="coerce",
            )

            valid_models = model_df.dropna(
                subset=[mae_column]
            )

            if not valid_models.empty:

                best_row = valid_models.loc[
                    valid_models[
                        mae_column
                    ].idxmin()
                ]

                model_name = best_row.get(
                    "model",
                    best_row.get(
                        "model_name",
                        "Best Model",
                    ),
                )

                best_mae = best_row[
                    mae_column
                ]

                st.success(
                    f"Best performing model: "
                    f"**{model_name}** "
                    f"with MAE = **{best_mae:.4f}**"
                )

    else:

        st.info(
            "Model comparison data is not available."
        )

    # ========================================================
    # DETAILS
    # ========================================================

    render_section_title(
        "Forecast Details"
    )

    st.dataframe(
        filtered_df.head(200),
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
        label="⬇️ Download Forecast Data",
        data=csv_data,
        file_name="filtered_medicine_forecast.csv",
        mime="text/csv",
    )