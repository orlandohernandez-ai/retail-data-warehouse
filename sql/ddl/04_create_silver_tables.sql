CREATE TABLE IF NOT EXISTS silver.sales_clean (
    order_id INTEGER PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    store_id VARCHAR(20) NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
    source_file VARCHAR(255) NOT NULL,
    bronze_load_timestamp TIMESTAMP NOT NULL,
    silver_load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);