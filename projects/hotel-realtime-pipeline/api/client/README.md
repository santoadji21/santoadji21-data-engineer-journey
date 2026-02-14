# Hotel Realtime Pipeline API — Bruno Collection

REST API client for the Hotel Data Lake API that normalizes bookings from 3 different PMS systems in real-time.

## Setup

1. **Start the pipeline:**
   ```bash
   cd /Users/santoadji21/Projects/data-engineer-journey/projects/hotel-realtime-pipeline
   docker compose up --build
   ```

2. **Wait ~30 seconds** for:
   - Redpanda to start
   - 3 PMS producers to send sample bookings
   - Consumer to write Parquet files
   - API to become available

3. **Open Bruno:**
   - Click **Open Collection**
   - Navigate to: `projects/hotel-realtime-pipeline/api/client/`
   - Select environment: **Local**

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/bookings` | GET | Normalized bookings (default limit: 100) |
| `/bookings?limit=10` | GET | 10 most recent bookings |
| `/bookings?limit=500` | GET | 500 most recent bookings |
| `/stats/occupancy` | GET | Aggregated stats by source system |

## The Problem This API Solves

**3 Different Hotel PMS Systems → 1 Unified API**

### Source Systems:
1. **Legacy PMS** (mainframe)
   ```json
   {
     "source": "legacy",
     "GUEST_NM": "Smith, John",
     "ARR_DT": "15/03/2026",
     "AMT": "175.50"
   }
   ```

2. **Modern PMS** (nested JSON)
   ```json
   {
     "source": "modern",
     "guest": {
       "lastName": "Johnson"
     },
     "booking": {
       "checkInDate": "2026-03-16",
       "totalPrice": "220.75"
     }
   }
   ```

3. **Budget PMS** (minimal)
   ```json
   {
     "source": "budget",
     "client": "Williams",
     "start_date": "20260317",
     "cost": "85.00"
   }
   ```

### Unified Output:
```json
{
  "source_system": "modern",
  "guest_name": "Johnson",
  "check_in_date": "2026-03-16",
  "amount": 220.75,
  "raw_json": "{...original JSON...}"
}
```

## Key Technology

- **DuckDB** — runs SQL directly on Parquet files (no database setup!)
- **JSON extraction** — `json_extract_string()` navigates nested JSON
- **COALESCE** — tries multiple field paths, returns first non-null value
- **Real-time streaming** — Kafka (Redpanda) + Parquet writes

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────┐
│  3 x PMS    │────▶│  Kafka      │────▶│ Consumer │
│  Producers  │     │ (Redpanda)  │     │ (Parquet)│
└─────────────┘     └─────────────┘     └────┬─────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │ Parquet Files │
                                      │  (Data Lake)  │
                                      └───────┬───────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │  FastAPI      │
                                      │  + DuckDB     │
                                      └───────────────┘
```

## Ports

| Service | Port | URL |
|---------|------|-----|
| API (FastAPI) | 8000 | http://localhost:8000 |
| API Docs (Swagger) | 8000 | http://localhost:8000/docs |
| Redpanda Console | 8080 | http://localhost:8080 |
| Kafka Broker | 9092 | localhost:9092 |
