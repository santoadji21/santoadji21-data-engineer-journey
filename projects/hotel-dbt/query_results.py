import duckdb
import pandas as pd

# Connect to the persistent DuckDB file created by dbt
con = duckdb.connect('/app/data/hotel.duckdb')

print("=== 🥉 Bronze Layer (Raw View) ===")
# Note: Bronze is a View, so it reads from Parquet on the fly
try:
    print(con.sql("SELECT * FROM stg_raw_bookings LIMIT 3").df())
except Exception as e:
    print(f"Error reading Bronze: {e}")

print("\n=== 🥈 Silver Layer (Cleaned Table) ===")
try:
    print(con.sql("SELECT source_system, guest_name, amount, check_in_date FROM fact_bookings LIMIT 3").df())
except Exception as e:
    print(f"Error reading Silver: {e}")

print("\n=== 🥇 Gold Layer (Aggregated Stats) ===")
try:
    print(con.sql("SELECT * FROM daily_occupancy").df())
except Exception as e:
    print(f"Error reading Gold: {e}")
