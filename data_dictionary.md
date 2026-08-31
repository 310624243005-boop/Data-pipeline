# Data Dictionary

## cleaned_orders

| Column | Type | Description |
|---|---|---|
| order_id | TEXT | Unique order identifier |
| customer_name | TEXT | Customer full name |
| region | TEXT | Customer region |
| order_date | TEXT | Order date in YYYY-MM-DD format |
| amount | REAL | Total order amount |
| quantity | INTEGER | Number of items purchased |
| customer_age | INTEGER | Customer age |
| status | TEXT | Order status |
| is_high_value | INTEGER | Flag for high-value orders |
| amount_per_item | REAL | Average value per item |
| created_at | TEXT | Record creation timestamp |

## pipeline_runs

| Column | Type | Description |
|---|---|---|
| run_id | INTEGER | Run identifier |
| source_file | TEXT | Source CSV file |
| rows_loaded | INTEGER | Number of rows read from source |
| rows_cleaned | INTEGER | Number of valid rows after cleaning |
| duplicates_removed | INTEGER | Number of duplicate rows removed |
| nulls_fixed | INTEGER | Number of missing values repaired |
| run_at | TEXT | Pipeline execution time |
