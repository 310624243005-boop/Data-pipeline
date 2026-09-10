import plotly.express as px
import streamlit as st

from pipeline import generate_feature_view, query_database

st.title("Feature View")
st.caption("Cleaned data prepared for future AI / ML models")

try:
    df = query_database("SELECT * FROM cleaned_orders")
    feature_df = generate_feature_view(df)

    if feature_df.empty:
        st.info("Run the pipeline first to populate the warehouse.")
    else:
        st.subheader("Graph Analytics")
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Orders", len(feature_df))
        metric_col2.metric("Total Value", f"${feature_df['total_value'].sum():,.2f}")
        metric_col3.metric("Average Order", f"${feature_df['total_value'].mean():,.2f}")

        if "order_date" in feature_df.columns:
            trend_df = (
                feature_df.dropna(subset=["order_date"])
                .groupby("order_date", as_index=False)["total_value"]
                .sum()
            )
            if not trend_df.empty:
                st.plotly_chart(
                    px.line(
                        trend_df,
                        x="order_date",
                        y="total_value",
                        markers=True,
                        title="Order Value Over Time",
                        labels={"order_date": "Order Date", "total_value": "Total Value"},
                    ),
                    use_container_width=True,
                )

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            segment_df = (
                feature_df.groupby("customer_segment", as_index=False)["total_value"]
                .agg(total_value="sum")
            )
            st.plotly_chart(
                px.bar(
                    segment_df,
                    x="customer_segment",
                    y="total_value",
                    color="customer_segment",
                    title="Value by Customer Segment",
                    labels={"customer_segment": "Segment", "total_value": "Total Value"},
                ),
                use_container_width=True,
            )

        with chart_col2:
            if {"quantity", "total_value"}.issubset(feature_df.columns):
                st.plotly_chart(
                    px.scatter(
                        feature_df,
                        x="quantity",
                        y="total_value",
                        color="customer_segment",
                        hover_data=["order_id"] if "order_id" in feature_df.columns else None,
                        title="Order Value vs Quantity",
                        labels={"quantity": "Quantity", "total_value": "Total Value"},
                    ),
                    use_container_width=True,
                )

        st.subheader("Feature Data")
    st.dataframe(feature_df.head(20), use_container_width=True)
except Exception as exc:
    st.error(f"Feature view could not be prepared: {exc}")
