# Phase 2: Infrastructure & Modern Data Stack (Hotel Analytics)

## 🎯 Objectives
- Containerize hotel data workflows.
- Learn the "T" in ELT (Transformation) using dbt.
- Understand Cloud Storage patterns for hospitality data.

## 🛠 Tech Stack
- **Containers:** Docker & Docker Compose.
- **Transformation:** dbt (data build tool).
- **Storage:** S3 (or MinIO for local) & Snowflake/BigQuery (or DuckDB for local).

## 📚 Topics to Cover
- [ ] **Docker:** Networking multiple services (Postgres + dbt + Metabase).
- [ ] **dbt (Analytics Engineering):** Writing SQL models for `stg_bookings`, `fct_revenue`.
- [ ] **Data Quality:** Implementing dbt tests for unique booking IDs and non-negative prices.
- [ ] **dbt Advanced:** Snapshots, incremental models, sources, exposures, docs site.
- [ ] **CI/CD:** Run `dbt build` and `dbt test` on PRs.
- [ ] **Medallion Architecture:**
    - **Bronze:** Raw JSON/CSV from PMS.
    - **Silver:** Cleaned bookings with standardized date formats.
    - **Gold:** Aggregated metrics like "Monthly RevPAR by Property".
- [ ] **IaC:** Basic Terraform to set up a cloud bucket for hotel images or logs.

## 🏗 Small Win Project
- Use **Docker Compose** to spin up a Postgres DB and a **dbt** environment. Transform "raw" Kaggle hotel data into a "Gold" table showing Revenue by Room Type using SQL models.

## 🔗 Free Resources
- [dbt Fundamentals Course](https://courses.getdbt.com/courses/fundamentals)
- [Docker for Data Engineers (YouTube)](https://www.youtube.com/results?search_query=docker+for+data+engineering)
- [Medallion Architecture Explained](https://www.databricks.com/glossary/medallion-architecture)
