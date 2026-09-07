import streamlit as st

from pipeline import run_full_pipeline

st.title("Run Pipeline")
st.caption("Trigger the full extract → clean → quality check → load workflow")

if st.button("Run pipeline"):
    try:
        source_path = st.session_state.get("data_source_path")
        result = run_full_pipeline(source_path)
        st.session_state.raw_data = result["raw"]
        st.session_state.cleaned_data = result["cleaned"]
        st.session_state.quality_report = result["quality"]
        st.session_state.feature_view = result["feature_view"]
        st.success("Pipeline executed successfully")
        st.json({
            "source_file": source_path,
            "rows_loaded": len(result["raw"]),
            "rows_cleaned": len(result["cleaned"]),
            "quality_checks": result["quality"],
        })
    except Exception as exc:
        st.error(f"Pipeline failed: {exc}")
else:
    source_name = st.session_state.get("uploaded_file_name", "sample_data.csv")
    st.info(f"Current source: {source_name}. Click the button above to process it and load it into SQLite.")
