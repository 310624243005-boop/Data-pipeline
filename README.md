# Data Pipeline Studio

A student-friendly Streamlit project that demonstrates the full data engineering workflow:

CSV / API → Airflow DAG → Extract → Pandas Cleaning → Data Quality Checks → SQLite Warehouse → Streamlit Dashboard → Analytics / AI Feature View

## Features

- Streamlit web app with multiple pages
- CSV upload support
- pandas-based data cleaning
- basic quality checks for nulls and invalid values
- SQLite warehouse storage
- analytics dashboard with Plotly charts
- ML-ready feature view table

## Project Structure

```text
data_pipeline/
├── airflow/
│   └── dags/
│       └── data_pipeline.py
├── data/
│   └── sample_data.csv
├── warehouse/
│   └── warehouse.db
├── streamlit_app.py
├── pipeline.py
├── requirements.txt
├── schema.sql
├── data_dictionary.md
├── README.md
└── pages/
    ├── 0_Home.py
    ├── 1_Dashboard.py
    ├── 2_Upload_Data.py
    ├── 3_Run_Pipeline.py
    ├── 4_Data_Cleaning.py
    ├── 5_Data_Quality.py
    ├── 6_Warehouse.py
    ├── 7_Analytics.py
    └── 8_Feature_View.py
```

## Setup

1. Create a virtual environment
2. Install requirements

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

## Run with Airflow

The DAG at `airflow/dags/data_pipeline.py` runs the existing pipeline once per day.
It stores cleaned records in `warehouse/warehouse.db` in the `cleaned_orders` table
and records each run in `pipeline_runs`. Copy the `airflow/dags` folder into the
Airflow DAGs directory, then enable `data_pipeline_to_sqlite_warehouse` in the
Airflow UI.

## Notes

- SQLite is used as the initial warehouse for local development.
- Airflow orchestrates the existing pipeline and SQLite is used as the local warehouse.
- The demo pipeline is intentionally simple and suitable for student project work.
