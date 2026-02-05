# Data Engineer Roadmap — Hotel Tech Specialization

## -1. Foundations (Pre-Phase)
- Linux CLI basics (files, permissions, grep/rg, pipes)
- Git essentials (branches, PRs, commits, diffs)
- Python fundamentals for data work
  - Virtual envs, package layout, type hints
  - Testing with pytest
- SQL mastery
  - Joins, window functions, CTEs, grouping sets
  - Query performance basics (EXPLAIN, indexes)

## 0. Domain Fundamentals (Hotel Industry)
- Hotel operations overview
  - Front Office (PMS)
  - Revenue Management
  - Housekeeping
  - Sales & Marketing
  - Finance
- Key hotel metrics
  - ADR (Average Daily Rate)
  - RevPAR
  - Occupancy Rate
  - LOS (Length of Stay)
  - Cancellation Rate
  - No-Show Rate
- Booking channels
  - Direct (Website, Mobile App)
  - OTAs (Booking.com, Agoda, Expedia)
  - GDS (Amadeus, Sabre, Travelport)

---

## 1. Data Sources in Hotel Tech

### Core Systems
- PMS (Property Management System)
  - Reservations
  - Check-in / Check-out
  - Room Inventory
  - Guest Profiles
- CRS (Central Reservation System)
- Channel Manager
- RMS (Revenue Management System)
- POS (Restaurant, Spa, Bar)
- Housekeeping Systems
- Finance / Accounting Systems

### External Sources
- OTA APIs
- Payment Gateways
- Review Platforms (Google Reviews, TripAdvisor)
- Weather APIs
- Event & Holiday Calendars

---

## 2. Data Generation & Collection

- Reservation events
- Rate updates
- Inventory changes
- Guest activity logs
- Payment & invoice events
- Review & rating events

### Techniques
- Webhooks from PMS / Channel Manager
- REST APIs
- Scheduled exports (CSV, SFTP)
- Streaming events (Kafka)

---

## 3. Data Ingestion (Hotel Context)

### Ingestion Patterns
- Batch ingestion (nightly reservations, revenue)
- Near real-time ingestion (bookings, cancellations)
- CDC from transactional databases

### Tools
- Apache Kafka / Confluent
- AWS Kinesis
- Airbyte / Fivetran (OTA, CRM connectors)
- Custom Python ingestion services

---

## 4. Data Storage Design

### Operational Datastores
- PostgreSQL / MySQL (normalized schemas)
- NoSQL for guest sessions & events

### Data Lake
- Raw Zone
  - PMS exports
  - OTA booking snapshots
- Curated Zone
  - Cleaned reservations
  - Normalized guests
- Analytics Zone
  - Aggregated metrics

### Tools
- Amazon S3 / GCS
- Delta Lake / Iceberg

---

## 5. Data Modeling for Hotels

### Core Fact Tables
- `fact_reservations`
- `fact_room_nights`
- `fact_revenue`
- `fact_cancellations`
- `fact_payments`

### Dimension Tables
- `dim_property`
- `dim_room_type`
- `dim_rate_plan`
- `dim_guest`
- `dim_channel`
- `dim_date`

### Modeling Approach
- Star Schema
- Slowly Changing Dimensions (SCD Type 2 for rates & rooms)

---

## 6. Data Warehousing

### Use Cases
- Daily hotel performance reports
- Property-level vs chain-level analytics
- Revenue forecasting inputs

### Tools
- BigQuery / Snowflake / Redshift

---

## 7. Data Processing

### Batch Processing
- Nightly revenue aggregation
- Occupancy calculations
- ADR / RevPAR computation

### Stream Processing
- Real-time booking dashboards
- Rate parity monitoring
- Overbooking alerts

### Tools
- Apache Spark
- Apache Flink
- Kafka Streams

---

## 8. Data Pipelines & Orchestration

### Pipelines
- PMS → Data Lake → Warehouse
- OTA → Normalization → Revenue Tables
- Reviews → Sentiment Aggregates

### Orchestration
- Apache Airflow
- Prefect
- dbt (analytics engineering)

---

## 9. Analytics & BI (Hotel-Specific)

### Dashboards
- Daily Pickup Report
- Pace Report
- Revenue by Channel
- Cancellation & No-Show Trends
- Room Inventory Utilization

### Tools
- Looker
- Power BI
- Tableau
- Superset

---

## 10. Data Quality & Validation

### Hotel-Specific Checks
- No negative room nights
- Reservation dates consistency
- Revenue = rate × nights
- Channel totals match PMS totals

### Tools
- dbt tests
- Great Expectations

---

## 11. Security & Privacy (Hotel Data)

### Sensitive Data
- Guest PII
- Payment data
- Passport / ID data

### Practices
- Tokenization of guest identifiers
- Column-level encryption
- Role-based access (Finance vs Ops)

---

## 12. Data Governance

- Data ownership per system (PMS, RMS, Finance)
- Data lineage for revenue numbers
- Metric definitions (single source of truth)
- Audit-ready reporting

---

## 13. Advanced Hotel Use Cases

- Demand forecasting
- Dynamic pricing inputs
- Guest segmentation
- Personalization & loyalty analytics
- Fraud & chargeback detection

---

## 14. Cloud & Infrastructure

- AWS / GCP
- Data services (Glue, Dataflow)
- Terraform for infra
- Cost optimization (multi-property scale)

---

## 15. Career Focus (Hotel Tech Data Engineer)

### What to Master First
- SQL + Data Modeling
- PMS / OTA domain logic
- Revenue metrics correctness
- Reliable pipelines over fancy tools

### Typical Roles
- Hotel Data Engineer
- Revenue Analytics Engineer
- Hospitality Platform Data Engineer
