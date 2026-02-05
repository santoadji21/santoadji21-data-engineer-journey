# Phase 1: The Data Engineering Pivot & Lifecycle (Hotel Tech Edition)

## 🎯 Objectives
- Understand the 5 Stages of the Data Engineering Lifecycle.
- Master analytical SQL (OLAP) and Star Schema modeling for hospitality data.
- Understand how hotel source systems (PMS, CRS, OTAs) generate data.

## 🛠 Tech Stack
- **SQL:** PostgreSQL or DuckDB (Window Functions, CTEs).
- **Python:** Pandas or Polars (Vectorized operations).
- **Storage Concepts:** Object Storage (S3/MinIO) vs. Block Storage.

## 📚 Topics to Cover
### 1. The Data Engineering Lifecycle
**📖 Deep Dive:** [Data Engineering Lifecycle Guide](../docs/learning-notes/data-engineering-lifecycle.md)

- [ ] **Generation:** Evaluating hotel source systems (PMS - Property Management Systems, POS - Point of Sale).
  - Read: [Hotel Source Systems](../docs/learning-notes/hotel-source-systems.md)
- [ ] **Ingestion:** Batch (Nightly audits) vs. Streaming (Real-time booking notifications).
- [ ] **Storage:** Data Lakes for raw logs vs. Data Warehouses for guest profiles.
- [ ] **Transformation:** Calculating hospitality metrics (ADR - Average Daily Rate, RevPAR - Revenue Per Available Room).
  - Read: [Hotel Metrics Explained](../docs/learning-notes/hotel-metrics.md)
- [ ] **Serving:** Making data available for Revenue Management Systems (RMS) or BI.

### 2. Sources of Data (The "Input" Layer)
- [ ] **Hotel DBs (OLTP):** Extracting booking data (CDC - Change Data Capture).
- [ ] **APIs & Webhooks:** Pulling from OTA (Expedia/Booking.com) or Channel Manager APIs.
- [ ] **Logs & IoT:** Smart room sensor data or website clickstreams.

### 3. Data Logic
- [ ] **Analytical SQL:** Window functions (`RANK` for top guests, `LEAD` for stay duration).
- [ ] **Modeling:** `fact_bookings` vs. `dim_guests`, `dim_rooms`, `dim_hotels`.

### 4. Storage & File Formats (Practical Basics)
- [ ] **File formats:** CSV vs Parquet (columnar, compression).
- [ ] **Partitioning:** By date/property to reduce scan costs.
- [ ] **Incremental loads:** Append-only vs upserts.

## 🏗 Small Win Project
- **The Hotel Lifecycle Prototype:**
  1. **Generate:** Use a Python script to simulate "Check-in/Check-out" events.
  2. **Ingest/Store:** Save these events into a local directory as JSON.
  3. **Transform:** Use SQL (DuckDB) to calculate "Daily Occupancy %".
  4. **Serve:** Generate a simple CSV report of occupancy trends.

## 🔗 Free Resources
- [Data Engineering Zoomcamp](https://datatalks.club/courses/data-engineering-zoomcamp.html)
- [Hotel Booking Demand Dataset (Kaggle)](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)
- [Mode SQL Tutorial](https://mode.com/sql-tutorial/)
