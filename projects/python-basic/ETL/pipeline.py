"""
ETL Pipeline — The "Glue" Script

Orchestrates the full ETL flow:
  1. EXTRACT  → Scrape quotes from the web (or load existing data)
  2. TRANSFORM → Clean & enrich data with Pandas
  3. LOAD     → Save to DuckDB persistent database + Parquet file

This is a simple sequential pipeline. In production, you'd use
Airflow, Prefect, or Dagster to orchestrate tasks with retries,
scheduling, and monitoring.

Usage:
    python -m ETL.pipeline
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import duckdb

# ============================================================
# Setup
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("etl_pipeline")

# Project paths
ETL_DIR = Path(__file__).parent
OUTPUT_DIR = ETL_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCRAPER_OUTPUT = ETL_DIR / "scraper" / "output" / "quotes_raw.json"
CLEAN_JSON = OUTPUT_DIR / "quotes_clean.json"
PARQUET_FILE = OUTPUT_DIR / "quotes.parquet"
DB_FILE = OUTPUT_DIR / "quotes.db"


# ============================================================
# STEP 1: EXTRACT — Scrape or load raw data
# ============================================================

def extract(max_pages: int = 5) -> list[dict]:
    """
    Extract raw quote data.

    Strategy:
      - If a recent scrape file exists (< 1 hour old), reuse it
      - Otherwise, run the scraper to fetch fresh data

    Returns:
        List of raw quote dicts
    """
    logger.info("=" * 50)
    logger.info("STEP 1: EXTRACT")
    logger.info("=" * 50)

    # Check if we have a recent scrape file
    if SCRAPER_OUTPUT.exists():
        # .stat().st_mtime returns the last modification time as a timestamp
        age_seconds = time.time() - SCRAPER_OUTPUT.stat().st_mtime
        age_minutes = age_seconds / 60

        if age_minutes < 60:  # less than 1 hour old
            logger.info(f"Using cached data ({age_minutes:.0f} min old): {SCRAPER_OUTPUT}")
            with SCRAPER_OUTPUT.open("r") as f:
                return json.load(f)
                # json.load(file) reads JSON from a file handle (vs json.loads for strings)

    # No recent cache — run the scraper
    logger.info("No recent data found. Running scraper...")
    try:
        from ETL.scraper.quotes_spider import scrape_all_quotes, save_quotes

        quotes = scrape_all_quotes(max_pages=max_pages, delay=1.0)
        save_quotes(quotes, SCRAPER_OUTPUT)
        return quotes
    except Exception as e:
        logger.error(f"Scraper failed: {e}")
        # Fallback: generate sample data for demo purposes
        logger.warning("Using sample fallback data")
        return _generate_sample_data()


def _generate_sample_data() -> list[dict]:
    """Generate sample quotes when scraping is not available."""
    return [
        {
            "text": "\u201cThe world as we have created it is a process of our thinking.\u201d",
            "author": "Albert Einstein",
            "tags": ["change", "deep-thoughts", "thinking", "world"],
            "author_url": None,
        },
        {
            "text": "\u201cIt is our choices that show what we truly are.\u201d",
            "author": "J.K. Rowling",
            "tags": ["abilities", "choices"],
            "author_url": None,
        },
        {
            "text": "\u201cThere are only two ways to live your life.\u201d",
            "author": "Albert Einstein",
            "tags": ["inspirational", "life", "live"],
            "author_url": None,
        },
        {
            "text": "\u201cThe person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.\u201d",
            "author": "Jane Austen",
            "tags": ["aliteracy", "books", "classic", "humor"],
            "author_url": None,
        },
        {
            "text": "\u201cA day without sunshine is like, you know, night.\u201d",
            "author": "Steve Martin",
            "tags": ["humor", "obvious", "simile"],
            "author_url": None,
        },
    ]


# ============================================================
# STEP 2: TRANSFORM — Clean & enrich with Pandas
# ============================================================

def transform(raw_quotes: list[dict]) -> pd.DataFrame:
    """
    Clean and enrich raw quote data.

    Transformations:
      - Remove unicode quote characters from text
      - Count tags per quote
      - Extract first tag as primary category
      - Add text length and word count
      - Add processing timestamp

    Args:
        raw_quotes: list of raw quote dicts from the scraper

    Returns:
        Cleaned Pandas DataFrame
    """
    logger.info("=" * 50)
    logger.info("STEP 2: TRANSFORM")
    logger.info("=" * 50)

    # pd.DataFrame() converts a list of dicts → DataFrame
    df = pd.DataFrame(raw_quotes)
    logger.info(f"Raw records: {len(df)}")

    # --- Clean text: remove unicode quote marks ---
    # str.replace() on a Series applies to every element (vectorized)
    df["text"] = df["text"].str.replace("\u201c", "").str.replace("\u201d", "").str.strip()

    # --- Enrich: add computed columns ---

    # .str.len() returns the length of each string
    df["text_length"] = df["text"].str.len()

    # .str.split().str.len() counts words (split by whitespace, count pieces)
    df["word_count"] = df["text"].str.split().str.len()

    # tags is a list column; .apply(len) counts items in each list
    df["tag_count"] = df["tags"].apply(len)

    # Extract primary tag (first tag, or "untagged" if empty)
    # .apply(lambda) runs a function on each value
    df["primary_tag"] = df["tags"].apply(lambda t: t[0] if t else "untagged")

    # Convert tags list to comma-separated string for storage
    # .str.join() joins list elements (only works on list-type columns)
    df["tags_str"] = df["tags"].apply(lambda t: ", ".join(t))

    # Add processing metadata
    # datetime.now(timezone.utc) gets current UTC time
    df["processed_at"] = datetime.now(timezone.utc).isoformat()

    # --- Remove duplicates by text ---
    before = len(df)
    df = df.drop_duplicates(subset=["text"])
    after = len(df)
    if before > after:
        logger.warning(f"Removed {before - after} duplicate quotes")

    # --- Select and order final columns ---
    df = df[[
        "author", "text", "text_length", "word_count",
        "primary_tag", "tag_count", "tags_str",
        "processed_at",
    ]]

    logger.info(f"Clean records: {len(df)}")
    logger.info(f"Columns: {df.columns.tolist()}")

    return df


# ============================================================
# STEP 3: LOAD — Save to Parquet + DuckDB
# ============================================================

def load(df: pd.DataFrame) -> dict:
    """
    Load cleaned data to persistent storage.

    Outputs:
      1. Parquet file (for data lake / analytics)
      2. DuckDB database (for SQL querying)
      3. Clean JSON (for API consumption)

    Args:
        df: cleaned Pandas DataFrame

    Returns:
        Dict with output file paths and row counts
    """
    logger.info("=" * 50)
    logger.info("STEP 3: LOAD")
    logger.info("=" * 50)

    # --- 3a: Save to Parquet ---
    # to_parquet() writes a DataFrame to Parquet format
    df.to_parquet(PARQUET_FILE, engine="pyarrow", compression="snappy", index=False)
    logger.info(f"Parquet: {PARQUET_FILE} ({PARQUET_FILE.stat().st_size / 1024:.1f} KB)")

    # --- 3b: Save to DuckDB ---
    # duckdb.connect(str(path)) opens/creates a persistent database file
    con = duckdb.connect(str(DB_FILE))

    # Register the DataFrame as a virtual table, then CREATE TABLE from it
    # This copies data into DuckDB's internal columnar format
    con.sql("CREATE OR REPLACE TABLE quotes AS SELECT * FROM df")

    # Verify
    row_count = con.sql("SELECT COUNT(*) FROM quotes").fetchone()[0]
    logger.info(f"DuckDB : {DB_FILE} — {row_count} rows loaded")

    # Create a summary view for quick analytics
    # CREATE VIEW creates a virtual table (query is re-run each time)
    con.sql("""
        CREATE OR REPLACE VIEW author_summary AS
        SELECT
            author,
            COUNT(*) AS quote_count,
            ROUND(AVG(word_count), 1) AS avg_words,
            STRING_AGG(DISTINCT primary_tag, ', ') AS topics
        FROM quotes
        GROUP BY author
        ORDER BY quote_count DESC
    """)
    # STRING_AGG(column, separator) concatenates values with a separator
    # DISTINCT inside STRING_AGG removes duplicates

    logger.info("DuckDB : Created 'author_summary' view")

    # Quick verification query
    logger.info("\n--- Author Summary ---")
    con.sql("SELECT * FROM author_summary LIMIT 5").show()

    con.close()

    # --- 3c: Save clean JSON ---
    # to_json() writes DataFrame to JSON
    #   orient='records' → list of dicts (most common for APIs)
    #   force_ascii=False → allow unicode characters
    df.to_json(CLEAN_JSON, orient="records", indent=2, force_ascii=False)
    logger.info(f"JSON   : {CLEAN_JSON} ({CLEAN_JSON.stat().st_size / 1024:.1f} KB)")

    return {
        "rows_processed": len(df),
        "output_file": str(PARQUET_FILE),
        "parquet_path": str(PARQUET_FILE),
        "duckdb_path": str(DB_FILE),
        "json_path": str(CLEAN_JSON),
    }


# ============================================================
# Pipeline Runner
# ============================================================

def run_pipeline(max_pages: int = 5) -> dict:
    """
    Execute the full ETL pipeline: Extract → Transform → Load.

    Args:
        max_pages: max pages to scrape (default 5)

    Returns:
        Dict with pipeline results and output paths
    """
    start = time.perf_counter()
    logger.info("🚀 Pipeline starting...")

    # E → T → L
    raw_data = extract(max_pages=max_pages)
    clean_df = transform(raw_data)
    result = load(clean_df)

    elapsed = time.perf_counter() - start
    logger.info(f"\n✅ Pipeline completed in {elapsed:.2f}s")
    logger.info(f"   Rows processed: {result['rows_processed']}")
    logger.info(f"   Parquet: {result['parquet_path']}")
    logger.info(f"   DuckDB : {result['duckdb_path']}")
    logger.info(f"   JSON   : {result['json_path']}")

    return result


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    run_pipeline()
