# Hotel Source Systems Deep Dive 🏨

Understanding where hotel data comes from and how to work with it.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HOTEL TECH ECOSYSTEM                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PMS (Core)    │  │   POS (Revenue) │  │   CRS (Multi)   │
│  Opera, Mews    │  │   Micros, Revel │  │  Synxis, SHR    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                     │
         └────────────────────┼─────────────────────┘
                              │
              ┌───────────────▼───────────────┐
              │    Channel Manager            │
              │    (SiteMinder, RateTiger)    │
              └───────────────┬───────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼─────────┐
│ OTAs            │  │ GDS             │  │ Direct Website  │
│ Booking.com     │  │ Amadeus         │  │ Hotel.com       │
│ Expedia         │  │ Sabre           │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                              │
                              │ Competitor Data
                              │ Market Intelligence
                              ▼
              ┌───────────────────────────────┐
              │   RMS (Revenue Management)    │
              │   RoomPriceGenie, IDeaS       │
              │   → Dynamic Pricing           │
              └───────────────────────────────┘
```

---

## 1. PMS (Property Management System) 🏢

**The Single Source of Truth** for hotel operations.

### What is a PMS?

The PMS is the central database that manages:
- **Reservations:** All bookings from all channels
- **Guest Profiles:** Contact info, preferences, history
- **Room Inventory:** Room types, availability, status
- **Housekeeping:** Clean/dirty room status
- **Front Desk:** Check-in/out, room assignments
- **Billing:** Folios, charges, payments

### Popular PMS Systems

| System | Market | Strengths |
|--------|--------|-----------|
| **Oracle Opera** | Enterprise | Large chains, complex integrations |
| **Mews** | Modern | Cloud-native, API-first |
| **Cloudbeds** | Small/Mid | All-in-one, easy setup |
| **Protel** | Europe | Multilingual, strong in Germany |
| **RoomKey** | Budget | Simple, cost-effective |

### Data Access Methods

#### 1. Database Direct Access (Best)
```python
# Direct PostgreSQL/MySQL connection
import psycopg2
conn = psycopg2.connect(
    host="pms.hotel.com",
    database="opera_prod",
    user="readonly_user",
    password="secret"
)

# Query reservations
query = """
SELECT 
    reservation_id,
    guest_name,
    check_in,
    check_out,
    room_number,
    rate
FROM reservations
WHERE check_in >= CURRENT_DATE
"""
df = pd.read_sql(query, conn)
```

**Pros:**
- ✅ Full access to data
- ✅ Complex queries possible
- ✅ No API rate limits

**Cons:**
- ❌ Requires database credentials
- ❌ Can impact production (use read replicas!)
- ❌ Schema knowledge required

#### 2. REST API (Modern)
```python
# Mews API example
import requests

headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

payload = {
    "StartUtc": "2026-01-01T00:00:00Z",
    "EndUtc": "2026-01-31T23:59:59Z"
}

response = requests.post(
    'https://api.mews.com/api/connector/v1/reservations/getAll',
    json=payload,
    headers=headers
)

reservations = response.json()['Reservations']
```

**Pros:**
- ✅ Safe (no direct DB access)
- ✅ Vendor-supported
- ✅ Webhooks for real-time events

**Cons:**
- ❌ Rate limits (100-1000 req/hour)
- ❌ Limited query flexibility
- ❌ Pagination for large datasets

#### 3. File Export (Legacy)
```python
# Daily CSV export from PMS
import pandas as pd

