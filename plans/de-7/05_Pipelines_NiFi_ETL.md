# Module 5: Data Pipelines, Orchestration & Quality

## 🎯 Learning Objectives
*   **Master** the "Flow-Based Programming" paradigm of NiFi or the "DAG" paradigm of Airflow.
*   **Implement** Data Quality checks (Circuit Breakers).
*   **Understand** Backpressure, Queues, and Retries.
*   **Compare** NiFi (Data Movement) vs. Airflow/Mage (Workflow Orchestration).

## 1. ETL vs ELT vs Data Quality
*   **ETL (Old School):** Extract -> Transform on a server -> Load to Warehouse.
*   **ELT (Modern):** Extract -> Load to Warehouse (Raw) -> Transform inside the Warehouse (using SQL/dbt).
*   **Data Quality (The "New" Step):** Extract -> Load -> **Test** -> Transform.
    *   *Why?* You don't want to process "garbage" data. Tools like **Great Expectations** or simple SQL assertions are critical.

## 2. Orchestration: The Brain of the Stack
While NiFi moves data, Orchestrators (Airflow, Mage, Dagster) manage the *timing* and *dependencies*.
*   **DAG (Directed Acyclic Graph):** A map of tasks. "Task B only runs if Task A succeeds."
*   **Retries:** If an API is down, the orchestrator automatically tries again in 5 minutes.

## 🧪 Hands-On Activity: Orchestrated Pipeline with Quality Checks
**Goal:** Build a pipeline that pulls data, checks its quality, and then saves it.

**Step 1: Choose your Tool**
*   **Option A (Visual):** Use NiFi.
    1.  **Processor 1:** `InvokeHTTP`. Set URL to a public API (e.g., `https://api.coindesk.com/v1/bpi/currentprice.json`).
    2.  **Processor 2:** `EvaluateJsonPath`. Extract the USD rate.
    3.  **Processor 3:** `PutFile`. Save it to a local directory.
*   **Option B (Code-First):** Use **Mage.ai** or **Airflow**. (Recommended for modern DE).

**Step 2: The Logic with a "Circuit Breaker"**
1.  **Extract:** Pull data from an API.
2.  **Validate (The Quality Check):**
    *   *Task:* Write a Python function that checks if the `price` is a valid number and > 0.
    *   *Action:* If it fails, stop the pipeline and log an error.
3.  **Load:** Save only the "Clean" data to your database.

**Step 3: Cursor Assistance**
*   **Prompt:** "I want to add a data quality check to my Python ingestion script. How can I use a simple `assert` or a library like `pydantic` to ensure my incoming JSON matches the expected schema before I write it to Postgres?"
