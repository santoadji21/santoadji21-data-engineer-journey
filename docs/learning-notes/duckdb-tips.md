# DuckDB Tips & Tricks 🦆

DuckDB is an in-process SQL OLAP database management system. It's perfect for data engineering learning because it's fast, lightweight, and requires zero setup.

## Why DuckDB for Data Engineering?

- **Zero Setup:** No server, no installation hassles
- **Fast:** Columnar storage optimized for analytics
- **SQL:** Full SQL support (CTEs, window functions, etc.)
- **File Formats:** Reads CSV, Parquet, JSON directly
- **Pandas Integration:** Seamless DataFrame interop

## Basic Usage

### Connect to DuckDB

```python
import duckdb

# In-memory database (temporary)
con = duckdb.connect()

# Persistent database (saved to disk)
con = duckdb.connect(database='data/my_analytics.duckdb')
```

### Read CSV Directly

```python
# Query CSV without loading into memory
result = con.execute("""
    SELECT * 
    FROM read_csv_auto('data/bookings.csv')
    WHERE hotel_name = 'Grand Plaza'
""").df()
```

### Create Tables

```python
# Load CSV into a table
con.execute("""
    CREATE TABLE bookings AS 
    SELECT * FROM read_csv_auto('data/bookings.csv')
""")

# Query the table
result = con.execute("SELECT COUNT(*) FROM bookings").fetchone()
```

## Advanced Patterns

### Window Functions

```python
# Rank hotels by revenue
query = """
SELECT 
    hotel_name,
    total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM (
    SELECT 
        hotel_name,
        SUM(total_revenue) as total_revenue
    FROM bookings
    GROUP BY hotel_name
)
"""
con.execute(query).df()
```

### CTEs (Common Table Expressions)

```python
query = """
WITH daily_revenue AS (
    SELECT 
        DATE_TRUNC('day', check_in) as date,
        SUM(total_revenue) as revenue
    FROM bookings
    WHERE status = 'Checked-In'
    GROUP BY DATE_TRUNC('day', check_in)
)
SELECT 
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) as prev_day_revenue
FROM daily_revenue
ORDER BY date
"""
```

### Aggregations with GROUPING SETS

```python
# Multiple grouping levels in one query
query = """
SELECT 
    hotel_name,
    room_type,
    COUNT(*) as bookings,
    SUM(total_revenue) as revenue
FROM bookings
GROUP BY GROUPING SETS (
    (hotel_name, room_type),  -- By hotel and room type
    (hotel_name),             -- By hotel only
    ()                        -- Grand total
)
ORDER BY hotel_name, room_type
"""
```

## DuckDB vs PostgreSQL

| Feature | DuckDB | PostgreSQL |
|---------|--------|------------|
| Setup | None | Server required |
| Use Case | Analytics (OLAP) | Transactional (OLTP) |
| Performance | Faster for reads | Faster for writes |
| Deployment | Embedded | Client-server |

## Export Results

### To CSV
```python
con.execute("""
    COPY (
        SELECT * FROM bookings WHERE hotel_name = 'Grand Plaza'
    ) TO 'output/grand_plaza.csv' (HEADER, DELIMITER ',')
""")
```

### To Parquet
```python
con.execute("""
    COPY bookings TO 'data/bookings.parquet' (FORMAT PARQUET)
""")
```

### To Pandas DataFrame
```python
df = con.execute("SELECT * FROM bookings").df()
```

## Best Practices

1. **Use `read_csv_auto()`** for automatic type inference
2. **Create indexes** on frequently queried columns
3. **Use CTEs** for complex queries (more readable than subqueries)
4. **Leverage Parquet** for better compression and performance
5. **Close connections** when done: `con.close()`

## Useful Links

- [DuckDB Documentation](https://duckdb.org/docs/)
- [DuckDB SQL Introduction](https://duckdb.org/docs/sql/introduction)
- [DuckDB Guides](https://duckdb.org/docs/guides/index)

---

*See also: `/projects/phase1-lifecycle/scripts/analyze_data.py` for working examples*
