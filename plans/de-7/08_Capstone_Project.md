# Module 8: Capstone Project - End-to-End Data Pipeline

## 🎯 Learning Objectives
*   **Integrate** all previous modules into a single, cohesive data system.
*   **Implement** a full Medallion Architecture (Bronze -> Silver -> Gold).
*   **Apply** Data Quality checks and Orchestration.
*   **Visualize** the final output in a dashboard.

## 1. The Scenario: "Global Hotel Analytics"
You are the Lead Data Engineer for a hotel chain. You need to build a pipeline that:
1.  **Ingests** raw booking data from a legacy Postgres system (Bronze).
2.  **Cleans and Enriches** the data using Spark/DuckDB (Silver).
3.  **Aggregates** KPIs like "Revenue per Room" and "Occupancy Rate" (Gold).
4.  **Orchestrates** the whole flow using a scheduler.

## 2. Architecture Diagram
`Postgres (Source) -> Airflow/Mage (Orchestrator) -> Spark (Processing) -> DuckDB/Postgres (Gold Warehouse) -> Dashboard`

## 3. Project Requirements
### Phase 1: Infrastructure
*   `docker-compose` with Postgres, Spark, and an Orchestrator.
*   Shared volume for data persistence.

### Phase 2: The Pipeline
*   **Bronze:** Python script to extract data from Postgres to Parquet files.
*   **Silver:** Spark job to handle NULLs, deduplicate bookings, and join with "Hotel Metadata."
*   **Gold:** SQL views or Spark jobs to create Star Schema tables (Fact_Bookings, Dim_Hotels, Dim_Time).

### Phase 3: Quality & Reliability
*   Add at least 3 data quality checks (e.g., "Amount cannot be negative").
*   Configure Slack/Email alerts for pipeline failures.

## 🧪 Hands-On Activity: Final Submission
**Goal:** Deploy the full stack and run a successful "Backfill" of 1 year of data.

1.  **Run the Orchestrator:** Trigger the DAG.
2.  **Monitor:** Check logs for any Spark shuffling issues.
3.  **Verify:** Query the Gold layer to ensure KPIs match the raw data totals.
4.  **Showcase:** Create a 1-page PDF/Markdown report with the final dashboard screenshots.
