# SQL Mastery Lab

A hands-on learning environment for mastering advanced SQL concepts using PostgreSQL and Jupyter Notebooks — powered by Docker.

## Tech Stack

| Component | Tool |
|-----------|------|
| Database | PostgreSQL 15 |
| Interface | Jupyter Lab (with `jupysql` SQL magic) |
| Admin UI | PgAdmin 4 |
| Dataset | Hotel Booking Demand (~119k rows) |

## Getting Started

```bash
# Start all services (Postgres, Jupyter, PgAdmin)
make up

# Rebuild Jupyter image after changing requirements.txt
make build

# Stop services
make down

# Stop services and delete all data
make clean
```

| Service | URL | Credentials |
|---------|-----|-------------|
| Jupyter Lab | [http://localhost:8888](http://localhost:8888) | No password |
| PgAdmin | [http://localhost:5050](http://localhost:5050) | `admin@admin.com` / `password` |
| Postgres | `localhost:5432` | `admin` / `password` / `mastery_db` |

## Notebooks

Work through these in order. Each notebook builds on concepts from the previous one.

| # | Notebook | Topics |
|---|----------|--------|
| 01 | [Setup & Data Exploration](notebooks/01_setup.ipynb) | Connect to Postgres, load CSV, schema inspection, NULL checks, basic analytics |
| 02 | [Window Functions](notebooks/02_window_functions.ipynb) | ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD, running totals, moving averages, NTILE |
| 03 | [Performance Tuning](notebooks/03_performance_tuning.ipynb) | EXPLAIN ANALYZE, Seq Scan vs Index Scan, B-Tree indexes, composite indexes, monitoring |
| 04 | [Complex Aggregations](notebooks/04_complex_aggregations.ipynb) | GROUPING SETS, ROLLUP, CUBE, FILTER clause, CTEs for multi-step analysis |

Each notebook includes:
- Clear learning objectives
- Explained examples with real business questions
- Observation notes on what to look for
- Practice exercises with hints

## Dataset Columns

The `hotel_bookings` table has 36 columns. Key columns used across notebooks:

- `hotel` — Resort Hotel / City Hotel
- `is_canceled` — 1 = canceled, 0 = kept
- `lead_time` — Days between booking and arrival
- `arrival_date_year`, `arrival_date_month` — When the guest arrives
- `adr` — Average Daily Rate (revenue per room-night)
- `country` — Guest's country of origin
- `market_segment` — How the booking was made (Online TA, Direct, etc.)
- `customer_type` — Transient, Contract, Group, Transient-Party
- `deposit_type` — No Deposit, Non Refund, Refundable
- `agent` — Travel agent ID (NULL if direct)
