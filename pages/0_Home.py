import pandas as pd
import streamlit as st

from pipeline import load_raw_data

st.title("Data Pipeline Studio")
st.caption("Extract → Clean → Quality Check → Warehouse → Analytics")

st.subheader("Project Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Warehouse", "SQLite")
col2.metric("Frontend", "Streamlit")
col3.metric("Processing", "pandas")

st.markdown(
    """
    This project demonstrates a student-friendly data engineering workflow:
    - CSV / API input
    - pandas-based cleaning
    - data quality validation
    - SQLite warehouse loading
    - analytics and ML-ready feature generation
    """
)

try:
    sample_df = load_raw_data()
    st.success(f"Sample dataset loaded successfully: {len(sample_df)} rows")
    st.dataframe(sample_df.head(10), use_container_width=True)
except Exception as exc:
    st.warning(f"Sample data is not available yet: {exc}")
