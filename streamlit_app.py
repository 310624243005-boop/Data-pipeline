from pathlib import Path

import pandas as pd
import streamlit as st

from pipeline import load_raw_data

PROJECT_ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Data Pipeline Dashboard", page_icon="📊", layout="wide")

if "raw_data" not in st.session_state:
    st.session_state.raw_data = pd.DataFrame()
if "cleaned_data" not in st.session_state:
    st.session_state.cleaned_data = pd.DataFrame()
if "quality_report" not in st.session_state:
    st.session_state.quality_report = {}
if "feature_view" not in st.session_state:
    st.session_state.feature_view = pd.DataFrame()
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = "sample_data.csv"

home = st.Page("pages/0_Home.py", title="🏠 Home", icon="🏠")
dashboard = st.Page("pages/1_Dashboard.py", title="📊 Dashboard", icon="📊")
upload = st.Page("pages/2_Upload_Data.py", title="📤 Upload Data", icon="📤")
run_pipeline = st.Page("pages/3_Run_Pipeline.py", title="🔄 Run Pipeline", icon="🔄")
cleaning = st.Page("pages/4_Data_Cleaning.py", title="🧹 Data Cleaning", icon="🧹")
quality = st.Page("pages/5_Data_Quality.py", title="✅ Data Quality", icon="✅")
warehouse = st.Page("pages/6_Warehouse.py", title="🗄️ Warehouse", icon="🗄️")
analytics = st.Page("pages/7_Analytics.py", title="📈 Analytics", icon="📈")
feature_view = st.Page("pages/8_Feature_View.py", title="🤖 Feature View", icon="🤖")

pg = st.navigation({
    "Project": [home],
    "Workflow": [dashboard, upload, run_pipeline, cleaning, quality, warehouse, analytics, feature_view],
})

pg.run()
