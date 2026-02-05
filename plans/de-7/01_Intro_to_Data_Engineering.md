# Module 1: Introduction to Data Engineering

## 🎯 Learning Objectives
* **Distinguish** clearly between Data Engineering, Data Science, and Software Engineering.
* **Map** the Modern Data Stack (MDS) ecosystem.
* **Set up** a professional development environment using Cursor and Docker.

## 1. Overview of Data Engineering
### The Core Mission
Data Engineering is the practice of designing and building systems for collecting, storing, and analyzing data at scale. It is a "Force Multiplier"—data scientists and analysts cannot work effectively without the infrastructure engineers build.

### Roles & Responsibilities Matrix
| Role | Primary Focus | Key Output | Typical Tools |
| :--- | :--- | :--- | :--- |
| **Data Engineer** | Infrastructure & Pipelines | Clean, reliable Tables/APIs | SQL, Python, Spark, Airflow |
| **Data Scientist** | Math & Algorithms | Predictive Models | Python (Pandas/Sklearn), Jupyter |
| **Analytics Engineer** | Business Logic | Dashboards & Metrics | dbt, SQL, Tableau |

### Why is it exploding now?
Data volume is growing exponentially (Big Data), but **data variety** (JSON, Video, Logs) and **velocity** (Real-time) have made traditional systems obsolete. Companies need engineers to manage this complexity.

## 2. The Data Lifecycle (Detailed)
1.  **Generation:** Data is created by users (clicks), systems (logs), or sensors (IoT).
2.  **Ingestion:** Moving data from Source to a Landing Zone.
    * *Push vs. Pull:* Do we query the API, or does the API send data to us?
3.  **Storage:** Persisting data.
    * *Hot Storage:* Fast, expensive (RAM/SSD) for frequent access.
    * *Cold Storage:* Slow, cheap (S3 Glacier) for archiving.
4.  **Processing (Transformation):** The "T" in ETL. Cleaning, deduplicating, and aggregating.
5.  **Serving:** Making data available for BI tools or ML models.

## 3. The Modern Data Stack Landscape
* **Cloud Providers:** AWS, Azure, GCP (The foundation).
* **Compute:** Snowflake (Warehousing), Databricks (Spark/AI).
* **Ingestion:** Fivetran, Airbyte (Move data without code).
* **Orchestration:** Airflow, Dagster, Mage (The "traffic controllers").
* **Transformation:** dbt (Data Build Tool) - effectively standard for SQL transformation.

## 🧪 Hands-On Activity: The "Cursor" Setup
**Goal:** Configure your machine for maximum productivity.

1.  **Install Docker Desktop:** Mandatory for running databases locally without messing up your system.
2.  **Install Cursor:**
    * Open Cursor.
    * Install the **"Docker"** and **"Python"** extensions.
3.  **Cursor AI Power Move:**
    * Create a file named `requirements.txt`.
    * Open the Cursor Chat (`Cmd+L` or `Ctrl+L`).
    * **Prompt:** "I am learning data engineering. Generate a `requirements.txt` file with the most common Python libraries for Data Engineering (include pandas, polars, pyspark, sqlalchemy, psycopg2)."
    * Run `pip install -r requirements.txt` in the terminal.