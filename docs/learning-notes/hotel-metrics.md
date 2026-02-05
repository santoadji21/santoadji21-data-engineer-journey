# Hotel Industry Metrics 🏨

Key performance indicators (KPIs) used in hotel revenue management and analytics.

## Core Metrics

### ADR (Average Daily Rate)
**Formula:** `Total Room Revenue / Number of Rooms Sold`

The average rental income per paid occupied room in a given time period.

**Example:**
```sql
SELECT 
    hotel_name,
    ROUND(AVG(price_per_night), 2) as ADR
FROM bookings
WHERE status = 'Checked-In'
GROUP BY hotel_name;
```

**Why it matters:** Shows pricing power and revenue per room. Higher ADR can indicate premium positioning or high demand periods.

---

### RevPAR (Revenue Per Available Room)
**Formula:** `Total Room Revenue / Total Available Rooms`  
**Alternative:** `ADR × Occupancy Rate`

The revenue generated per available room, whether occupied or not.

**Example:**
```sql
-- Assuming 100 rooms available per hotel
SELECT 
    hotel_name,
    SUM(total_revenue) as total_revenue,
    100 as available_rooms,
    COUNT(DISTINCT check_in) as operating_days,
    ROUND(SUM(total_revenue) / (100 * COUNT(DISTINCT check_in)), 2) as RevPAR
FROM bookings
WHERE status = 'Checked-In'
GROUP BY hotel_name;
```

**Why it matters:** The most important metric for hotel profitability. Balances both occupancy and pricing.

---

### Occupancy Rate
**Formula:** `(Rooms Sold / Available Rooms) × 100`

The percentage of available rooms that are occupied.

**Example:**
```sql
SELECT 
    DATE_TRUNC('day', check_in) as date,
    COUNT(*) as rooms_sold,
    100 as available_rooms,
    ROUND((COUNT(*) * 100.0 / 100), 2) as occupancy_rate
FROM bookings
WHERE status = 'Checked-In'
GROUP BY DATE_TRUNC('day', check_in)
ORDER BY date;
```

**Why it matters:** Shows demand. High occupancy with low ADR means you're underpriced. Low occupancy with high ADR means you're overpriced.

---

### TRevPAR (Total Revenue Per Available Room)
**Formula:** `Total Hotel Revenue / Available Rooms`

Like RevPAR, but includes all revenue streams (F&B, spa, parking, etc.), not just rooms.

---

## Secondary Metrics

### Length of Stay (LOS)
Average number of nights guests stay.

```sql
SELECT 
    hotel_name,
    ROUND(AVG(stay_nights), 1) as avg_length_of_stay
FROM bookings
WHERE status = 'Checked-In'
GROUP BY hotel_name;
```

---

### Cancellation Rate
Percentage of bookings that are cancelled.

```sql
SELECT 
    ROUND(
        COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) as cancellation_rate
FROM bookings;
```

---

### No-Show Rate
Percentage of bookings where guests don't arrive.

---

## Data Modeling for Hotel Metrics

### Fact Table: `fact_bookings`
```sql
CREATE TABLE fact_bookings (
    booking_id VARCHAR PRIMARY KEY,
    hotel_id INT,
    room_type_id INT,
    guest_id INT,
    check_in_date DATE,
    check_out_date DATE,
    stay_nights INT,
    price_per_night DECIMAL(10,2),
    total_revenue DECIMAL(10,2),
    status VARCHAR
);
```

### Dimension Tables
- `dim_hotels`: Hotel properties
- `dim_room_types`: Room categories
- `dim_guests`: Guest profiles
- `dim_date`: Time dimension

---

## Real-World Application

In hotel tech, these metrics are used for:
- **Revenue Management:** Dynamic pricing algorithms
- **Forecasting:** Predicting demand and revenue
- **Benchmarking:** Comparing against competitors
- **BI Dashboards:** Executive reporting

---

*See also: `/plans/Phase1_The_Pivot.md` for SQL practice with these metrics*
