import plotly.express as px
import streamlit as st

from pipeline import query_database

st.title("Analytics")
st.caption("Business insights and charts from the warehouse")

try:
    df = query_database("SELECT * FROM cleaned_orders")
    if df.empty:
        st.info("Run the pipeline first to populate the warehouse.")
    else:
        total_revenue = float(df["amount"].sum()) if "amount" in df.columns else 0
        avg_order = float(df["amount"].mean()) if "amount" in df.columns else 0
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:,.2f}")
        col2.metric("Average Order", f"${avg_order:,.2f}")
        col3.metric("Records", len(df))

        if "region" in df.columns:
            region_chart = df.groupby("region")["amount"].sum().reset_index()
            st.plotly_chart(px.bar(region_chart, x="region", y="amount", title="Revenue by Region"), use_container_width=True)

        if "status" in df.columns:
            status_chart = df["status"].value_counts().reset_index()
            status_chart.columns = ["status", "count"]
            st.plotly_chart(px.pie(status_chart, names="status", values="count", title="Order Status Distribution"), use_container_width=True)
except Exception as exc:
    st.error(f"Analytics could not be generated: {exc}")
