"""
FastAPI application — a lightweight API for hotel booking data.

FastAPI is the modern standard for Data Engineering APIs:
  - Built on Python type hints (automatic validation)
  - Auto-generates Swagger UI docs at /docs
  - Async-ready for high performance
  - Perfect for serving data or triggering ETL jobs

Run with:
    uvicorn ETL.api.main:app --reload --port 8000

Then open:
    http://localhost:8000/docs   ← interactive Swagger UI
"""

from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import duckdb
import json

from .schemas import BookingCreate, BookingResponse, BookingSummary, PipelineStatus

# ============================================================
# App Initialization
# ============================================================
# FastAPI() creates the application instance.
# title, description, version appear in the auto-generated docs.
app = FastAPI(
    title="Hotel Booking ETL API",
    description="API for ingesting, querying, and serving hotel booking data.",
    version="1.0.0",
)

# In-memory storage for demo (in production, use a real database)
bookings_db: list[dict] = []
next_id: int = 1

# Path to the hotel CSV (used by query endpoints)
DATA_DIR = Path(__file__).parent.parent.parent / "notebooks" / "data"
HOTEL_CSV = DATA_DIR / "hotel_booking.csv"


# ============================================================
# Health Check
# ============================================================
# @app.get(path) registers a GET endpoint.
# The function name becomes the operation ID in docs.
@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint — verify the API is running.
    Returns 200 OK with status info.
    """
    return {
        "status": "healthy",
        "data_file_exists": HOTEL_CSV.exists(),
    }


# ============================================================
# POST — Ingest a new booking
# ============================================================
# @app.post(path, response_model=..., status_code=...)
#   response_model : Pydantic model for the response (auto-serialized)
#   status_code    : HTTP status code to return (201 = Created)
@app.post("/bookings", response_model=BookingResponse, status_code=201, tags=["Bookings"])
def create_booking(booking: BookingCreate):
    """
    Ingest a new booking record.

    The `booking` parameter is auto-validated against the BookingCreate schema.
    If validation fails, FastAPI returns a 422 error with details.
    """
    global next_id

    # Build the record with computed fields
    record = {
        "id": next_id,
        **booking.model_dump(),
        # model_dump() converts the Pydantic model to a plain dict
        # ** unpacks the dict into key-value pairs
        "total_revenue": round(booking.adr * booking.total_nights, 2),
        # Convert date to string for JSON storage
        "arrival_date": booking.arrival_date,
    }

    bookings_db.append(record)
    next_id += 1

    return record


# ============================================================
# GET — Retrieve bookings
# ============================================================
@app.get("/bookings", response_model=list[BookingResponse], tags=["Bookings"])
def list_bookings(
    # Query() parameters become URL query strings: /bookings?hotel=City+Hotel&limit=10
    hotel: str | None = Query(default=None, description="Filter by hotel type"),
    country: str | None = Query(default=None, description="Filter by country code"),
    limit: int = Query(default=50, ge=1, le=500, description="Max results to return"),
):
    """
    List ingested bookings with optional filters.

    Query parameters:
      - hotel: filter by hotel type (e.g. "City Hotel")
      - country: filter by country code (e.g. "PRT")
      - limit: max number of results (default 50)
    """
    results = bookings_db

    # Apply filters
    if hotel:
        results = [b for b in results if b["hotel"] == hotel]
    if country:
        results = [b for b in results if b["country"] == country]

    return results[:limit]


# ============================================================
# GET — Query hotel CSV with DuckDB
# ============================================================
@app.get("/analytics/summary", response_model=BookingSummary, tags=["Analytics"])
def get_booking_summary(
    hotel: str | None = Query(default=None, description="Filter by hotel type"),
    year: int | None = Query(default=None, description="Filter by arrival year"),
):
    """
    Get aggregated booking statistics from the hotel CSV dataset.

    Uses DuckDB to run SQL directly on the CSV file — no pre-loading needed.
    """
    if not HOTEL_CSV.exists():
        # HTTPException raises an HTTP error response
        # status_code=404 = Not Found
        raise HTTPException(status_code=404, detail=f"Data file not found: {HOTEL_CSV}")

    # Build dynamic WHERE clause
    conditions = ["is_canceled = 0", "adr > 0"]
    if hotel:
        conditions.append(f"hotel = '{hotel}'")
    if year:
        conditions.append(f"arrival_date_year = {year}")

    where_clause = " AND ".join(conditions)

    # Run SQL with DuckDB
    # duckdb.sql() runs a query without a persistent connection (in-memory)
    result = duckdb.sql(f"""
        SELECT
            COUNT(*) AS total_bookings,
            ROUND(SUM(adr * (stays_in_weekend_nights + stays_in_week_nights)), 2) AS total_revenue,
            ROUND(AVG(adr), 2) AS avg_adr
        FROM read_csv_auto('{HOTEL_CSV}')
        WHERE {where_clause}
    """).fetchone()
    # fetchone() returns a single tuple: (total_bookings, total_revenue, avg_adr)

    # Top 5 countries
    top_countries = duckdb.sql(f"""
        SELECT country, COUNT(*) AS count
        FROM read_csv_auto('{HOTEL_CSV}')
        WHERE {where_clause}
        GROUP BY country
        ORDER BY count DESC
        LIMIT 5
    """).fetchall()
    # fetchall() returns a list of tuples

    return BookingSummary(
        total_bookings=result[0],
        total_revenue=result[1],
        avg_adr=result[2],
        top_countries=[{"country": r[0], "count": r[1]} for r in top_countries],
    )


# ============================================================
# POST — Trigger the ETL pipeline
# ============================================================
@app.post("/pipeline/run", response_model=PipelineStatus, tags=["Pipeline"])
def trigger_pipeline():
    """
    Trigger the ETL pipeline (scrape → clean → load).

    In production, this would call the pipeline script asynchronously
    (e.g., via Celery, Airflow, or a background thread).
    For demo purposes, this imports and runs the pipeline directly.
    """
    try:
        # Import the pipeline module and run it
        from ETL.pipeline import run_pipeline
        result = run_pipeline()
        return PipelineStatus(
            status="success",
            message="Pipeline completed successfully",
            rows_processed=result.get("rows_processed", 0),
            output_file=result.get("output_file"),
        )
    except Exception as e:
        return PipelineStatus(
            status="failed",
            message=str(e),
            rows_processed=0,
        )
