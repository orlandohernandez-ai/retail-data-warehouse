"""
Project: Retail Data Warehouse
Layer: Gold
File: transform_sales_to_gold.py

Purpose:
Read clean sales data from the Silver layer, verify the extracted data,
create business-level sales summaries, and prepare the results
for loading into the Gold layer.
"""

#========================================
# IMPORT REQUIRED LIBRARIES
#========================================

import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

#========================================
# LOAD ENVIRONMENT VARIABLES
#========================================

# Load values from the .env file so database credentials
# do not have to be hardcoded into the Python script.
load_dotenv()

#========================================
# CONNECT TO POSTGRESQL
#========================================

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="retail_dw",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
)

print("Connected to PostgreSQL successfully.")

#========================================
# EXTRACT FROM THE SILVER LAYER
#========================================

query = """
SELECT *
FROM silver.sales_clean;
"""

df = pd.read_sql(query, conn)

#========================================
#VERIFY THE EXTRACTED SILVER DATA
#========================================

#Inspect the silver data before creating
#Gold-Layer summaries.
print(df.head())
print(df.columns)
print(df.dtypes)

#confirm the number of records extracted from silver.
print(f"Rows read from silver: {len(df)}")

#========================================
# TRANSFORM DATA FOR THE GOLD LAYER
#========================================

# Group the Silver sales data by product and calculate
# business-level summary metrics for the Gold layer.
gold_df = df.groupby("product_id").agg(
    total_orders=("order_id", "count"),
    total_quantity=("quantity", "sum"),
    total_sales=("total_amount", "sum")
).reset_index()

#========================================
# VERIFY THE GOLD TRANSFORMATION
#========================================

# Inspect the Gold summary before loading it
# into the Gold layer.
print(gold_df.head())
print(gold_df.columns)
print(gold_df.dtypes)

# Confirm the number of product summary records created.
print(f"Gold summary rows created: {len(gold_df)}")

#========================================
# LOAD DATA INTO THE GOLD LAYER
#========================================

# Create a cursor to execute SQL commands.
cursor = conn.cursor()

# Remove existing Gold summary records before reloading.
# This allows the Gold layer to be rebuilt cleanly.
cursor.execute("DELETE FROM gold.product_sales_summary;")

# SQL statement to insert Gold summary records.
insert_query = """
INSERT INTO gold.product_sales_summary (
    product_id,
    total_orders,
    total_quantity,
    total_sales
)
VALUES (%s, %s, %s, %s);
"""

# Insert each Gold summary row into PostgreSQL.
for _, row in gold_df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["product_id"],
            row["total_orders"],
            row["total_quantity"],
            row["total_sales"]
        )
    )

# Save the inserted records to PostgreSQL.
conn.commit()

#========================================
# VERIFY THE GOLD LOAD
#========================================

# Confirm the number of records loaded into the Gold table.
cursor.execute("SELECT COUNT(*) FROM gold.product_sales_summary;")

count = cursor.fetchone()[0]

expected = len(gold_df)

print(f"Expected Gold rows: {expected}")
print(f"Rows in Gold table: {count}")

if count == expected:
    print("✓ Gold load verification successful.")
else:
    print("✗ Gold load verification failed.")

#========================================
# CLOSE DATABASE CONNECTION
#========================================

# Close the cursor.
cursor.close()

# Close the database connection.
conn.close()

print("Gold ETL pipeline completed successfully.")    