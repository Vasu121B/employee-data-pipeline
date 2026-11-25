"""Clean the messy employee dataset step by step.

Input:  data/raw_employees.csv  (made by generate_data.py)
Output: data/clean_employees.csv
        headcount_by_department.png
        salary_distribution.png

Cleaning rules, in order:
1. Trim stray whitespace from every text column.
2. Standardise department and status: fix casing and spelling variants
   so each real value has exactly one written form.
3. Parse the mixed date formats into ISO dates (YYYY-MM-DD).
4. Drop exact duplicate rows.
5. Missing values: rows missing a name, department, or start date are
   dropped (those fields are required). Missing status becomes
   "Unknown". Missing salary stays missing (NaN) so averages are not
   skewed by invented numbers. Missing email stays missing.
6. Salary: strip commas, convert to a number, and drop rows where the
   salary is not numeric or falls outside 10,000 to 500,000.
"""

import matplotlib

matplotlib.use("Agg")  # write PNGs without needing a display
import matplotlib.pyplot as plt
import pandas as pd

RAW_PATH = "data/raw_employees.csv"
CLEAN_PATH = "data/clean_employees.csv"

# Every written variant of a department, mapped to one standard form.
DEPARTMENT_MAP = {
    "sales": "Sales",
    "engineering": "Engineering",
    "hr": "Human Resources",
    "human resources": "Human Resources",
    "finance": "Finance",
    "support": "Customer Support",
    "customer support": "Customer Support",
    "marketing": "Marketing",
}

# Every written variant of a status (typos included), mapped to one form.
STATUS_MAP = {
    "active": "Active",
    "actve": "Active",
    "activ": "Active",
    "inactive": "Inactive",
    "inactve": "Inactive",
    "on leave": "On Leave",
    "onleave": "On Leave",
    "terminated": "Terminated",
}

df = pd.read_csv(RAW_PATH, dtype=str)  # read everything as text first
rows_in = len(df)
print(f"Rows in: {rows_in}")

# 1. Trim whitespace from all text columns.
for col in df.columns:
    df[col] = df[col].str.strip()

# 2. Standardise department and status.
df["department"] = df["department"].str.lower().map(DEPARTMENT_MAP)
df["status"] = df["status"].str.lower().map(STATUS_MAP)

# 3. Parse mixed date formats to ISO. Unparseable dates become NaT.
df["start_date"] = pd.to_datetime(
    df["start_date"], format="mixed", dayfirst=False, errors="coerce"
).dt.date

# 4. Drop exact duplicate rows.
before_dupes = len(df)
df = df.drop_duplicates()
dupes_removed = before_dupes - len(df)

# 5. Handle missing values.
missing_before = df.isna().sum()
required = ["name", "department", "start_date"]
before_missing = len(df)
df = df.dropna(subset=required)
dropped_missing = before_missing - len(df)
df["status"] = df["status"].fillna("Unknown")
status_filled = int(missing_before["status"])

# 6. Salary: remove commas, convert to number, keep a sane range.
df["salary"] = pd.to_numeric(
    df["salary"].str.replace(",", "", regex=False), errors="coerce"
)
before_salary = len(df)
df = df[df["salary"].isna() | df["salary"].between(10000, 500000)]
salary_dropped = before_salary - len(df)

# id back to integer, sorted for a tidy output file.
df["id"] = df["id"].astype(int)
df = df.sort_values("id").reset_index(drop=True)

df.to_csv(CLEAN_PATH, index=False)
print(f"Rows out: {len(df)}")
print(f"Exact duplicates removed: {dupes_removed}")
print(f"Rows dropped for missing name/department/start_date: {dropped_missing}")
print(f"Rows dropped for out-of-range salary: {salary_dropped}")
print(f"Missing status filled with 'Unknown': {status_filled}")
print(f"Missing salary left as-is: {int(df['salary'].isna().sum())}")
print(f"Missing email left as-is: {int(df['email'].isna().sum())}")

# Chart 1: headcount by department.
counts = df["department"].value_counts().sort_index()
plt.figure(figsize=(8, 4.5))
counts.plot(kind="bar", color="#4C72B0")
plt.title("Headcount by department")
plt.xlabel("Department")
plt.ylabel("Employees")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("headcount_by_department.png", dpi=150)
plt.close()

# Chart 2: salary distribution.
plt.figure(figsize=(8, 4.5))
df["salary"].dropna().plot(kind="hist", bins=30, color="#55A868")
plt.title("Salary distribution")
plt.xlabel("Salary")
plt.ylabel("Employees")
plt.tight_layout()
plt.savefig("salary_distribution.png", dpi=150)
plt.close()

print("Wrote headcount_by_department.png and salary_distribution.png")
print(f"Departments in clean data: {sorted(df['department'].unique())}")
print(f"Statuses in clean data: {sorted(df['status'].unique())}")
print(f"Salary range: {df['salary'].min():,.0f} to {df['salary'].max():,.0f}")
print(f"Median salary: {df['salary'].median():,.0f}")
