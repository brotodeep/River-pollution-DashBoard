import streamlit as st

from utils.pde_solver import simulate_pollution

from utils.charts import (
    pde_chart,
    heatmap_chart,
    animation_chart
)

def show_pde_tab():

    st.header("📐 PDE Pollution Simulation")

    st.markdown("""
    This module simulates the spread of pollutants in a river using the
    **1D Advection–Diffusion Equation**.

    The equation solved is:

    ∂C/∂t = D ∂²C/∂x² − v ∂C/∂x
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        river_length = st.slider(
            "River Length (km)",
            10,
            500,
            100
        )

        velocity = st.slider(
            "Flow Velocity (m/s)",
            0.1,
            5.0,
            1.0
        )

        initial_pollution = st.slider(
            "Initial Pollution (mg/L)",
            10,
            100,
            50
        )
        source_location = st.slider(
            "Pollution Source Location (km)",
            0,
            river_length,
            river_length // 4
        )

    with col2:

        grid_points = st.slider(
            "Grid Points",
            20,
            300,
            100
        )

        diffusion = st.slider(
            "Diffusion Coefficient",
            0.001,
            1.0,
            0.05
        )

        simulation_time = st.slider(
            "Simulation Time (hours)",
            1,
            100,
            20
        )

    st.divider()

    if st.button("▶ Run Simulation"):

        distance, concentration, history = simulate_pollution(
            river_length,
            grid_points,
            simulation_time,
            velocity,
            diffusion,
            initial_pollution,
            source_location
        )

        st.plotly_chart(
            pde_chart(
                distance,
                concentration,
                source_location
            ),
            use_container_width=True
        )

        #heatmap
        st.subheader("🌈 Pollution Heatmap")

        st.plotly_chart(
            heatmap_chart(history, distance),
            use_container_width=True
        )

        st.success("Simulation completed successfully.")

        st.subheader("🎬 Pollution Animation")
        
        st.plotly_chart(
            animation_chart(
                distance,
                history
            ),
            use_container_width=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Maximum Pollution",
                f"{concentration.max():.2f} mg/L"
            )

        with c2:
            st.metric(
                "Average Pollution",
                f"{concentration.mean():.2f} mg/L"
            )

        with c3:
            non_zero = concentration[concentration > 0]

        if len(non_zero) > 0:
            min_pollution = non_zero.min()
        else:
            min_pollution = 0

        st.metric(
            "Minimum Pollution",
            f"{min_pollution:.2f} mg/L"
        )
        # -----------------------------------------
        # Water Quality Assessment
        # -----------------------------------------

        st.divider()

        st.subheader("🚦 Water Quality Assessment")

        average_pollution = concentration.mean()

        if average_pollution < 20:
            st.success("✅ Safe Water Quality")

        elif average_pollution < 50:
            st.warning("⚠ Moderate Pollution")

        else:
            st.error("🚨 Highly Polluted Water")

    