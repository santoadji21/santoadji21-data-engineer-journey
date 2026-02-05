# Data Model Architecture 🏗️

Documentation for the data models used across learning phases.

## Phase 1: Simple Star Schema (Hotel Bookings)

### Current Implementation (Learning)
A denormalized table for initial SQL practice:

```
bookings (flat table)
├── booking_id
├── hotel_name
├── room_type
├── check_in
├── check_out
├── stay_nights
├── price_per_night
├── total_revenue
└── status
```

### Target Model (Star Schema)

#### Fact Table: `fact_bookings`
```sql
CREATE TABLE fact_bookings (
    booking_id VARCHAR PRIMARY KEY,
    hotel_id INT REFERENCES dim_hotels(hotel_id),
    room_type_id INT REFERENCES dim_room_types(room_type_id),
    guest_id INT REFERENCES dim_guests(guest_id),
    date_id INT REFERENCES dim_date(date_id),
    check_in_date DATE,
    check_out_date DATE,
    stay_nights INT,
    price_per_night DECIMAL(10,2),
    total_revenue DECIMAL(10,2),
    booking_status_id INT
);
```

#### Dimension Tables

**dim_hotels**
```sql
CREATE TABLE dim_hotels (
    hotel_id INT PRIMARY KEY,
    hotel_name VARCHAR,
    city VARCHAR,
    country VARCHAR,
    total_rooms INT,
    star_rating INT,
    created_at TIMESTAMP
);
```

**dim_room_types**
```sql
CREATE TABLE dim_room_types (
    room_type_id INT PRIMARY KEY,
    room_type_name VARCHAR,  -- Standard, Deluxe, Suite
    max_occupancy INT,
    base_price DECIMAL(10,2)
);
```

**dim_guests** (SCD Type 2 for historical tracking)
```sql
CREATE TABLE dim_guests (
    guest_id INT PRIMARY KEY,
    guest_name VARCHAR,
    email VARCHAR,
    loyalty_tier VARCHAR,
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);
```

**dim_date** (Time dimension)
```sql
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    date DATE,
    day_of_week VARCHAR,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    month INT,
    quarter INT,
    year INT
);
```

### Why Star Schema?

| Benefit | Explanation |
|---------|-------------|
| **Query Performance** | Fewer joins, denormalized dimensions |
| **BI Tool Friendly** | Easy for visualization tools to understand |
| **Business Clarity** | Metrics (fact) and context (dimensions) are clear |
| **Scalability** | Can add dimensions without changing fact table |

## Phase 2: Medallion Architecture

### Bronze Layer (Raw)
```
projects/phase2-infrastructure/data/bronze/
├── api_bookings/          # Raw JSON from OTA APIs
├── pms_exports/           # CSV dumps from PMS
└── event_logs/            # Raw event streams
```

### Silver Layer (Cleaned)
```
projects/phase2-infrastructure/data/silver/
├── bookings_cleaned/      # Deduplicated, type-cast
├── guests_normalized/     # Standardized guest data
└── events_enriched/       # Parsed and enriched
```

### Gold Layer (Business Logic)
```
projects/phase2-infrastructure/data/gold/
├── fact_bookings/         # Star schema fact table
├── dim_*/                 # Dimension tables
└── agg_daily_metrics/     # Pre-aggregated metrics
```

## Phase 3: Real-Time Additions

### Streaming Tables
- **Kafka Topics:** `bookings.created`, `bookings.cancelled`, `price.changed`
- **Processing:** Windowed aggregations in Spark Structured Streaming
- **Storage:** Append to existing fact tables with late-arriving data handling

## Data Quality Rules

### Fact Table Constraints
```sql
-- No negative values
CHECK (price_per_night >= 0)
CHECK (total_revenue >= 0)
CHECK (stay_nights > 0)

-- Referential integrity
FOREIGN KEY (hotel_id) REFERENCES dim_hotels(hotel_id)

-- Date logic
CHECK (check_out_date > check_in_date)
```

### Testing (dbt Tests)
- Unique `booking_id`
- Not null `hotel_id`, `check_in_date`
- Accepted values for `status` (Checked-In, Cancelled, No-Show)
- Relationships to dimension tables

---

## Evolution Path

1. **Phase 1:** Flat table for SQL learning ✅
2. **Phase 2:** Star schema with dbt transformations
3. **Phase 3:** Streaming updates with Kafka
4. **Phase 4:** Production-ready with data quality monitoring

---

*This model will evolve as you progress through the phases.*
