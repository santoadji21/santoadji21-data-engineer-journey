# Phase 3: Orchestration & Distributed Systems (Scaling Hotel Data)

## 🎯 Objectives
- Move from "Scripts" to "Automated Hotel Pipelines."
- Handle failures gracefully (Retries for flaky OTA APIs).
- Scale processing for large-scale review data (e.g., HotelRec dataset).

## 🛠 Tech Stack
- **Orchestration:** Apache Airflow or Mage.ai.
- **Distributed Compute:** Apache Spark (PySpark) or DuckDB (for medium scale).
- **Streaming:** Kafka or Redpanda (for real-time booking alerts).

## 📚 Topics to Cover
- [ ] **DAGs:** Designing Directed Acyclic Graphs for nightly hotel audits.
- [ ] **Idempotency:** Ensuring a pipeline can re-run for a specific date without doubling revenue.
- [ ] **Backfills:** Reprocessing historical dates safely.
- [ ] **Observability:** Logs, metrics, alerts, and SLAs.
- [ ] **Spark Architecture:** Processing 50M hotel reviews from the HotelRec dataset.
- [ ] **Monitoring:** Slack alerts when a booking ingestion job fails.

## 🏗 Small Win Project
- Build an **Airflow DAG** that:
  1. Downloads a daily "Hotel Review" file.
  2. Triggers a **PySpark** job to perform sentiment analysis.
  3. Updates a "Guest Satisfaction" dashboard.

## 🔗 Free Resources
- [Astronomer Academy (Airflow)](https://academy.astronomer.io/)
- [Spark by Examples](https://sparkbyexamples.com/pyspark-tutorial/)
- [HotelRec: 50M Hotel Reviews Dataset](https://github.com/Diego999/HotelRec)
