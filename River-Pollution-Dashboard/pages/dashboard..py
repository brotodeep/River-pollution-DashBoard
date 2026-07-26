import streamlit as st

from utils.loader import *
from utils.cleaner import *

def dashboard_page():

    st.header("📊 Dashboard")

    ganga_df = clean_ganga(load_ganga_data())
    water_df = clean_water(load_waterquality_data())

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Ganga Records", len(ganga_df))

    with col2:
        st.metric("Water Quality Records", len(water_df))

    st.dataframe(ganga_df.head())