"""
Project 4 - Europe Retail Data Platform
Script: profile_source_data.py

Purpose:
Profile generated source files before Azure upload.
Checks row counts, columns, and basic file-level information.
"""

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR / "data" / "source_files"


def profile_csv(file_name):
    file_path = SOURCE_DIR / file_name

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames

    print(f"\nCSV File: {file_name}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(columns)}")
    print(f"Column Names: {columns}")


def profile_json(file_name):
    file_path = SOURCE_DIR / file_name

    with open(file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"\nJSON File: {file_name}")
    print(f"Orders: {len(data)}")

    if data:
        print(f"Top-level fields: {list(data[0].keys())}")
        print(f"Customer fields: {list(data[0]['customer'].keys())}")
        print(f"Payment fields: {list(data[0]['payment'].keys())}")
        print(f"Shipping fields: {list(data[0]['shipping'].keys())}")


csv_files = [
    "products.csv",
    "stores.csv",
    "suppliers.csv",
    "calendar.csv",
    "sales_transactions.csv",
    "inventory_snapshot.csv",
    "purchase_orders.csv",
    "stock_transfers.csv",
    "returns.csv",
]

json_files = [
    "online_orders.json"
]


print("Project 4 Source Data Profiling Started")
print(f"Source folder: {SOURCE_DIR}")

for csv_file in csv_files:
    profile_csv(csv_file)

for json_file in json_files:
    profile_json(json_file)

print("\nProject 4 Source Data Profiling Completed")