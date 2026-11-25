"""Load the clean employee data into a SQLite database.

Input:  data/clean_employees.csv  (made by clean_data.py)
Output: data/employees.db

The database has one table, employees, with a typed column for each
field and the employee id as the primary key. Missing salary and
email values are stored as NULL so queries can tell "no value" apart
from a real value of zero or an empty string.

The clean CSV still contains a few repeated ids: the same employee
exported twice with small differences, which exact-duplicate removal
in clean_data.py cannot catch. The loader keeps the first row for
each id, skips the repeats, and prints how many it skipped.
"""

import csv
import os
import sqlite3

CSV_PATH = "data/clean_employees.csv"
DB_PATH = "data/employees.db"

# Start from a fresh database file so re-running this script does not
# pile new rows on top of old ones.
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Typed columns: id is an integer and the primary key, salary is a
# real number, the rest are text. Dates are stored as ISO text
# (YYYY-MM-DD), which sorts and compares correctly in SQLite.
cur.execute(
    """
    CREATE TABLE employees (
        id          INTEGER PRIMARY KEY,
        name        TEXT NOT NULL,
        department  TEXT NOT NULL,
        start_date  TEXT NOT NULL,
        salary      REAL,
        status      TEXT NOT NULL,
        email       TEXT
    )
    """
)

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = []
    seen_ids = set()
    skipped_duplicate_ids = 0
    for row in reader:
        # Keep only the first row for each id (see module docstring).
        emp_id = int(row["id"])
        if emp_id in seen_ids:
            skipped_duplicate_ids += 1
            continue
        seen_ids.add(emp_id)
        # Empty strings in the CSV mean "missing", so store NULL.
        salary = float(row["salary"]) if row["salary"] else None
        email = row["email"] if row["email"] else None
        rows.append(
            (
                emp_id,
                row["name"],
                row["department"],
                row["start_date"],
                salary,
                row["status"],
                email,
            )
        )

cur.executemany(
    "INSERT INTO employees (id, name, department, start_date, salary, status, email)"
    " VALUES (?, ?, ?, ?, ?, ?, ?)",
    rows,
)
conn.commit()

# Read the count back from the database itself, not from the CSV,
# so the printed number proves what actually landed in the table.
cur.execute("SELECT COUNT(*) FROM employees")
count = cur.fetchone()[0]
print(f"Loaded {count} rows into {DB_PATH} (table: employees)")
print(f"Skipped {skipped_duplicate_ids} rows with a repeated id (first row kept)")

conn.close()
