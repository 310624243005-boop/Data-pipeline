import streamlit as st

from pipeline import load_raw_data, data_quality_report

st.title("Data Quality")
st.caption("Check nulls, duplicates, and invalid values")

try:
    source_path = st.session_state.get("data_source_path")
    df = load_raw_data(source_path)
    report = data_quality_report(df)
    st.json(report)
except Exception as exc:
    st.error(f"Unable to generate quality report: {exc}")
