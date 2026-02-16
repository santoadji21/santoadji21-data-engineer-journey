SELECT * FROM happiness_scores
LIMIT 10;

SELECT * FROM country_stats
LIMIT 10;

-- Basic JOIN

SELECT *
FROM happiness_scores hs
    INNER JOIN country_stats cs
    ON hs.country = cs.country;

-- Product JOIN
SELECT
    p.product_id,
    p.product_name
FROM products p
         LEFT JOIN orders o
                   ON p.product_id = o.product_id
WHERE o.product_id IS NULL;

-- JOIN Multiple Column
SELECT year, country, happiness_score
FROM happiness_scores;

SELECT year, country_name, inflation_rate
FROM inflation_rates;

SELECT hs.year, hs.country,
       hs.happiness_score, ir.inflation_rate
FROM happiness_scores hs
    INNER JOIN inflation_rates ir
    ON hs.year = ir.year AND hs.country = ir.country_name;

-- Self JOIN
CREATE TABLE IF NOT EXISTS  employees(
    employee_id INT PRIMARY KEY ,
    employee_name VARCHAR(100),
    salary INT,
    manager_id INT
);

INSERT INTO employees (employee_id, employee_name, salary, manager_id) VALUES
    (1, 'John Doe', 100000, NULL),
    (2, 'Jane Smith', 80000, 1),
    (3, 'Jim Beam', 60000, 1),
    (4, 'Jill Johnson', 70000, 2),
    (5, 'Jack Johnson', 70000, 2),
    (6, 'Sara Parker', 65000, 3),
    (7, 'Tom Bradley', 72000, 3),
    (8, 'Emily Davis', 58000, 2),
    (9, 'Mike Chen', 95000, 1),
    (10, 'Anna Lee', 67000, 4),
    (11, 'Chris Martin', 71000, 4),
    (12, 'Diana Ross', 63000, 3);

SELECT * FROM employees;

-- Employees with the same salary
SELECT e1.employee_id, e1.employee_name, e1.salary,
    e2.employee_id, e2.employee_name, e2.salary
FROM employees e1 INNER JOIN employees e2
     ON e1.salary = e2.salary
WHERE e1.employee_name <> e2.employee_name
ORDER BY e1.employee_name;

-- Employees that have a greater salary
SELECT e1.employee_id, e1.employee_name, e1.salary,
    e2.employee_id, e2.employee_name, e2.salary
FROM employees e1 INNER JOIN employees e2
     ON e1.salary > e2.salary
WHERE e1.employee_name <> e2.employee_name
ORDER BY e1.salary DESC ;

-- Employees and their managers
SELECT e1.employee_id, e1.employee_name, e1.manager_id,
    e2.employee_name AS manager_name
FROM employees e1 LEFT JOIN employees e2
     ON e1.manager_id = e2.employee_id;

-- Which products are within 25 cents of each other in terms of unit price? also add price diff
SELECT p1.product_id, p1.product_name, p1.unit_price,
    p2.product_id, p2.product_name, p2.unit_price,
    p1.unit_price - p2.unit_price AS price_diff
FROM products p1 INNER JOIN products p2
     ON ABS(p1.unit_price - p2.unit_price) < 0.25
WHERE p1.product_id <> p2.product_id
ORDER BY price_diff DESC;

-- CROSS JOIN

CREATE TABLE IF NOT EXISTS tops(
    id INT,
    item VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS sizes(
    id INT,
    size VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS outerwear(
    id INT,
    item VARCHAR(50)
);

INSERT INTO tops (id, item) VALUES
    (1, 'T-Shirt'),
    (2, 'Hoodie'),
    (3, 'Sweater'),
    (4, 'Jacket'),
    (5, 'Coat'),
    (6, 'Shirt'),
    (7, 'Polo'),
    (8, 'Tank Top'),
    (9, 'Hoodie'),
    (10, 'Sweater'),
    (11, 'Jacket');

INSERT INTO sizes (id, size) VALUES
    (101, 'Small'),
    (102, 'Medium'),
    (103, 'Large');
    
INSERT INTO outerwear (id, item) VALUES
    (2, 'Hoodie'),
    (3, 'Jacket'),
    (4, 'Coat');

SELECT * FROM tops;
SELECT * FROM sizes;
SELECT * FROM outerwear;

-- CROSS JOIN the tables
SELECT * FROM tops CROSS JOIN sizes;

SELECT t.item, s.size
FROM tops t
    CROSS JOIN sizes s;

-- UNION the tables
SELECT * FROM tops
UNION
SELECT * FROM outerwear;

-- UNION ALL the tables
SELECT * FROM tops
UNION ALL
SELECT * FROM outerwear;

-- UNION with different column names
SELECT * FROM tops
UNION ALL
SELECT * FROM outerwear;

-- UNION with different column names
SELECT * FROM tops
UNION ALL
SELECT * FROM outerwear;

-- UNION with different column names
SELECT * FROM tops
UNION ALL
SELECT * FROM outerwear;
