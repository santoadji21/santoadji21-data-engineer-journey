# SQL Mastery Lab

A hands-on learning environment for mastering advanced SQL concepts using PostgreSQL, Jupyter Notebooks, and real hotel industry data.

## Tech Stack

| Component | Tool |
|-----------|------|
| Database | PostgreSQL 15 |
| Interface | Jupyter Lab (with `jupysql`) |
| Admin UI | PgAdmin 4 |
| Datasets | Hotel Booking Demand (~119k rows) + Hotel Reservations (~36k rows) |

## Getting Started

```bash
make up      # Start Postgres, Jupyter, PgAdmin
make build   # Rebuild Jupyter image after changing requirements
make down    # Stop services
make clean   # Stop + delete all data (fresh start)
```

| Service | URL | Credentials |
|---------|-----|-------------|
| Jupyter Lab | [http://localhost:8888](http://localhost:8888) | No password |
| PgAdmin | [http://localhost:5050](http://localhost:5050) | `admin@admin.com` / `password` |
| Postgres | `localhost:5432` | `admin` / `password` / `mastery_db` |

## Curriculum

Work through these in order. Each notebook builds on the previous.

### Foundation (Taught with Examples)

| # | Notebook | Topics |
|---|----------|--------|
| 01 | [Setup & Data Exploration](notebooks/01_setup.ipynb) | Connect, load CSV, schema inspection, NULL checks, basic analytics |
| 02 | [Window Functions](notebooks/02_window_functions.ipynb) | ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD, running totals, moving averages, NTILE |
| 03 | [Performance Tuning](notebooks/03_performance_tuning.ipynb) | EXPLAIN ANALYZE, Seq Scan vs Index Scan, B-Tree, composite indexes |
| 04 | [Complex Aggregations](notebooks/04_complex_aggregations.ipynb) | GROUPING SETS, ROLLUP, CUBE, FILTER clause, CTEs |

### Practice (Exercises — You Write the SQL)

| # | Notebook | Topics |
|---|----------|--------|
| 05 | [Hotel Reservation Practice](notebooks/05_hotel_reservation_practice.ipynb) | 20 exercises on the OTA dataset across all skill levels |

### Advanced Course (Hotel-Tech Quizzes with Business Scenarios)

| # | Notebook | Topics | Quizzes |
|---|----------|--------|---------|
| 06 | [JOINs & Multi-Table](notebooks/06_joins_and_multi_table.ipynb) | INNER, LEFT, RIGHT, FULL OUTER, Self JOIN, CROSS JOIN, UNION | 10 |
| 07 | [Subqueries & CTEs](notebooks/07_subqueries_and_ctes.ipynb) | Scalar, correlated, derived tables, ANY/ALL/EXISTS, chained CTEs | 10 |
| 08 | [Functions by Data Type](notebooks/08_functions_by_type.ipynb) | Numeric, DateTime, String, NULL handling | 10 |
| 09 | [Data Analysis Applications](notebooks/09_data_analysis_applications.ipynb) | Pivoting, rolling calcs, dedup, YoY, cohort analysis | 10 |

### Capstone (No Hints)

| # | Notebook | Topics |
|---|----------|--------|
| 10 | [Final Project](notebooks/10_final_project.ipynb) | 4-part business case: Revenue, Cancellations, Cross-System, Guest Intelligence |

## Datasets

### `hotel_bookings` (PMS — 119k rows, 36 columns)
Property Management System data. Key columns: `hotel`, `is_canceled`, `lead_time`, `arrival_date_year/month`, `adr`, `country`, `market_segment`, `customer_type`, `deposit_type`, `reserved_room_type`, `assigned_room_type`, `name`, `email`

### `hotel_reservations` (OTA — 36k rows, 19 columns)
Channel Manager / OTA feed. Key columns: `booking_id`, `lead_time`, `arrival_year/month/date`, `avg_price_per_room`, `room_type_reserved`, `market_segment_type`, `booking_status`
