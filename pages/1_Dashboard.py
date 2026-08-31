import pandas as pd
import streamlit as st

from pipeline import query_database

st.title("Dashboard")
st.caption("Pipeline status and dataset overview")

try:
    table_df = query_database("SELECT * FROM cleaned_orders LIMIT 10")
    summary = query_database("SELECT COUNT(*) AS row_count FROM cleaned_orders")
    if not table_df.empty:
        st.metric("Cleaned Records", int(summary.iloc[0]["row_count"]))
        st.dataframe(table_df, use_container_width=True)
    else:
        st.info("No data has been loaded into the warehouse yet. Run the pipeline first.")
except Exception as exc:
    st.warning(f"Warehouse is empty or unavailable: {exc}")
