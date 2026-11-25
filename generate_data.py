"""Generate a messy synthetic employee dataset for the cleaning pipeline.

The data is fake on purpose. It is built to look like a real export from
an HR system that nobody maintained: duplicate rows, missing values,
mixed date formats, mixed-case departments, typos in status, and stray
whitespace. A fixed random seed keeps the output the same every run.
"""

import random
from datetime import date, timedelta

import numpy as np
import pandas as pd

SEED = 42
N_ROWS = 5000

random.seed(SEED)
np.random.seed(SEED)

FIRST_NAMES = [
    "Ava", "Liam", "Noah", "Emma", "Olivia", "Mason", "Sophia", "Lucas",
    "Mia", "Ethan", "Harper", "James", "Evelyn", "Ben", "Charlotte",
    "Henry", "Amelia", "Leo", "Ella", "Jack", "Grace", "Owen", "Chloe",
    "Luke", "Lily", "Adam", "Zoe", "Ryan", "Nora", "Sam",
]
LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Taylor", "Miller", "Davis", "Garcia",
    "Wilson", "Moore", "Anderson", "Thomas", "Jackson", "White", "Harris",
    "Martin", "Clark", "Lewis", "Walker", "Hall", "Young", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Adams", "Baker",
]
# Same department, written several ways. This is the mess.
DEPARTMENTS = [
    "Sales", "sales", "SALES", " Sales ",
    "Engineering", "engineering", "ENGINEERING",
    "HR", "hr", "Human Resources",
    "Finance", "finance", "FINANCE",
    "Support", "support", "Customer Support",
    "Marketing", "marketing",
]
# Same status, written several ways, with a couple of typos.
STATUSES = [
    "Active", "active", "ACTIVE", "Actve", "Activ",
    "Inactive", "inactive", "Inactve",
    "On Leave", "on leave", "OnLeave",
    "Terminated", "terminated",
]
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y", "%Y/%m/%d"]


def random_date():
    """Pick a random start date between 2015 and 2025."""
    start = date(2015, 1, 1)
    end = date(2025, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


def make_row(i):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    # Sometimes pad the name with spaces, like a sloppy manual entry.
    if random.random() < 0.15:
        name = f"  {name} "
    email = f"{first.lower()}.{last.lower()}@example.com"
    if random.random() < 0.10:
        email = email.upper()
    salary = round(random.uniform(35000, 120000), 2)
    # Sometimes store salary as text with a comma, sometimes as a number.
    if random.random() < 0.30:
        salary = f"{salary:,.2f}"
    return {
        "id": i,
        "name": name,
        "department": random.choice(DEPARTMENTS),
        "start_date": random_date().strftime(random.choice(DATE_FORMATS)),
        "salary": salary,
        "status": random.choice(STATUSES),
        "email": email,
    }


rows = [make_row(i) for i in range(1, N_ROWS + 1)]
df = pd.DataFrame(rows)

# Add exact duplicate rows (about 3% of the file).
dupes = df.sample(frac=0.03, random_state=SEED)
df = pd.concat([df, dupes], ignore_index=True)

# Blank out some values at random (about 5% per column, never the id).
for col in ["name", "department", "start_date", "salary", "status", "email"]:
    mask = np.random.random(len(df)) < 0.05
    df.loc[mask, col] = np.nan

# Shuffle so duplicates and blanks are not grouped together.
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

df.to_csv("data/raw_employees.csv", index=False)
print(f"Wrote data/raw_employees.csv with {len(df)} rows")
print(f"Missing values per column:\n{df.isna().sum().to_string()}")
