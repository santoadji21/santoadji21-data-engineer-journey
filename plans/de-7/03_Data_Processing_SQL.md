# Module 3: Advanced SQL & Transformation with dbt

## 🎯 Learning Objectives
*   **Master** Window Functions (The hallmark of a skilled Data Engineer).
*   **Implement** dbt (Data Build Tool) for modular, version-controlled SQL.
*   **Optimize** queries using CTEs and Indexing strategies.
*   **Handle** messy data (NULLs, duplicates, string parsing).

## 1. Advanced SQL Concepts
### The Order of Execution
Understanding this helps you debug. SQL does **NOT** run top-to-bottom.
1.  `FROM` / `JOIN` (Gather data)
2.  `WHERE` (Filter rows)
3.  `GROUP BY` (Aggregate)
4.  `HAVING` (Filter groups)
5.  `SELECT` (Return columns)
6.  `ORDER BY` (Sort)
7.  `LIMIT` (Restrict)

### Window Functions
Unlike `GROUP BY`, which collapses rows, Window Functions keep the original rows but add a calculation based on a "window" of data.
*   **Syntax:** `FUNC() OVER (PARTITION BY col1 ORDER BY col2)`
*   **Common Functions:** `RANK()`, `ROW_NUMBER()`, `LEAD()`, `LAG()`.

## 2. The dbt (Data Build Tool) Revolution
dbt is the "T" in ELT. It allows you to write SQL and dbt handles the boilerplate (DDL/DML).
*   **Models:** Just `.sql` files with `SELECT` statements.
*   **Lineage:** dbt builds a graph of how tables depend on each other.
*   **Testing:** Built-in tests for uniqueness, non-null, and relationships.

## 🧪 Hands-On Activity: Your First dbt Model
**Goal:** Transform raw orders into a "Customer Sales Summary" using dbt.

**Step 1: Setup dbt**
*   Ensure `dbt-postgres` is installed.
*   Initialize a project: `dbt init my_transformation`.

**Step 2: Write a Model**
Create `models/marts/customer_summary.sql`:
```sql
{{ config(materialized='table') }}

WITH base_orders AS (
    SELECT * FROM {{ source('raw', 'orders') }}
)
SELECT 
    customer_id,
    COUNT(order_id) as total_orders,
    SUM(amount) as total_spent
FROM base_orders
GROUP BY 1
```

**Step 3: Run & Test**
*   `dbt run`
*   `dbt test`
