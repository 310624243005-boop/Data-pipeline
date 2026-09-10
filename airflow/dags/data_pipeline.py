from datetime import datetime, timedelta
from pathlib import Path
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline import run_full_pipeline


def load_data_into_warehouse() -> None:
    run_full_pipeline(PROJECT_ROOT / "data" / "sample_data.csv")


with DAG(
    dag_id="data_pipeline_to_sqlite_warehouse",
    start_date=datetime(2024, 1, 1),
    schedule=timedelta(days=1),
    catchup=False,
    default_args={
        "owner": "data-engineering",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["etl", "warehouse"],
) as dag:
    store_cleaned_data = PythonOperator(
        task_id="store_cleaned_data_in_warehouse",
        python_callable=load_data_into_warehouse,
    )