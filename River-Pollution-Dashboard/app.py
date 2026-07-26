import streamlit as st

from utils.loader import *
from utils.cleaner import *
from utils.charts import *
from tabs.pde_tab import show_pde_tab

st.set_page_config(
    page_title="River Pollution Dashboard",
    page_icon="🌊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------

ganga_df = clean_ganga(load_ganga_data())
water_df = clean_water(load_waterquality_data())

# -----------------------------
# Title
# -----------------------------

st.title("🌊 River Pollution Monitoring Dashboard")

st.write(
    "Water Pollution Analysis using Data Analytics and PDE Simulation"
)

# -----------------------------
# Tabs
# -----------------------------

dashboard_tab, ganga_tab, water_tab, comparison_tab, pde_tab, report_tab, about_tab = st.tabs(
    [
        "📊 Dashboard",
        "🌊 Ganga Analysis",
        "💧 Water Quality",
        "📈 Comparison",
        "📐 PDE Simulation",
        "📄 Reports",
        "ℹ️ About"
    ]
)

# ==========================================
# DASHBOARD TAB
# ==========================================

with dashboard_tab:

    st.header("📊 Dashboard")

    # Dataset Selection
    dataset = st.selectbox(
        "Select Dataset",
        ["Ganga River", "Water Quality"]
    )

    if dataset == "Ganga River":

        df = ganga_df.copy()

        st.subheader("🔍 Filters")

        col_filter1, col_filter2 = st.columns(2)

        with col_filter1:
            start_date = st.date_input(
                "Start Date",
                value=df["Date"].min().date()
            )

        with col_filter2:
            end_date = st.date_input(
                "End Date",
                value=df["Date"].max().date()
            )

        # Apply Date Filter
        df = df[
            (df["Date"].dt.date >= start_date) &
            (df["Date"].dt.date <= end_date)
        ]

        status = st.multiselect(
            "Water Quality Status",
            options=sorted(df["Status"].unique()),
            default=sorted(df["Status"].unique())
        )

        df = df[df["Status"].isin(status)]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Records", len(df))

        with col2:
            st.metric("Average pH", round(df["pH"].mean(), 2))

        with col3:
            st.metric("Average DO", round(df["DO"].mean(), 2))

        with col4:
            st.metric("Average WQI", round(df["WQI"].mean(), 2))

    else:

        df = water_df.copy()

        st.subheader("🔍 Filters")

        col_filter1, col_filter2 = st.columns(2)

        with col_filter1:

            selected_states = st.multiselect(
                "Select State",
                options=sorted(df["STATE"].dropna().unique()),
                default=sorted(df["STATE"].dropna().unique())
            )

        with col_filter2:

            selected_locations = st.multiselect(
                "Select Location",
                options=sorted(df["LOCATIONS"].dropna().unique()),
                default=sorted(df["LOCATIONS"].dropna().unique())
            )

        df = df[
            (df["STATE"].isin(selected_states)) &
            (df["LOCATIONS"].isin(selected_locations))
        ]

        # KPI Cards

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Records", len(df))

        with col2:
            st.metric("Average pH", round(df["pH"].mean(), 2))

        with col3:
            st.metric("Average DO", round(df["DO"].mean(), 2))

        with col4:
            st.metric("Average BOD", round(df["BOD"].mean(), 2))


    st.divider()

    if dataset == "Ganga River":

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                line_chart(
                    df,
                    "Date",
                    "DO",
                    "DO Trend Over Time"
                ),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                line_chart(
                    df,
                    "Date",
                    "pH",
                    "pH Trend Over Time"
                ),
                use_container_width=True
            )
        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                line_chart(
                    df,
                    "Date",
                    "Temp",
                    "Temperature Trend"
                ),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                line_chart(
                    df,
                    "Date",
                    "ORP",
                    "ORP Trend"
                ),
                use_container_width=True
            )
        st.plotly_chart(
            line_chart(
                df,
                "Date",
                "Cond",
                "Conductivity Trend"
            ),
            use_container_width=True
        )

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                pie_chart(
                    df,
                    "Status",
                    "Water Quality Status"
                ),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                histogram(
                    df,
                    "WQI",
                    "Water Quality Index Distribution"
                ),
                use_container_width=True
            )

    else:

    # -----------------------------
    # Average BOD by State
    # -----------------------------

        top_bod = (
            df.groupby("STATE")["BOD"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        # -----------------------------
        # Average DO by State
        # -----------------------------

        top_do = (
            df.groupby("STATE")["DO"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        left, right = st.columns(2)

        with left:

            st.plotly_chart(
                bar_chart(
                    top_bod,
                    "STATE",
                    "BOD",
                    "Average BOD by State"
                ),
                use_container_width=True
            )

        with right:

            st.plotly_chart(
                bar_chart(
                    top_do,
                    "STATE",
                    "DO",
                    "Average DO by State"
                ),
                use_container_width=True
            )

        left, right = st.columns(2)

        with left:

            st.plotly_chart(
                histogram(
                    df,
                    "pH",
                    "pH Distribution"
                ),
                use_container_width=True
            )

        with right:

            st.plotly_chart(
                histogram(
                    df,
                    "CONDUCTIVITY",
                    "Conductivity Distribution"
                ),
                use_container_width=True
            )

        st.plotly_chart(
            scatter_chart(
                df,
                "DO",
                "BOD",
                "DO vs BOD"
            ),
            use_container_width=True
        )

#Adding Charts

    st.divider()

    st.subheader("📋 Latest Records")

    st.dataframe(
        df.tail(20),
        use_container_width=True
    )


    # Download button
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Dataset",
        csv,
        "river_data.csv",
        "text/csv"
    )

with pde_tab:
    show_pde_tab()