# Phase 4: The End-to-End Portfolio Project

## 🎯 Objective
- Build a production-grade data pipeline that proves you are a Data Engineer in the Hotel Tech space.

## 🏗 Final Project: The "Hotel Revenue Engine"
- **Extract:** Use a Python scraper or API to pull hotel pricing/availability (or use the Kaggle Hotel Demand dataset).
- **Ingest:** Push data into a Cloud Data Lake (S3/GCS) or local MinIO.
- **Transform:** Use **dbt** to build a Star Schema (`fct_bookings`, `dim_hotels`).
- **Orchestrate:** Schedule nightly updates with **Airflow**.
- **Visualize:** Build a custom **Next.js** dashboard (using your Frontend skills!) or use **Apache Superset** to show RevPAR and Occupancy trends.

## ✅ Skills Checklist for Interviews
- [ ] Can I explain the difference between ADR and RevPAR in my data model?
- [ ] How do I handle a guest changing their stay dates (SCD Type 2)?
- [ ] How do I handle late-arriving booking data from an OTA?

## 🔗 Free Resources
- [Apache Superset (Open Source BI)](https://superset.apache.org/)
- [Next.js + Tremor (Dashboard UI)](https://tremor.so/)
- [Full Stack Data Engineering (Blog)](https://www.startdataengineering.com/)