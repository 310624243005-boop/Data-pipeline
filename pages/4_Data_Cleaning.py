import streamlit as st

from pipeline import load_raw_data, clean_dataframe

st.title("Data Cleaning")
st.caption("See the raw data before and after the cleaning logic")

try:
    raw_df = load_raw_data()
    clean_df = clean_dataframe(raw_df)

    tab1, tab2 = st.tabs(["Raw Data", "Cleaned Data"])
    with tab1:
        st.dataframe(raw_df.head(20), use_container_width=True)
    with tab2:
        st.dataframe(clean_df.head(20), use_container_width=True)
except Exception as exc:
    st.error(f"Could not prepare cleaning preview: {exc}")
