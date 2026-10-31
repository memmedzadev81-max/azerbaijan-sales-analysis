"""
Azərbaycan Satış Datası - SQLite-ə yükləmə
CSV → SQLite pipeline
"""

import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "sales_data.csv"
DB_PATH = BASE_DIR / "data" / "sales.db"

print("CSV oxunur...")
df = pd.read_csv(CSV_PATH)

# Təmizləmə
df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%B")
df["quarter"] = df["order_date"].dt.quarter
df["year_month"] = df["order_date"].dt.strftime("%Y-%m")

# Endirim məbləği
df["discount_amount"] = (df["unit_price"] * df["quantity"] * df["discount"]).round(2)

print(f"Sətir sayı: {len(df)}")
print(f"Regionlar: {df['region'].unique().tolist()}")
print(f"Kateqoriyalar: {df['category'].unique().tolist()}")
print(f"Satış nümayəndələri: {df['salesperson'].unique().tolist()}")

# SQLite
conn = sqlite3.connect(DB_PATH)
conn.execute("DROP TABLE IF EXISTS sales")
df.to_sql("sales", conn, index=False, if_exists="replace")

conn.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON sales(order_date)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_region ON sales(region)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON sales(category)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_salesperson ON sales(salesperson)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_customer ON sales(customer_id)")

conn.commit()
conn.close()

print(f"\nSQLite hazır → {DB_PATH}")
print("Uğurla tamamlandı!")
