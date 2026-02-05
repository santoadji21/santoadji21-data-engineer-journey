# The Data Engineering Lifecycle 🔄

A deep dive into the 5 stages of data engineering, with hotel tech examples.

## Overview

The Data Engineering Lifecycle consists of 5 key stages:

```
Generation → Ingestion → Storage → Transformation → Serving
```

Each stage has unique challenges, tools, and considerations. Let's explore each in the context of hotel technology.

---

## 1. Generation 📊

**Definition:** Where data originates from source systems.

### Hotel Source Systems

#### PMS (Property Management System)
The central brain of hotel operations.

**What it generates:**
- **Reservations:** Guest bookings, room assignments, stay dates
- **Check-ins/Check-outs:** Real-time arrival and departure events
- **Guest Profiles:** Contact info, preferences, loyalty status
- **Room Status:** Clean, dirty, occupied, vacant, maintenance
- **Folios:** Itemized billing and charges

**Examples:** Opera (Oracle), Protel, Cloudbeds, Mews

**Data Characteristics:**
- **Volume:** Medium (100-1000 transactions/day per property)
- **Velocity:** Real-time for check-ins, batch for night audit
- **Schema:** Highly structured (relational database)
- **Late-Arriving Data:** Rare, but manual corrections happen

#### POS (Point of Sale)
Tracks all revenue-generating transactions.

**What it generates:**
- Restaurant orders and payments
- Bar/minibar purchases
- Spa bookings and charges
- Gift shop sales

**Data Characteristics:**
- **Volume:** High during peak hours (breakfast, dinner)
- **Velocity:** Real-time transaction streams
- **Schema:** Semi-structured (transaction logs)

#### CRS (Central Reservation System)
Manages bookings across multiple properties.

**What it generates:**
- Multi-property availability
- Rate plans and pricing rules
- Channel distribution (OTA sync)

#### Other Sources
- **Channel Manager:** Booking.com, Expedia API data
- **Revenue Management System (RMS):** Pricing recommendations
- **IoT Sensors:** Smart thermostats, door locks, occupancy sensors
- **Website Analytics:** Clickstream, funnel drop-offs

### Key Considerations for Generation

#### Rate of Data
**Question:** How often is data produced?

| System | Rate | Example |
|--------|------|---------|
| PMS Check-in | Per event | 3 PM check-in spike |
| Night Audit | Daily batch | Midnight reconciliation |
| IoT Sensors | Continuous | Temperature every 5 seconds |
| API Webhooks | Event-driven | OTA booking notification |

#### Schema Consistency
**Question:** Does the data structure change?

- **Stable:** PMS guest profiles (decades-old schemas)
- **Evolving:** OTA APIs (version updates quarterly)
- **Chaotic:** Log files (unstructured text)

**Impact on DE:**
- Stable schemas → Simple pipelines
- Evolving schemas → Schema evolution handling (Avro, Protobuf)
- Chaotic → Complex parsing logic

#### Late-Arriving Data
**Question:** Can data arrive out of order?

**Hotel Example:**
- Guest checks out at 11 AM
- Minibar charges discovered at 2 PM during room inspection
- Data arrives 3 hours late → Must backfill the folio

**Solution:** Use event timestamps (not processing timestamps)

---

## 2. Ingestion 🔄

**Definition:** Moving data from source systems into your data platform.

### Batch Ingestion
**Characteristics:** Periodic, scheduled, full or incremental loads

#### Hotel Use Cases

**Night Audit (Daily Batch)**
```python
# Pseudocode: Daily PMS export
schedule: 00:30 daily
source: PMS database
method: Full table dump → CSV
destination: S3 bucket
volume: 1-10 MB/property
```

**Monthly Financial Close**
```python
schedule: 1st of month
source: Accounting system
method: Incremental (last 30 days)
format: Parquet
```

**Advantages:**
- ✅ Simple to implement
- ✅ Predictable resource usage
- ✅ Easy to retry failures

**Disadvantages:**
- ❌ Data latency (hours to days)
- ❌ Not suitable for real-time analytics

### Streaming Ingestion
**Characteristics:** Continuous, real-time, event-driven

#### Hotel Use Cases

**Real-Time Booking Notifications**
```python
source: OTA webhooks (Booking.com API)
method: HTTP POST → Kafka topic
latency: < 1 second
use_case: Inventory updates, revenue alerts
```

**IoT Sensor Data**
```python
source: Smart room devices
protocol: MQTT
frequency: Every 5 seconds
volume: 17,280 events/day/room
```

**Website Clickstream**
```python
source: Next.js frontend
method: Browser events → Kafka
use_case: Real-time funnel analysis
```

**Advantages:**
- ✅ Low latency (seconds)
- ✅ Enables real-time dashboards
- ✅ Event-driven architecture

