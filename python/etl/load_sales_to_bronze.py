import pandas as pd
import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / "data" / "raw" / "sales.csv"

df = pd.read_csv(CSV_FILE)

print(df.head())

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="retail_dw",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
)

print("Connected to PostgreSQL successfully.")

cursor = conn.cursor()

cursor.execute(
    "DELETE FROM bronze.sales_raw WHERE source_file = %s;",
    (CSV_FILE.name,)
)

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

conn.commit()

print(f"Successfully loaded {len(df)} rows into bronze.sales_raw.")

cursor.close()
conn.close()   

