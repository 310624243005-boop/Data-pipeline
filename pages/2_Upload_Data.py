from pathlib import Path

import pandas as pd
import streamlit as st

from pipeline import load_raw_data

st.title("Upload Data")
st.caption("Upload a CSV file to replace the sample data for the pipeline")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    file_path = Path("data") / uploaded_file.name
    file_path.parent.mkdir(exist_ok=True, parents=True)
    file_path.write_bytes(uploaded_file.getvalue())
    st.session_state.uploaded_file_name = uploaded_file.name
    st.session_state.data_source_path = str(file_path.resolve())
    st.success(f"File saved: {file_path}")

    try:
        df = load_raw_data(file_path)
        st.dataframe(df.head(10), use_container_width=True)
    except Exception as exc:
        st.error(f"Unable to read uploaded file: {exc}")
else:
    st.info("Upload a CSV file to test the Extract step.")
