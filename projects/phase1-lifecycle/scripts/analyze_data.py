import duckdb
import pandas as pd

def run_analysis():
    # Connect to DuckDB (creates a file-based DB)
    con = duckdb.connect(database='data/hotel_analytics.duckdb')
    
    print("--- Loading Data ---")
    # Load CSV directly into DuckDB
    con.execute("CREATE OR REPLACE TABLE bookings AS SELECT * FROM read_csv_auto('data/raw_bookings.csv')")
    
    print("--- Calculating Hospitality Metrics (ADR & Revenue) ---")
    # SQL for ADR (Average Daily Rate) and Total Revenue per Hotel
    query = """
    SELECT 
        hotel_name,
        COUNT(booking_id) as total_bookings,
        SUM(total_revenue) as total_revenue,
        ROUND(AVG(price_per_night), 2) as ADR,
        ROUND(SUM(total_revenue) / SUM(stay_nights), 2) as calculated_ADR
    FROM bookings
    WHERE status = 'Checked-In'
    GROUP BY hotel_name
    ORDER BY total_revenue DESC
    """
    
    result = con.execute(query).df()
    print(result)
    
    print("\n--- Occupancy by Room Type ---")
    query_rooms = """
    SELECT 
        room_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bookings), 2) as percentage
    FROM bookings
    GROUP BY room_type
    """
    print(con.execute(query_rooms).df())

if __name__ == "__main__":
    run_analysis()
