-- Business questions about the cleaned employee data.
-- Run against data/employees.db (table: employees).
-- Each query is one question, with the question written above it.

-- Q1: How many employees does each department have?
SELECT department,
       COUNT(*) AS employees
FROM employees
GROUP BY department
ORDER BY employees DESC;

-- Q2: What is the average and median salary in each department?
-- SQLite has no built-in median, so salaries are ranked inside each
-- department and the middle rank is picked (for an even count that
-- is the upper of the two middle values). AVG ignores NULL salaries
-- on its own, so missing salaries do not drag it down.
WITH ranked AS (
    SELECT department,
           salary,
           ROW_NUMBER() OVER (
               PARTITION BY department
               ORDER BY salary
           ) AS rank_in_department,
           COUNT(*) OVER (PARTITION BY department) AS salary_count
    FROM employees
    WHERE salary IS NOT NULL
),
medians AS (
    SELECT department, salary AS median_salary
    FROM ranked
    WHERE rank_in_department = salary_count / 2 + 1
)
SELECT e.department,
       COUNT(*) AS employees,
       ROUND(AVG(e.salary), 2) AS avg_salary,
       m.median_salary
FROM employees e
JOIN medians m ON m.department = e.department
GROUP BY e.department
ORDER BY e.department;

-- Q3: How do salaries compare across employee statuses?
SELECT status,
       COUNT(*) AS employees,
       ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY status
ORDER BY avg_salary DESC;

-- Q4: How many people were hired in each year?
-- start_date is stored as ISO text (YYYY-MM-DD), so strftime can
-- pull the year straight out of it.
SELECT CAST(strftime('%Y', start_date) AS INTEGER) AS hire_year,
       COUNT(*) AS hires
FROM employees
GROUP BY hire_year
ORDER BY hire_year;

-- Q5: Who are the 5 highest-paid employees in each department?
-- ROW_NUMBER ranks employees inside their own department, highest
-- salary first. Only ranks 1 to 5 are kept. Rows with no salary
-- are left out because they cannot be ranked.
SELECT department, name, salary
FROM (
    SELECT department,
           name,
           salary,
           ROW_NUMBER() OVER (
               PARTITION BY department
               ORDER BY salary DESC
           ) AS rank_in_department
    FROM employees
    WHERE salary IS NOT NULL
)
WHERE rank_in_department <= 5
ORDER BY department, salary DESC;

-- Q6: Which departments have the most rows with Unknown status?
-- These are the rows where the original status was missing, so a
-- high count points at where the source data was weakest.
SELECT department,
       COUNT(*) AS unknown_status_rows
FROM employees
WHERE status = 'Unknown'
GROUP BY department
ORDER BY unknown_status_rows DESC;
