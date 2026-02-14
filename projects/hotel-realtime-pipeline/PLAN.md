# Hotel Real-Time Data Pipeline

This project implements a real-time Event-Driven Architecture (EDA) for Hotel Bookings using Redpanda (Kafka), Python, DuckDB, and dbt.

## 🏗 Architecture

```mermaid
graph LR
    P1[PMS Legacy] -->|Format A| B[Redpanda (Kafka)]
    P2[PMS Modern] -->|Format B| B
    P3[PMS Budget] -->|Format C| B
    B -->|Topic: hotel_bookings| C[Consumer (Lake Writer)]
    C -->|Raw JSON| D[Data Lake (Parquet)]
    D -->|Read| E[DuckDB]
    E -->|Normalize & Clean| F[dbt (Silver)]
    F -->|Aggregate| G[dbt (Gold)]
```

## 🛠 Tech Stack

*   **Message Broker:** Redpanda (Kafka compatible).
*   **Producers:** 3 Python scripts simulating different Property Management Systems (PMS) with **different data schemas**.
*   **Consumer:** Python script writing raw events to Parquet.
*   **Storage:** Local filesystem (Bronze Layer).
*   **Warehouse:** DuckDB.
*   **Transformation:** dbt (handling the "Consensus" / Schema Normalization).

## 🧩 Data Heterogeneity (The Challenge)

We simulate 3 different PMS providers with unique quirks:

1.  **PMS Legacy (The Old School):**
    *   Keys are uppercase and cryptic (`GUEST_NM`, `ARR_DT`).
    *   Dates are `DD/MM/YYYY`.
    *   Flat structure.
2.  **PMS Modern (The Startup):**
    *   Nested JSON (`guest: { name: ... }`).
    *   ISO 8601 Dates (`YYYY-MM-DD`).
    *   Uses UUIDs.
3.  **PMS Budget (The Minimalist):**
    *   Different field names (`client`, `start_date`).
    *   Dates are integers (`20260214`).
    *   Missing some optional fields.

**Goal:** The pipeline must ingest all 3 formats into the Bronze layer, and then **dbt** will normalize them into a single "Consensus Schema" in the Silver layer.

## 🚀 Phases

### Phase 1: Infrastructure & Producers
*   Set up Redpanda.
*   Create `producer/pms_legacy.py`, `producer/pms_modern.py`, `producer/pms_budget.py`.
*   Run them in parallel to flood the topic with mixed-format data.

### Phase 2: Consumer & Data Lake
*   Create `consumer/main.py` to listen to `hotel_bookings`.
*   Store raw JSON blobs in Parquet (Variant/JSON type) to preserve the original structure.

### Phase 3: The "Consensus" (dbt)
*   Use DuckDB's JSON extraction functions.
*   Write dbt models to map:
    *   `GUEST_NM` -> `guest_name`
    *   `guest.name` -> `guest_name`
    *   `client` -> `guest_name`
*   Create a unified `silver_bookings` table.
