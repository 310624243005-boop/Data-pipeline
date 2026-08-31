CREATE TABLE IF NOT EXISTS cleaned_orders (
    order_id TEXT,
    customer_name TEXT,
    region TEXT,
    order_date TEXT,
    amount REAL,
    quantity INTEGER,
    customer_age INTEGER,
    status TEXT,
    is_high_value INTEGER,
    amount_per_item REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT,
    rows_loaded INTEGER,
    rows_cleaned INTEGER,
    duplicates_removed INTEGER,
    nulls_fixed INTEGER,
    run_at TEXT DEFAULT CURRENT_TIMESTAMP
);
