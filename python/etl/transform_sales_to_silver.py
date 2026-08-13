import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="retail_dw",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
)

print("Connected to PostgreSQL successfully.")

query = """
SELECT *
FROM bronze.sales_raw;
"""

df = pd.read_sql(query, conn)

print(df.head())
print(f"Rows read from Bronze: {len(df)}")

conn.close()