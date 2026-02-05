# Module 3: Advanced Data Processing with SQL

## 🎯 Learning Objectives
* **Master** Window Functions (The hallmark of a skilled Data Engineer).
* **Optimize** queries using CTEs and Indexing strategies.
* **Handle** messy data (NULLs, duplicates, string parsing).

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
* **Syntax:** `FUNC() OVER (PARTITION BY col1 ORDER BY col2)`
* **Common Functions:** `RANK()`, `ROW_NUMBER()`, `LEAD()` (look at next row), `LAG()` (look at previous row).

## 2. Data Transformation Strategy
* **CTEs (Common Table Expressions):** Using `WITH` clauses to break complex logic into readable chunks. Always prefer CTEs over nested subqueries for readability.
* **Data Cleaning:**
    * `COALESCE(col, 0)`: Replace NULL with 0.
    * `CAST(col AS DATE)`: Fix data types.
    * `TRIM()`: Remove whitespace.

## 🧪 Hands-On Activity: The "Complex Query" Challenge
**Goal:** Solve a hard business problem using SQL.

**Scenario:** You have the `orders` table from Module 2. We need to find the **Rolling 3-day Average Sales** for every customer.

**Step 1: Generate Data (if needed)**
Use Cursor to ensure your `orders` table has `customer_id`, `order_date`, and `amount`.

**Step 2: Write the Query (Try first, then use Cursor)**
Try to write a query that calculates the average sales for a customer over the current row plus the previous 2 rows.

**Step 3: The Cursor "Explain" Feature**
* Highlight your SQL query.
* Press `Cmd+L`.
* **Prompt:** "Explain this SQL query to me line-by-line. Is there a more performant way to write this using a Window Function?"

**Expected Solution Pattern:**
```sql
SELECT
    customer_id,
    order_date,
    amount,
    AVG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as rolling_3_day_avg
FROM orders;