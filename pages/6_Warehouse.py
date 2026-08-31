import pandas as pd
import streamlit as st

from pipeline import query_database

st.title("Warehouse")
st.caption("SQLite warehouse loaded from the cleaned data")

try:
    df = query_database("SELECT * FROM cleaned_orders")
    st.dataframe(df, use_container_width=True)
    st.metric("Rows in warehouse", len(df))
except Exception as exc:
    st.warning(f"Warehouse not populated yet: {exc}")
