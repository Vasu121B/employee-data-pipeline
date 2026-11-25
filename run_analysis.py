"""Run the SQL analysis questions and save the results.

Input:  analysis.sql        (the questions, as SQL queries)
        data/employees.db   (made by load_db.py)
Output: findings.md
        avg_salary_by_department.png
        hires_per_year.png

Each query in analysis.sql is run against the database. Results are
printed to the screen and written to findings.md so the numbers can
be read without running anything. Two charts are made from the
average-salary and hires-per-year results.
"""

import sqlite3

import matplotlib

matplotlib.use("Agg")  # write PNGs without needing a display
import matplotlib.pyplot as plt

SQL_PATH = "analysis.sql"
DB_PATH = "data/employees.db"
FINDINGS_PATH = "findings.md"


def split_queries(sql_text):
    """Split the .sql file into (title, query) pairs.

    Queries are separated by semicolons. The comment lines above each
    query become its title.
    """
    pairs = []
    for chunk in sql_text.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        title_lines = []
        for line in chunk.splitlines():
            line = line.strip()
            if line.startswith("--"):
                title_lines.append(line[2:].strip())
        # The question itself is the comment line that starts with
        # "Q" and a number, like "Q1: ...". The file header comment
        # sits above Q1, so skip past it to find the real question.
        title = "Query"
        for line in title_lines:
            if len(line) > 1 and line[0] == "Q" and line[1].isdigit():
                title = line
                break
        else:
            if title_lines:
                title = title_lines[0]
        pairs.append((title, chunk))
    return pairs


def format_value(value):
    """Format one result value for display."""
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:,.2f}"
    return str(value)


with open(SQL_PATH, encoding="utf-8") as f:
    queries = split_queries(f.read())

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

all_results = []  # (title, column names, rows) for every query
for title, query in queries:
    cur.execute(query)
    columns = [d[0] for d in cur.description]
    rows = cur.fetchall()
    all_results.append((title, columns, rows))

    print(f"\n{title}")
    print(" | ".join(columns))
    for row in rows:
        print(" | ".join(format_value(v) for v in row))

conn.close()

# Write the same results to findings.md as simple markdown tables.
with open(FINDINGS_PATH, "w", encoding="utf-8") as f:
    f.write("# Findings\n\n")
    f.write(
        "Results of the questions in analysis.sql, run against "
        "data/employees.db. The data is synthetic (see README.md).\n"
    )
    for title, columns, rows in all_results:
        f.write(f"\n## {title}\n\n")
        f.write("| " + " | ".join(columns) + " |\n")
        f.write("| " + " | ".join("---" for _ in columns) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(format_value(v) for v in row) + " |\n")

print(f"\nWrote {FINDINGS_PATH}")

# Chart 1: average salary by department (from Q2, the second query).
_, _, salary_rows = all_results[1]
departments = [r[0] for r in salary_rows]
avg_salaries = [r[2] for r in salary_rows]
plt.figure(figsize=(8, 4.5))
plt.bar(departments, avg_salaries, color="#4C72B0")
plt.title("Average salary by department")
plt.xlabel("Department")
plt.ylabel("Average salary")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("avg_salary_by_department.png", dpi=150)
plt.close()

# Chart 2: hires per year (from Q4, the fourth query).
_, _, hire_rows = all_results[3]
years = [r[0] for r in hire_rows]
hires = [r[1] for r in hire_rows]
plt.figure(figsize=(8, 4.5))
plt.bar(years, hires, color="#55A868")
plt.title("Hires per year")
plt.xlabel("Year")
plt.ylabel("Hires")
plt.tight_layout()
plt.savefig("hires_per_year.png", dpi=150)
plt.close()

print("Wrote avg_salary_by_department.png and hires_per_year.png")
