# Phase 1: Hotel Booking Lifecycle

Learn the **5 stages of the Data Engineering Lifecycle** using hotel booking data.

## 🎯 Objectives

- Understand the data engineering lifecycle (Generation → Ingestion → Storage → Transformation → Serving)
- Master analytical SQL with DuckDB
- Calculate hotel-specific metrics (ADR, RevPAR, Occupancy)

## 📊 Project Structure

```
phase1-lifecycle/
├── data/               # Raw and processed data files
├── scripts/            # Python scripts for generation and analysis
├── notebooks/          # Jupyter notebooks (future)
└── README.md           # This file
```

## 🚀 How to Run

### Generate Sample Hotel Booking Data

```bash
cd projects/phase1-lifecycle
python scripts/generate_data.py
```

This creates `data/raw_bookings.csv` with 500 simulated hotel bookings.

### Analyze with DuckDB

```bash
python scripts/analyze_data.py
```

This runs analytical SQL queries to calculate:
- **ADR (Average Daily Rate)** per hotel
- **Total Revenue** by hotel
- **Occupancy distribution** by room type

## 🏨 Data Schema

| Column | Description |
|--------|-------------|
| `booking_id` | Unique booking identifier |
| `hotel_name` | Hotel property name |
| `room_type` | Standard, Deluxe, or Suite |
| `check_in` | Check-in date |
| `check_out` | Check-out date |
| `stay_nights` | Number of nights stayed |
| `price_per_night` | Nightly rate |
| `total_revenue` | Total booking revenue |
| `status` | Checked-In, Cancelled, or No-Show |

## 📚 Concepts Covered

- [x] Data Generation (simulating PMS data)
- [x] Data Storage (CSV as object storage)
- [x] SQL Transformation (aggregations, filtering)
- [ ] Window Functions (`RANK`, `LEAD`)
- [ ] Star Schema modeling (`fact_bookings`, `dim_hotels`)
- [ ] Data Export for serving

## 🔗 Related Learning

- See `/docs/learning-notes/` for SQL tips and hotel metrics explanations
- See `/plans/Phase1_The_Pivot.md` for the full learning plan
