"""
Project: Retail Data Warehouse
Layer: Silver
File: transform_sales_to_silver.py

Purpose:
Read data from the Bronze layer, verify the extracted data, 
apply Silver-layer transformations, and prepare the data
for loading into the Silver layer.
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

#Load values from the .env file so database credentials
#do not have to be hardcoded into the python script
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
# EXTRACT FROM THE BRONZE LAYER
#========================================

query = """
SELECT *
FROM bronze.sales_raw;
"""

df = pd.read_sql(query, conn)

#========================================
# VERIFY THE EXTRACTED BRONZE DATA
#========================================

# Inspect the data before transforming it to confirm
# the expected rows, columns, and data types were loaded.
print(df.head())
print(df.columns)
print(df.dtypes)

# Confirm the expected number of records were extracted.
print(f"Rows read from Bronze: {len(df)}")

#========================================
# TRANSFORM DATA FOR THE SILVER LAYER
#========================================

# Convert order_date from text to a datetime object.
df["order_date"] = pd.to_datetime(df["order_date"])

# Create a calculated field representing the total sale amount.
df["total_amount"] = df["quantity"] * df["unit_price"]

#========================================
# VERIFY THE TRANSFORMATION
#========================================

# Confirm the transformed data before loading it into
# the silver layer.
print(df.head())
print(df.dtypes)
df.info()

#========================================
# LOAD DATA INTO THE SILVER LAYER
#========================================

#Create a cursor to executeSQL commands.
cursor = conn.cursor()

# SQL statement to insert transformed records into the silver table.
insert_query = """
INSERT INTO silver.sales_clean (
    order_id,
    order_date,
    customer_id,
    product_id,
    quantity,
    unit_price,
    store_id,
    total_amount,
    source_file,
    load_timestamp
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    cursor.execute(insert_query, (
    row["order_id"],
    row["order_date"],
    row["customer_id"],
    row["product_id"],
    row["quantity"],
    row["unit_price"],
    row["store_id"],
    row["total_amount"],
    row["source_file"],
    row["load_timestamp"]
))

# Save the inserted records to PostgreSQL.
conn.commit()

# ============================================
# VERIFY THE LOAD
# ============================================

cursor.execute("SELECT COUNT(*) FROM silver.sales_clean")

count = cursor.fetchone()[0]

expected = len(df)

print(f"Expected rows: {expected}")
print(f"Rows in Silver table: {count}")

if count == expected:
    print("✓ Load verification successful.")
else:
    print("✗ Load verification failed.")

# Close the cursor.
cursor.close()

#========================================
# CLOSE DATABASE CONNECTION
#========================================

conn.close()