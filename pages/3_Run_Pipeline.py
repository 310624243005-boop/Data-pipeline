import streamlit as st

from pipeline import run_full_pipeline

st.title("Run Pipeline")
st.caption("Trigger the full extract → clean → quality check → load workflow")

if st.button("Run pipeline"):
    try:
        result = run_full_pipeline()
        st.success("Pipeline executed successfully")
        st.json({
            "rows_loaded": len(result["raw"]),
            "rows_cleaned": len(result["cleaned"]),
            "quality_checks": result["quality"],
        })
    except Exception as exc:
        st.error(f"Pipeline failed: {exc}")
else:
    st.info("Click the button above to process the sample data and load it into SQLite.")
