import streamlit as st

from pipeline import generate_feature_view, query_database

st.title("Feature View")
st.caption("Cleaned data prepared for future AI / ML models")

try:
    df = query_database("SELECT * FROM cleaned_orders")
    feature_df = generate_feature_view(df)
    st.dataframe(feature_df.head(20), use_container_width=True)
except Exception as exc:
    st.error(f"Feature view could not be prepared: {exc}")
