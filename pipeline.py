from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"
DB_PATH = WAREHOUSE_DIR / "warehouse.db"
SCHEMA_PATH = PROJECT_ROOT / "schema.sql"
SAMPLE_DATA_PATH = DATA_DIR / "sample_data.csv"


def ensure_database() -> str:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    return str(DB_PATH)


def load_raw_data(file_path: str | Path | None = None) -> pd.DataFrame:
    source = Path(file_path) if file_path else SAMPLE_DATA_PATH
    if not source.exists():
        raise FileNotFoundError(f"CSV not found: {source}")
    df = pd.read_csv(source)
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    def find_column(candidates: list[str]) -> str | None:
        return next((column for column in candidates if column in cleaned.columns), None)

    for column in cleaned.columns:
        if cleaned[column].dtype == object:
            cleaned[column] = cleaned[column].replace({np.nan: None, pd.NA: None})
            cleaned[column] = cleaned[column].apply(
                lambda value: value.strip() if isinstance(value, str) else value
            )
            cleaned[column] = cleaned[column].fillna("unknown")

    amount_column = find_column(["amount", "purchase_amount", "price", "revenue", "total_amount"])
    quantity_column = find_column(["quantity", "orders", "order_count", "units"])
    age_column = find_column(["customer_age", "age"])
    numeric_candidates = [column for column in [amount_column, quantity_column, age_column] if column]
    for column in numeric_candidates:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
            median_value = cleaned[column].median()
            if pd.notna(median_value):
                cleaned[column] = cleaned[column].fillna(median_value)

    if amount_column:
        cleaned[amount_column] = cleaned[amount_column].abs()
    if quantity_column:
        cleaned[quantity_column] = cleaned[quantity_column].round().astype(int)
    if age_column:
        cleaned[age_column] = cleaned[age_column].clip(lower=18, upper=100).round().astype(int)
    if "status" in cleaned.columns:
        cleaned["status"] = cleaned["status"].replace({"": "pending", "unknown": "pending"})
    if "region" in cleaned.columns:
        cleaned["region"] = cleaned["region"].replace({"": "unknown"})
    if "order_date" in cleaned.columns:
        cleaned["order_date"] = pd.to_datetime(cleaned["order_date"], errors="coerce").dt.strftime("%Y-%m-%d")
        cleaned["order_date"] = cleaned["order_date"].replace({"NaT": "unknown"})

    if amount_column:
        cleaned["is_high_value"] = (cleaned[amount_column] > cleaned[amount_column].median()).astype(int)
    else:
        cleaned["is_high_value"] = 0
    if amount_column and quantity_column:
        cleaned["amount_per_item"] = (cleaned[amount_column] / cleaned[quantity_column]).replace(
            [np.inf, -np.inf], np.nan
        )
        cleaned["amount_per_item"] = cleaned["amount_per_item"].fillna(cleaned[amount_column].mean())

    return cleaned


def data_quality_report(df: pd.DataFrame) -> dict:
    report = {
        "total_rows": int(len(df)),
        "nulls_by_column": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "invalid_values": {},
    }

    if "amount" in df.columns:
        report["invalid_values"]["negative_amount"] = int(pd.to_numeric(df["amount"], errors="coerce").lt(0).sum())
    if "customer_age" in df.columns:
        report["invalid_values"]["age_out_of_range"] = int(
            (~df["customer_age"].between(18, 100, inclusive="both")).sum()
        )
    if "status" in df.columns:
        valid_statuses = {"pending", "paid", "cancelled", "shipped"}
        report["invalid_values"]["invalid_status"] = int(
            ~df["status"].fillna("unknown").str.lower().isin({s.lower() for s in valid_statuses}).sum()
        )

    report["null_total"] = int(df.isna().sum().sum())
    report["columns"] = list(df.columns)
    return report


def save_to_database(df: pd.DataFrame, table_name: str = "cleaned_orders") -> None:
    ensure_database()
    conn = sqlite3.connect(DB_PATH)
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()
    finally:
        conn.close()


def generate_feature_view(df: pd.DataFrame) -> pd.DataFrame:
    feature_df = df.copy()
    if "order_date" in feature_df.columns:
        feature_df["order_date"] = pd.to_datetime(feature_df["order_date"], errors="coerce")
    feature_df["total_value"] = feature_df["amount"] if "amount" in feature_df.columns else 0
    feature_df["quantity_bin"] = pd.qcut(
        feature_df["quantity"], q=4, duplicates="drop", labels=["low", "medium", "high", "very_high"]
    ) if "quantity" in feature_df.columns else "unknown"
    feature_df["customer_segment"] = np.where(
        feature_df.get("customer_age", 0) >= 40, "mature", "young"
    )
    return feature_df


def run_full_pipeline(file_path: str | Path | None = None) -> dict:
    ensure_database()
    raw_df = load_raw_data(file_path)
    cleaned_df = clean_dataframe(raw_df)
    quality = data_quality_report(raw_df)
    save_to_database(cleaned_df)
    feature_view = generate_feature_view(cleaned_df)

    conn = sqlite3.connect(DB_PATH)
    rows_cleaned = len(cleaned_df)
    duplicates_removed = int(raw_df.duplicated().sum())
    nulls_fixed = int(raw_df.isna().sum().sum())
    conn.execute(
        "INSERT INTO pipeline_runs (source_file, rows_loaded, rows_cleaned, duplicates_removed, nulls_fixed) VALUES (?, ?, ?, ?, ?)",
        (str(file_path or SAMPLE_DATA_PATH), len(raw_df), rows_cleaned, duplicates_removed, nulls_fixed),
    )
    conn.commit()
    conn.close()

    return {
        "raw": raw_df,
        "cleaned": cleaned_df,
        "quality": quality,
        "feature_view": feature_view,
        "database_path": str(DB_PATH),
    }


def query_database(query: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


if __name__ == "__main__":
    result = run_full_pipeline()
    print(f"Rows loaded: {len(result['raw'])}")
    print(f"Rows cleaned: {len(result['cleaned'])}")
    print(f"Warehouse: {result['database_path']}")