**Disadvantages:**
- ❌ Complex to implement
- ❌ Higher infrastructure costs
- ❌ Harder to debug

### Batch vs. Streaming Decision Matrix

| Scenario | Choose Batch | Choose Streaming |
|----------|--------------|------------------|
| **Night Audit** | ✅ Once per day is sufficient | ❌ Overkill |
| **Revenue Dashboard** | ✅ Hourly updates OK | ✅ Real-time preferred |
| **Dynamic Pricing** | ❌ Too slow | ✅ Needs < 1 min latency |
| **Compliance Reporting** | ✅ Historical analysis | ❌ Not needed |
| **Fraud Detection** | ❌ Too slow | ✅ Must be real-time |

### Ingestion Patterns

#### Full Load
```sql
-- Export entire table
SELECT * FROM pms.reservations
```
**When:** Small tables, first-time load

#### Incremental Load
```sql
-- Only new/updated records
SELECT * FROM pms.reservations
WHERE updated_at > '2026-01-28 00:00:00'
```
**When:** Large tables, daily updates

#### CDC (Change Data Capture)
```python
# Capture database log events
INSERT → Kafka topic "reservations.created"
UPDATE → Kafka topic "reservations.updated"
DELETE → Kafka topic "reservations.deleted"
```
**When:** Real-time sync, minimal database impact

**Tools:**
- **Batch:** Airflow, dbt, cron jobs
- **Streaming:** Kafka, Kinesis, Pub/Sub, Debezium (CDC)

---

## 3. Storage 💾

**Definition:** Where you persist data for analysis.

### Data Lake (Unstructured)
**What:** Store raw files in object storage

**Hotel Example:**
```
s3://hotel-data-lake/
├── bronze/
│   ├── pms_exports/
│   │   └── 2026-01-29-reservations.csv
│   ├── api_logs/
│   │   └── booking_com_webhooks.json
│   └── iot_events/
│       └── room_sensors.parquet
```

**Advantages:**
- ✅ Cheap storage (S3: $0.023/GB/month)
- ✅ Store any format (CSV, JSON, Parquet)
- ✅ Schema-on-read (define schema later)

**Disadvantages:**
- ❌ Slow queries (scan entire files)
- ❌ No ACID transactions
- ❌ Can become a "data swamp" without governance

**Use Cases:**
- Raw backups
- Log archives
- ML training data

### Data Warehouse (Structured)
**What:** Optimized for analytical SQL queries

**Hotel Example:**
```sql
-- Star schema in Snowflake/BigQuery
fact_bookings (200M rows)
├── hotel_id → dim_hotels
├── room_type_id → dim_room_types
├── guest_id → dim_guests
└── date_id → dim_date
```

**Advantages:**
- ✅ Fast queries (columnar storage)
- ✅ SQL-friendly (BI tools love it)
- ✅ Schema enforcement (data quality)

**Disadvantages:**
- ❌ More expensive ($5-$50 per TB scanned)
- ❌ Schema must be defined upfront
- ❌ Not ideal for unstructured data

**Use Cases:**
- BI dashboards
- Revenue reports
- Guest analytics

### Medallion Architecture (Best of Both Worlds)

```
Bronze (Raw)           Silver (Cleaned)       Gold (Business Logic)
└── Data Lake          └── Data Lake          └── Data Warehouse
    CSV, JSON              Parquet                Star Schema
    As-is data             Deduplicated           Aggregated metrics
    Keep everything        Type-cast              ADR, RevPAR
```

**Example Flow:**
```
1. PMS CSV → S3 bronze/           (Data Lake)
2. Clean + Parquet → S3 silver/   (Data Lake)
3. Aggregate → Snowflake gold/    (Data Warehouse)
```

---

## 4. Transformation 🔧

**Definition:** Converting raw data into business value.

### Types of Transformations

#### Cleaning
```python
# Remove duplicates
df.drop_duplicates(subset=['booking_id'])

# Handle nulls
df['email'].fillna('unknown@hotel.com')

# Fix data types
df['check_in'] = pd.to_datetime(df['check_in'])
```

#### Enrichment
```sql
-- Add calculated fields
SELECT 
    *,
    DATEDIFF(day, check_in, check_out) as stay_nights,
    price_per_night * stay_nights as total_revenue
FROM raw_bookings
```

#### Aggregation
```sql
-- Calculate hotel-level metrics
SELECT 
    hotel_name,
    DATE_TRUNC('day', check_in) as date,
    COUNT(*) as bookings,
    SUM(total_revenue) as daily_revenue,
    AVG(price_per_night) as ADR
FROM bookings
GROUP BY hotel_name, DATE_TRUNC('day', check_in)
```

