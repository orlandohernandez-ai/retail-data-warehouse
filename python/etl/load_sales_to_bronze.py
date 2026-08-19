# ============================================================
# Bronze ETL Pipeline
# ============================================================
#
# Purpose:
# Extract raw retail sales data from a CSV file and load it
# into the Bronze layer without modifying the original data.
#
# Pipeline:
# Extract
# Verify
# Load
# Verify
#
# The Bronze layer preserves the raw source data and serves
# as the system of record for rebuilding downstream layers.
# ============================================================

import pandas as pd
import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv

# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

# Load environment variables from the .env file.
# This keeps sensitive information, such as passwords,
# out of the source code.
load_dotenv()

# ============================================
# LOCATE THE SOURCE DATA FILE
# ============================================

# Determine the project root directory.
BASE_DIR = Path(__file__).resolve().parents[2]

# Build the path to the raw sales CSV file.
CSV_FILE = BASE_DIR / "data" / "raw" / "sales.csv"

# ============================================
# EXTRACT DATA FROM THE CSV FILE
# ============================================

# Read the raw sales data into a Pandas DataFrame.
df = pd.read_csv(CSV_FILE)

# ============================================
# VERIFY THE EXTRACT
# ============================================

# Display the first few records to confirm
# the CSV file was loaded successfully.
print(df.head())

# Confirm the number of records extracted.
print(f"Rows extracted: {len(df)}")

# ============================================
# CONNECT TO POSTGRESQL
# ============================================

# Establish a connection to the PostgreSQL database.
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="retail_dw",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
)

# Confirm that the database connection was established.
print("Connected to PostgreSQL successfully.")

# ============================================
# LOAD DATA INTO THE BRONZE LAYER
# ============================================

# Create a cursor to execute SQL commands.
cursor = conn.cursor()

# Remove any previously loaded records from this source file.
# This prevents duplicate data when rerunning the pipeline.
cursor.execute(
    "DELETE FROM bronze.sales_raw WHERE source_file = %s;",
    (CSV_FILE.name,)
)

# SQL statement used to insert raw records into the Bronze table.
insert_query = """
INSERT INTO bronze.sales_raw (
    order_id,
    order_date,
    customer_id,
    product_id,
    quantity,
    unit_price,
    store_id,
    source_file
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

# Insert each row from the DataFrame into PostgreSQL.
for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["order_id"],
            row["order_date"],
            row["customer_id"],
            row["product_id"],
            row["quantity"],
            row["unit_price"],
            row["store_id"],
            CSV_FILE.name
        )
    )

# Save all inserted records.
conn.commit()

# ============================================
# VERIFY THE LOAD
# ============================================

# Confirm the number of records loaded into Bronze.
cursor.execute("SELECT COUNT(*) FROM bronze.sales_raw")

count = cursor.fetchone()[0]

print(f"Expected rows: {len(df)}")
print(f"Rows in Bronze table: {count}")

if count == len(df):
    print("✓ Load verification successful.")
else:
    print("✗ Load verification failed.")

# ============================================
# CLOSE DATABASE CONNECTION
# ============================================

# Close the cursor.
cursor.close()

# Close the database connection.
conn.close()

print("Bronze ETL pipeline completed successfully.")