df = pd.read_csv('ftp://pms.hotel.com/exports/reservations_20260129.csv')
```

**Pros:**
- ✅ Simple to implement
- ✅ No API knowledge needed

**Cons:**
- ❌ Not real-time (daily/hourly)
- ❌ Manual FTP setup
- ❌ CSV parsing issues (encoding, delimiters)

### PMS Data Tables (Typical Schema)

#### reservations
```sql
CREATE TABLE reservations (
    reservation_id INT PRIMARY KEY,
    confirmation_number VARCHAR(20),
    guest_id INT,
    hotel_id INT,
    room_type_id INT,
    check_in DATE,
    check_out DATE,
    adults INT,
    children INT,
    rate_code VARCHAR(10),
    total_amount DECIMAL(10,2),
    status VARCHAR(20),  -- Confirmed, Cancelled, No-Show, Checked-In
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### guests
```sql
CREATE TABLE guests (
    guest_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    country VARCHAR(2),
    loyalty_number VARCHAR(20),
    lifetime_stays INT,
    lifetime_revenue DECIMAL(12,2)
);
```

#### rooms
```sql
CREATE TABLE rooms (
    room_id INT PRIMARY KEY,
    room_number VARCHAR(10),
    room_type_id INT,
    floor INT,
    status VARCHAR(20),  -- Clean, Dirty, Occupied, Maintenance
    last_cleaned_at TIMESTAMP
);
```

### Common PMS Data Challenges

#### 1. Historical Data Gaps
**Problem:** PMS systems purge old data after 2-5 years.

**Solution:** Archive to data lake before deletion.
```python
# Monthly archival job
reservations = pms_api.get_reservations(older_than='2_years')
s3.upload('archive/reservations_2024.parquet', reservations)
```

#### 2. Real-Time Updates
**Problem:** Database polling is inefficient.

**Solution:** Use CDC (Change Data Capture) or webhooks.
```python
# Debezium CDC stream
kafka_consumer.subscribe(['pms.reservations'])
for message in consumer:
    event = message.value
    if event['op'] == 'c':  # Create
        process_new_reservation(event)
```

#### 3. Multi-Property Sync
**Problem:** Each property has its own PMS instance.

**Solution:** Central data warehouse with property_id dimension.
```sql
-- Federated query
SELECT hotel_id, COUNT(*)
FROM (
    SELECT * FROM hotel_nyc.reservations
    UNION ALL
    SELECT * FROM hotel_la.reservations
    UNION ALL
    SELECT * FROM hotel_miami.reservations
)
GROUP BY hotel_id
```

---

## 2. POS (Point of Sale) 💳

Tracks all **ancillary revenue** beyond room bookings.

### What is a POS?

Systems that capture:
- **Restaurant:** Orders, tips, split bills
- **Bar:** Drinks, happy hour specials
- **Spa:** Treatments, products
- **Room Service:** In-room dining
- **Retail:** Gift shop purchases

### Popular POS Systems

| System | Use Case |
|--------|----------|
| **Oracle Micros** | Full-service restaurants |
| **Toast** | Quick-service, modern UI |
| **Square** | Small cafes, bars |
| **Lightspeed** | Retail + hospitality |

### Data Structure

#### transactions
```sql
CREATE TABLE pos_transactions (
    transaction_id INT PRIMARY KEY,
    outlet VARCHAR(50),  -- Restaurant, Bar, Spa
    room_number VARCHAR(10),  -- NULL if walk-in
    guest_id INT,
    transaction_time TIMESTAMP,
    subtotal DECIMAL(10,2),
    tax DECIMAL(10,2),
    tip DECIMAL(10,2),
    total DECIMAL(10,2),
    payment_method VARCHAR(20)  -- Cash, Card, Room Charge
);
```

#### line_items
```sql
CREATE TABLE pos_line_items (
    item_id INT PRIMARY KEY,
    transaction_id INT,
    item_name VARCHAR(100),
    category VARCHAR(50),  -- Food, Beverage, Service
    quantity INT,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2)
);
```

### Integration with PMS

**Post to Guest Folio:**
```python
# When guest charges to room
pos_transaction = {
    'amount': 45.50,
    'description': 'Restaurant - Breakfast',
    'room_number': '305'
}

# API call to PMS
pms_api.post_charge(
    room='305',
    amount=45.50,
    description='Breakfast at Terrace Cafe'
)
```

---

## 3. CRS (Central Reservation System) 🌐

Manages bookings across **multiple properties**.

### What is a CRS?

- **Inventory Management:** Room availability across chain
- **Rate Parity:** Ensure same price on all channels
- **Distribution:** Push inventory to OTAs, GDS
- **Reporting:** Chain-wide metrics

### Popular CRS Systems

- **Synxis (Sabre)**
- **SynXis CR (IHG)**
- **Pegasus CRS**

### Data Flow

```
Property 1 PMS ──┐
Property 2 PMS ──┼──→ CRS ──→ Channel Manager ──→ OTAs
Property 3 PMS ──┘
```

---

## 4. Channel Manager 📡

**Middleware** that syncs inventory to distribution channels.

### What Problems Does It Solve?

**Without Channel Manager:**
- 😰 Manual updates on Booking.com, Expedia, Airbnb
- 😰 Overbooking risk (sold same room twice)
- 😰 Rate parity violations

**With Channel Manager:**
- ✅ Two-way sync (inventory + bookings)
- ✅ Real-time availability updates
- ✅ Centralized rate management

### Popular Systems

- SiteMinder
- RateTiger
- Channel Manager (built into modern PMS like Mews)

### Data Flow Example

```python
# Booking received from Booking.com
booking_com_webhook = {
    'reservation_id': 'BDC123456',
    'guest_name': 'John Doe',
    'check_in': '2026-02-01',
    'check_out': '2026-02-03',
    'room_type': 'Deluxe',
    'total_price': 350.00
}

# Channel Manager processes
channel_manager.process_booking(booking_com_webhook)

# Sends to PMS
pms_api.create_reservation({
    'external_id': 'BDC123456',
    'source': 'Booking.com',
    ...
})

# Updates inventory on all channels
channel_manager.update_inventory(
    room_type='Deluxe',
    date='2026-02-01',
    available_count=23  # Was 24, now 23
)
```

---

## 5. OTAs (Online Travel Agencies) ✈️

**Booking.com, Expedia, Airbnb** - where most bookings come from.

### Data You Can Extract

#### Booking Data (Via API)
```python
# Booking.com Connectivity API
bookings = booking_com_api.get_reservations(
    hotel_id='12345',
    start_date='2026-01-01',
    end_date='2026-01-31'
)
```

#### Performance Metrics
```python
# Expedia Partner Central API
metrics = expedia_api.get_hotel_insights(
    hotel_id='67890',
    metrics=['impression_count', 'click_count', 'booking_count']
)
```

### Key Metrics to Track

| Metric | Formula | Why It Matters |
|--------|---------|----------------|
| **Conversion Rate** | Bookings / Page Views | Pricing optimization |
| **Cancellation Rate** | Cancellations / Bookings | Revenue forecasting |
| **Commission %** | OTA Fee / Total Price | True profitability |

---

## 6. RMS (Revenue Management System) 💰

**Dynamic pricing** engine (like airline pricing) that optimizes room rates to maximize revenue.

### What is RMS?

Revenue Management Systems use AI and machine learning to automatically adjust room rates based on:
- **Demand forecasting** - Predicting future bookings
- **Competitor pricing** - Real-time rate shopping
- **Historical trends** - Learning from past performance
- **Market events** - Conferences, concerts, holidays
- **Booking patterns** - Lead time, length of stay

### Popular RMS Systems

| System | Target Market | Key Features |
|--------|---------------|--------------|
| **RoomPriceGenie** | Small/Independent hotels | AI-powered, affordable, easy setup |
| **IDeaS (SAS)** | Enterprise chains | Advanced forecasting, group optimization |
| **Duetto** | Luxury/Upscale | Modern UI, open pricing |
| **Atomize** | Mid-market | Fully automated pricing |

### Why RoomPriceGenie is Interesting for Data Engineers

**Modern Architecture:**
- RESTful API-first design
- Cloud-native (no on-premise installation)
- Real-time recommendations
- Transparent AI reasoning

**Data Pipeline Integration:**
- Connects to PMS via API (reads historical data)
- Analyzes competitor rates (web scraping/API)
- Generates pricing recommendations
- Can auto-update PMS rates (if enabled)

**What Makes It Unique:**
- 🤖 **AI-Driven** - Machine learning adapts to each property
- 💰 **Affordable** - $50-200/month (vs $2,000-10,000 for enterprise)
- ⚡ **Fast Setup** - Days instead of months
- 📊 **Transparent** - Shows why it recommends each price

### Data Flow (Conceptual)

```
┌─────────────┐
│ PMS Data    │ → Historical bookings, rates
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐  ┌──▼──────────┐
│ RMS System  │  │ Competitor  │
│ (AI Engine) │  │ Rate Data   │
└──────┬──────┘  └─────────────┘
       │
       │ Analyzes demand, competition, patterns
       │
┌──────▼────────────────┐
│ Recommendations       │
│ - Suggested rates     │
│ - Confidence scores   │
│ - Reasoning/insights  │
└───────────────────────┘
```

### RMS Data Requirements

**What RMS Needs from Your Data Warehouse:**
- Historical booking data (2+ years)
- Room inventory and types
- Rate plans and restrictions
- Occupancy percentages
- ADR by room type and date
- Booking lead times
- Day of week patterns

**What RMS Provides Back:**
- Recommended rates per room type
- Occupancy forecasts
- Revenue projections
- Competitive position insights
- Demand indicators

### Business Value

**For a 100-room hotel:**
- 5% ADR increase = $50,000+ annual revenue
- Better occupancy optimization
- Reduced manual work (no more spreadsheets)
- Data-driven decisions vs. gut feeling

---

## Data Engineering Strategy for Hotel Systems

### 1. Start with PMS (Core)
```python
# Week 1: Extract PMS reservations
pms_reservations → S3 bronze/
```

### 2. Add POS (Revenue)
```python
# Week 2: Combine room + F&B revenue
pms_reservations + pos_transactions → Total Guest Spend
```

### 3. Integrate OTA Data
```python
# Week 3: Attribution analysis
booking_source → Channel performance metrics
```

### 4. Advanced: Real-Time Sync
```python
# Month 2: CDC pipelines
PMS changes → Kafka → Snowflake (real-time)
```

---

## Hands-On Exercise

**Goal:** Build a data model combining PMS + POS data

```sql
-- Total guest spend (room + ancillary)
SELECT 
    g.guest_name,
    r.confirmation_number,
    r.total_amount as room_revenue,
    COALESCE(SUM(p.total), 0) as ancillary_revenue,
    r.total_amount + COALESCE(SUM(p.total), 0) as total_spend
FROM reservations r
JOIN guests g ON r.guest_id = g.guest_id
LEFT JOIN pos_transactions p ON r.room_number = p.room_number
    AND p.transaction_time BETWEEN r.check_in AND r.check_out
GROUP BY g.guest_name, r.confirmation_number, r.total_amount
ORDER BY total_spend DESC
LIMIT 10;
```

---

## Further Reading

- [Data Engineering Lifecycle](data-engineering-lifecycle.md)
- [Hotel Metrics Guide](hotel-metrics.md)
- [Phase 1 Project](../../projects/phase1-lifecycle/README.md)

---

*This knowledge will be applied in Phase 2 when you integrate real APIs and build ETL pipelines.*
