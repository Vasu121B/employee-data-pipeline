# Employee data cleaning pipeline

## What this is

A small Python project that takes a messy employee spreadsheet and turns it
into a clean one that is safe to analyse. Four scripts: one makes the messy
data, one cleans it, one loads it into a SQLite database, and one answers
business questions about it with SQL. Four charts come out along the way.

## The question it answers

How many employees does each department have, and what do salaries look
like across the company? You cannot answer either question from the raw
file, because the same department is written six different ways and half
the salaries are stored as text.

## The data

The data is synthetic. There are no real employees in it. `generate_data.py`
builds 5,000 fake employee records (id, name, department, start date,
salary, status, email) with a fixed random seed, then adds the kinds of
mess you find in real exports:

- duplicate rows
- missing values in every column except id
- start dates in five different formats
- departments in mixed case, plus "HR" and "Human Resources" for the same team
- status values with typos, like "Actve" and "Inactve"
- stray spaces around names
- some salaries stored as text with commas, like "72,500.00"

The raw file has 5,150 rows once the duplicates are added.

## Cleaning steps

`clean_data.py` reads the raw CSV and fixes one problem at a time:

1. Trim stray spaces from every text column.
2. Standardise department and status. Each written variant, typos
   included, is mapped to one standard form, so "sales", "SALES" and
   " Sales " all become "Sales".
3. Parse all five date formats into ISO dates (YYYY-MM-DD).
4. Drop exact duplicate rows.
5. Handle missing values with a fixed rule: a row with no name,
   department, or start date is dropped, because those fields are
   required. A missing status becomes "Unknown". Missing salary and
   email are left missing. Inventing a salary would skew every average
   computed later, so the gap stays visible.
6. Clean the salary column: remove commas, convert to a number, and
   drop rows outside 10,000 to 500,000.

## Findings

- 5,150 rows went in and 4,345 came out. 76 were exact duplicates and
  729 were missing a required field.
- After standardising, there are 6 departments. Sales is the largest
  with 955 employees and Marketing is the smallest with 480.
- Median salary is 76,996, with a range of 35,048 to 119,991.
- 213 rows have "Unknown" status and 210 still have no salary. Those
  gaps are left in on purpose so anyone using the file can see them.

## Database and SQL analysis

`load_db.py` loads the clean CSV into a SQLite database,
`data/employees.db`. The `employees` table has a typed column for each
field, with `id` as the primary key. Missing salary and email values are
stored as NULL, so queries can tell "no value" apart from a real zero.

The clean CSV still has 33 repeated ids: the same employee exported twice
with small differences, which exact-duplicate removal cannot catch. The
loader keeps the first row for each id and skips the rest, so the database
holds 4,312 rows where the clean CSV has 4,345. The loader prints both
numbers so the difference is visible.

`analysis.sql` holds six business questions, each written as a comment
above its query:

1. How many employees does each department have?
2. What is the average and median salary in each department? SQLite has no
   built-in median, so salaries are ranked inside each department with a
   window function and the middle rank is picked.
3. How do salaries compare across employee statuses?
4. How many people were hired in each year?
5. Who are the 5 highest-paid employees in each department? This uses
   `ROW_NUMBER()` to rank employees inside their own department.
6. Which departments have the most rows with Unknown status? These are the
   rows where the original status was missing.

`run_analysis.py` runs every query, prints the results, writes them to
`findings.md`, and makes two more charts: average salary by department and
hires per year.

### Analysis findings

All numbers below come from the database run. Full tables are in
`findings.md`.

- Sales is the largest department with 946 employees. Marketing is the
  smallest with 477.
- Human Resources has the highest average salary at 78,634.96 and the
  highest median at 79,420.31. Marketing is lowest on both: average
  75,877.02, median 74,887.24. The spread between departments is small,
  which is what you would expect from randomly generated salaries.
- Average salary barely moves across statuses: 77,238.99 for On Leave up
  to 77,962.23 for Terminated. There is no real pattern there, again as
  expected from synthetic data.
- Hiring is steady: between 370 and 416 hires a year from 2015 to 2025.
  The busiest year is 2018 with 416 hires, the quietest is 2017 with 370.
- The highest-paid employee overall is Grace Walker in Customer Support
  at 119,991.46. The top 5 in every department sit just under 120,000,
  which is the top of the range the generator draws from.
- 205 rows have Unknown status. Sales has the most with 44, Marketing the
  fewest with 21. In real data this would point at where the source
  records were weakest.

## How to run it

You need Python 3 with pandas, numpy, and matplotlib. SQLite is part of
Python's standard library, so there is nothing extra to install for the
database steps.

```
python3 generate_data.py
python3 clean_data.py
python3 load_db.py
python3 run_analysis.py
```

Outputs:

- `data/raw_employees.csv` — the messy input
- `data/clean_employees.csv` — the cleaned output
- `data/employees.db` — the SQLite database
- `findings.md` — the SQL results as tables
- `headcount_by_department.png` — bar chart of employees per department
- `salary_distribution.png` — histogram of salaries
- `avg_salary_by_department.png` — bar chart of average salary per department
- `hires_per_year.png` — bar chart of hires per year

The cleaning script prints a before/after summary (rows in and out,
duplicates removed, rows dropped, values filled) so you can check what
changed without opening the files.
