-- ============================================================
-- Project : Retail Data Warehouse
-- Script  : 03_create_bronze_tables.sql
-- Purpose : Create raw ingestion tables for the Bronze layer.
-- ============================================================

CREATE TABLE IF NOT EXISTS bronze.sales_raw (
    order_id INT,
    order_date DATE,
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity INT,
    unit_price DECIMAL(10,2),
    store_id VARCHAR(20),
    source_file VARCHAR(255),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);