# Module 2: Data Ingestion and Storage Patterns

## 🎯 Learning Objectives
* **Compare** Row-oriented vs. Columnar storage (Critical for performance).
* **Understand** File Formats: CSV vs. Parquet vs. Avro.
* **Design** a basic Data Lake folder structure.

## 1. Data Ingestion Techniques
### Batch Ingestion
* **Definition:** Moving large groups of data at scheduled times (e.g., "Daily at 1 AM").
* **Pros:** Easy to manage, less strain on source systems.
* **Cons:** Data is always slightly outdated (high latency).

### Real-Time (Streaming) Ingestion
* **Definition:** Moving data event-by-event as it happens.
* **Pros:** Instant insights (Low latency).
* **Cons:** High complexity, requires specialized infrastructure (Kafka/Flink).

## 2. Storage Deep Dive
### The Database Debate: SQL vs NoSQL
* **SQL (Relational):** Strict schema. Great for financial data where accuracy is paramount.
    * *Concept:* **Normalization** (Reducing redundancy).
* **NoSQL (Non-Relational):** Flexible schema. Great for user profiles, product catalogs, or social media feeds.

### The "File Format" Secret
New engineers use CSVs. Seniors use **Parquet**.
* **CSV/JSON:** Human readable, but slow and heavy. Row-based.
* **Parquet:** Binary, compressed, **Columnar**.
    * *Why Columnar?* If you only need the "Price" column from a 1TB file, Parquet lets you read *only* that column. CSV forces you to read the whole file.

## 3. Introduction to Databases (Dockerized)
Instead of installing Postgres directly on your Mac/Windows, we use Docker. This keeps your OS clean.

## 🧪 Hands-On Activity: SQL & Ingestion
**Goal:** Spin up Postgres and ingest data using Python.

**Step 1: Cursor Composer (`Cmd+I`)**
* Open Cursor. Press `Cmd+I` (Composer).
* **Prompt:** "Write a `docker-compose.yml` file for a PostgreSQL 15 container. Map port 5432. Set user/password to 'admin'/'admin'. Also, include a mapped volume so data persists."
* Run `docker-compose up -d` in the terminal.

**Step 2: Python Ingestion Script**
* Create a file `ingest.py`.
* **Cursor Prompt (`Cmd+K` in file):** "Write a Python script using `sqlalchemy` and `pandas` to generate 1,000 fake ecommerce orders and insert them into the Postgres container we just made. Handle the connection string securely."

**Step 3: Verify**
* Use a tool like DBeaver or the Cursor "Database" extension to query the table: `SELECT * FROM orders LIMIT 10;`.