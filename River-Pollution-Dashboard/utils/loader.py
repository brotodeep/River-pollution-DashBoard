import pandas as pd
import streamlit as st


@st.cache_data
def load_ganga_data():
    return pd.read_csv("data/ganga_river.csv")


@st.cache_data
def load_waterquality_data():

    encodings = [
        "utf-8",
        "latin1",
        "cp1252",
        "ISO-8859-1"
    ]

    for enc in encodings:
        try:
            return pd.read_csv(
                "data/waterquality.csv",
                encoding=enc
            )
        except Exception:
            continue

    raise Exception("Unable to read waterquality.csv")