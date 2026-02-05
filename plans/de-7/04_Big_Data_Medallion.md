# Module 4: Big Data & The Medallion Architecture

## 🎯 Learning Objectives
* **Understand** Distributed Computing (Sharding, Shuffling).
* **Implement** the Medallion Architecture (Bronze/Silver/Gold) practically.
* **Master** Spark DataFrames vs. SQL.

## 1. Introduction to Spark
Apache Spark is the standard for big data processing.
* **In-Memory Processing:** 100x faster than Hadoop MapReduce because it tries to keep data in RAM.
* **Lazy Evaluation:** Spark doesn't do anything until you ask for a result (like `.show()` or `.write()`). It builds a "DAG" (Directed Acyclic Graph) to optimize the plan first.
* **Cluster Mode:**
    * *Driver:* The boss. Controls the app.
    * *Executors:* The workers. They do the math.

## 2. Medallion Architecture (The Industry Standard)
Organizing a Data Lake (e.g., S3 or ADLS) into three zones:

1.  **🥉 Bronze (Raw):**
    * Exact copy of source data.
    * Append-only.
    * "Dump the data here first so we don't lose it."
2.  **🥈 Silver (Refined):**
    * Cleaned (Deduplicated, Types casted).
    * Enriched (Joined with reference tables).
    * "The Single Source of Truth."
3.  **🥇 Gold (Aggregated):**
    * Business-level aggregates (Daily Sales, KPIs).
    * Optimized for Dashboards (Star Schema).

## 🧪 Hands-On Activity: Local Spark Cluster
**Goal:** Build a mini Medallion pipeline.

**Step 1: Setup**
Ensure `pyspark` is installed (`pip install pyspark`).

**Step 2: The Script**
Create `medallion_job.py`. Use Cursor (`Cmd+K`) to generate the boilerplate:
* **Prompt:** "Create a PySpark script. Initialize a SparkSession. Create a mock DataFrame with dirty data (nulls, duplicates). Implement a Bronze-to-Silver transformation that drops duplicates and fills nulls. Then Silver-to-Gold that groups by category."

**Step 3: Analyze the Plan**
Add this line to your code: `df.explain()`.
Run the script. Look at the output in the terminal.
* **Task:** Paste the "Physical Plan" output into Cursor Chat and ask: "Interpret this Spark Physical Plan for me. Where is the shuffling happening?"