#### Joining (Denormalization)
```sql
-- Create wide table for BI
SELECT 
    b.booking_id,
    h.hotel_name,
    h.city,
    g.guest_name,
    g.loyalty_tier,
    b.total_revenue
FROM bookings b
JOIN hotels h ON b.hotel_id = h.id
JOIN guests g ON b.guest_id = g.id
```

### Hotel-Specific Transformations

#### Calculate ADR (Average Daily Rate)
```sql
SELECT 
    hotel_name,
    ROUND(AVG(price_per_night), 2) as ADR
FROM bookings
WHERE status = 'Checked-In'
GROUP BY hotel_name
```

#### Calculate RevPAR (Revenue Per Available Room)
```sql
-- Assuming 100 rooms per hotel
SELECT 
    hotel_name,
    SUM(total_revenue) / (100 * COUNT(DISTINCT date)) as RevPAR
FROM daily_bookings
GROUP BY hotel_name
```

#### Occupancy Rate
```sql
SELECT 
    DATE_TRUNC('day', check_in) as date,
    COUNT(*) as rooms_sold,
    100 as available_rooms,
    ROUND(COUNT(*) * 100.0 / 100, 2) as occupancy_pct
FROM bookings
WHERE status = 'Checked-In'
GROUP BY date
```

### Transformation Tools

| Tool | Best For | Example |
|------|----------|---------|
| **SQL** | Simple aggregations | dbt, Snowflake |
| **Python (Pandas)** | Complex logic | Airflow tasks |
| **Spark** | Big Data (>1TB) | PySpark on Databricks |

---

## 5. Serving 🍽️

**Definition:** Making data accessible to end users and systems.

### Serving Patterns

#### Analytics (BI Dashboards)
**Consumers:** Revenue managers, hotel executives

**Tools:**
- Tableau, Looker, Power BI
- Apache Superset (open-source)
- Custom Next.js dashboard

**Data Model:** Star schema, aggregated tables

**Example:**
```sql
-- Pre-aggregated table for fast dashboards
CREATE TABLE agg_daily_metrics AS
SELECT 
    date,
    hotel_name,
    SUM(revenue) as total_revenue,
    AVG(adr) as avg_adr,
    AVG(occupancy) as avg_occupancy
FROM gold.fact_bookings
GROUP BY date, hotel_name
```

#### Machine Learning
**Use Cases:**
- Demand forecasting
- Dynamic pricing
- Guest churn prediction
- Sentiment analysis (reviews)

**Data Model:** Feature tables (wide, denormalized)

**Example:**
```python
# Feature table for demand forecasting
features = [
    'day_of_week',
    'is_holiday',
    'days_until_checkin',
    'historical_occupancy_7d',
    'competitor_avg_price',
    'local_event_flag'
]
```

#### Reverse ETL
**Definition:** Send warehouse data back to operational systems

**Hotel Example:**
```
Snowflake → Salesforce
├── High-value guest segments
└── Churn risk scores

Snowflake → Email Marketing
└── Personalized offer campaigns
```

**Tools:** Census, Hightouch, Fivetran Reverse ETL

#### APIs
**Use Cases:**
- Mobile app backend
- Third-party integrations
- Real-time availability checks

**Example:**
```python
# FastAPI endpoint
@app.get("/api/hotels/{hotel_id}/availability")
def get_availability(hotel_id: int, date: str):
    return db.query(f"""
        SELECT room_type, available_count
        FROM availability
        WHERE hotel_id = {hotel_id}
        AND date = '{date}'
    """)
```

---

## Putting It All Together: Hotel Booking Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ GENERATION                                                  │
│ PMS creates booking → Event: "Reservation Created"         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ INGESTION                                                   │
│ Webhook → Kafka topic → Stream processor                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ STORAGE                                                     │
│ Raw JSON → S3 Bronze                                        │
│ Cleaned Parquet → S3 Silver                                 │
│ Star Schema → Snowflake Gold                                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ TRANSFORMATION                                              │
│ dbt model: Calculate ADR, RevPAR, Occupancy                │
│ Aggregate: Daily hotel metrics                             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ SERVING                                                     │
│ Tableau Dashboard → Revenue Management Team                │
│ ML Model → Dynamic Pricing Engine                          │
│ API → Mobile App (Guest Loyalty Points)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Further Reading

- **Generation:** [docs/learning-notes/hotel-source-systems.md](hotel-source-systems.md)
- **Storage:** [docs/architecture/data-model.md](../architecture/data-model.md)
- **Transformation:** [docs/learning-notes/hotel-metrics.md](hotel-metrics.md)
- **Tools:** [docs/learning-notes/duckdb-tips.md](duckdb-tips.md)

---

*This is Phase 1 foundational knowledge. You'll implement these concepts hands-on throughout the 4 phases.*
