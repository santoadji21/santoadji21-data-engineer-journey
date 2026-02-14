import duckdb
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np

app = FastAPI(title="Hotel Data Lake API")

# Database Connection
# We use an in-memory connection that reads from the Parquet files directly
def get_db_connection():
    con = duckdb.connect(database=':memory:')
    return con

class Booking(BaseModel):
    source_system: Optional[str]
    guest_name: Optional[str]
    check_in_date: Optional[str]
    amount: Optional[float]
    raw_json: Optional[str]

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "hotel-data-api"}

@app.get("/bookings", response_model=List[Booking])
def get_bookings(limit: int = 100):
    """
    Reads raw Parquet files and normalizes the 3 different PMS formats on the fly
    using DuckDB's JSON extraction capabilities.
    """
    con = get_db_connection()
    
    # The Magic Query: Normalizing 3 formats into 1
    query = """
    WITH raw_data AS (
        SELECT * FROM '/app/data/raw/*.parquet'
    )
    SELECT 
        -- Determine Source System
        json_extract_string(raw_data, '$.source') as source_system,
        
        -- Normalize Guest Name (COALESCE tries the first non-null value)
        COALESCE(
            json_extract_string(raw_data, '$.GUEST_NM'),       -- Legacy
            json_extract_string(raw_data, '$.guest.lastName'), -- Modern
            json_extract_string(raw_data, '$.client')          -- Budget
        ) as guest_name,
        
        -- Normalize Check-in Date
        COALESCE(
            json_extract_string(raw_data, '$.ARR_DT'),            -- Legacy (DD/MM/YYYY)
            json_extract_string(raw_data, '$.booking.checkInDate'), -- Modern (ISO)
            json_extract_string(raw_data, '$.start_date')         -- Budget (YYYYMMDD)
        ) as check_in_date,
        
        -- Normalize Amount
        CAST(COALESCE(
            json_extract_string(raw_data, '$.AMT'),
            json_extract_string(raw_data, '$.booking.totalPrice'),
            json_extract_string(raw_data, '$.cost')
        ) AS DOUBLE) as amount,
        
        raw_data as raw_json
        
    FROM raw_data
    ORDER BY ingestion_time DESC
    LIMIT ?
    """
    
    try:
        result = con.execute(query, [limit]).fetchdf()
        # Convert NaN to None for JSON compatibility
        # replace() with np.nan → None properly handles all NaN values for Pydantic
        result = result.replace({np.nan: None})
        return result.to_dict(orient="records")
    except Exception as e:
        # Graceful handling if no data exists yet
        print(f"Error querying data: {e}")
        return []

@app.get("/stats/occupancy")
def get_occupancy_stats():
    con = get_db_connection()
    try:
        query = """
        SELECT 
            json_extract_string(raw_data, '$.source') as source,
            COUNT(*) as total_bookings,
            AVG(CAST(COALESCE(
                json_extract_string(raw_data, '$.AMT'),
                json_extract_string(raw_data, '$.booking.totalPrice'),
                json_extract_string(raw_data, '$.cost')
            ) AS DOUBLE)) as avg_revenue
        FROM '/app/data/raw/*.parquet'
        GROUP BY 1
        """
        result = con.execute(query).fetchdf()
        # Convert NaN to None for JSON compatibility
        result = result.replace({np.nan: None})
        return result.to_dict(orient="records")
    except Exception:
        return {"message": "No data available yet"}

