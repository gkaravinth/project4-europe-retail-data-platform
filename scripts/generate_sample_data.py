"""
Project 4 - Europe Retail Data Platform
Script: generate_sample_data.py

Purpose:
Generate realistic sample source-system files for the Project 4 Azure retail data platform.

Output location:
data/source_files/
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


# -----------------------------
# Configuration
# -----------------------------

random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "data" / "source_files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = datetime(2026, 5, 1)
END_DATE = datetime(2026, 5, 25)

CURRENCY = "EUR"


# -----------------------------
# Helper functions
# -----------------------------

def write_csv(file_name, fieldnames, rows):
    file_path = OUTPUT_DIR / file_name
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created CSV: {file_path}")


def write_json(file_name, data):
    file_path = OUTPUT_DIR / file_name
    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Created JSON: {file_path}")


def random_date(start_date, end_date):
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    random_seconds = random.randint(0, 86399)
    return start_date + timedelta(days=random_days, seconds=random_seconds)


def date_str(date_value):
    return date_value.strftime("%Y-%m-%d")


def datetime_str(date_value):
    return date_value.strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# Master data
# -----------------------------

stores = [
    {"StoreID": "S001", "StoreName": "Berlin Flagship", "StoreType": "Physical Store", "Country": "Germany", "City": "Berlin", "Region": "Central Europe", "OpenDate": "2020-01-15", "IsActive": True},
    {"StoreID": "S002", "StoreName": "Munich Store", "StoreType": "Physical Store", "Country": "Germany", "City": "Munich", "Region": "Central Europe", "OpenDate": "2020-03-20", "IsActive": True},
    {"StoreID": "S003", "StoreName": "Paris Store", "StoreType": "Physical Store", "Country": "France", "City": "Paris", "Region": "Western Europe", "OpenDate": "2021-02-10", "IsActive": True},
    {"StoreID": "S004", "StoreName": "Amsterdam Store", "StoreType": "Physical Store", "Country": "Netherlands", "City": "Amsterdam", "Region": "Western Europe", "OpenDate": "2021-06-01", "IsActive": True},
    {"StoreID": "S005", "StoreName": "Brussels Store", "StoreType": "Physical Store", "Country": "Belgium", "City": "Brussels", "Region": "Western Europe", "OpenDate": "2021-09-18", "IsActive": True},
    {"StoreID": "S006", "StoreName": "Madrid Store", "StoreType": "Physical Store", "Country": "Spain", "City": "Madrid", "Region": "Southern Europe", "OpenDate": "2022-01-05", "IsActive": True},
    {"StoreID": "S007", "StoreName": "Milan Store", "StoreType": "Physical Store", "Country": "Italy", "City": "Milan", "Region": "Southern Europe", "OpenDate": "2022-04-12", "IsActive": True},
    {"StoreID": "S008", "StoreName": "Warsaw Store", "StoreType": "Physical Store", "Country": "Poland", "City": "Warsaw", "Region": "Eastern Europe", "OpenDate": "2022-08-08", "IsActive": True},
    {"StoreID": "S009", "StoreName": "Stockholm Store", "StoreType": "Physical Store", "Country": "Sweden", "City": "Stockholm", "Region": "Northern Europe", "OpenDate": "2023-01-11", "IsActive": True},
    {"StoreID": "S010", "StoreName": "Vienna Store", "StoreType": "Physical Store", "Country": "Austria", "City": "Vienna", "Region": "Central Europe", "OpenDate": "2023-05-25", "IsActive": True},
    {"StoreID": "S011", "StoreName": "Online Store", "StoreType": "Online Store", "Country": "Germany", "City": "Online", "Region": "Digital", "OpenDate": "2020-01-01", "IsActive": True},
    {"StoreID": "W001", "StoreName": "Frankfurt Central Warehouse", "StoreType": "Warehouse", "Country": "Germany", "City": "Frankfurt", "Region": "Central Europe", "OpenDate": "2019-07-01", "IsActive": True},
]

suppliers = [
    {"SupplierID": "SUP001", "SupplierName": "Adler Sportswear GmbH", "Country": "Germany", "LeadTimeDays": 7, "ReliabilityScore": 94.5, "IsActive": True},
    {"SupplierID": "SUP002", "SupplierName": "Nordic Active AB", "Country": "Sweden", "LeadTimeDays": 10, "ReliabilityScore": 88.0, "IsActive": True},
    {"SupplierID": "SUP003", "SupplierName": "Iberia Footwear SL", "Country": "Spain", "LeadTimeDays": 12, "ReliabilityScore": 84.0, "IsActive": True},
    {"SupplierID": "SUP004", "SupplierName": "Milano Apparel SRL", "Country": "Italy", "LeadTimeDays": 9, "ReliabilityScore": 91.0, "IsActive": True},
    {"SupplierID": "SUP005", "SupplierName": "Paris Lifestyle SAS", "Country": "France", "LeadTimeDays": 8, "ReliabilityScore": 89.5, "IsActive": True},
    {"SupplierID": "SUP006", "SupplierName": "Benelux Accessories BV", "Country": "Netherlands", "LeadTimeDays": 6, "ReliabilityScore": 96.0, "IsActive": True},
    {"SupplierID": "SUP007", "SupplierName": "Warsaw Performance Sp Zoo", "Country": "Poland", "LeadTimeDays": 14, "ReliabilityScore": 81.5, "IsActive": True},
    {"SupplierID": "SUP008", "SupplierName": "Vienna Outdoor Handels GmbH", "Country": "Austria", "LeadTimeDays": 11, "ReliabilityScore": 86.5, "IsActive": True},
]

categories = {
    "Jerseys": ["Home Jersey", "Away Jersey", "Training Jersey"],
    "Caps": ["Baseball Cap", "Snapback Cap", "Beanie"],
    "Hoodies": ["Pullover Hoodie", "Zip Hoodie", "Training Hoodie"],
    "Footwear": ["Running Shoes", "Training Shoes", "Lifestyle Sneakers"],
    "Shorts": ["Training Shorts", "Match Shorts"],
    "Accessories": ["Water Bottle", "Backpack", "Scarf", "Gym Bag"],
    "Kidswear": ["Kids Jersey", "Kids Hoodie", "Kids Shorts"],
}

brands = ["EuroSport", "AdlerFit", "NordRun", "UrbanAthlete", "PeakMotion"]

products = []
product_counter = 1

for category, sub_categories in categories.items():
    for _ in range(15):
        if product_counter > 100:
            break

        product_id = f"P{product_counter:04d}"
        sku = f"SKU-{product_counter:05d}"
        sub_category = random.choice(sub_categories)
        brand = random.choice(brands)
        supplier = random.choice(suppliers)

        unit_cost = round(random.uniform(5, 80), 2)
        retail_price = round(unit_cost * random.uniform(1.4, 2.5), 2)

        products.append({
            "ProductID": product_id,
            "SKU": sku,
            "ProductName": f"{brand} {sub_category}",
            "Category": category,
            "SubCategory": sub_category,
            "Brand": brand,
            "SupplierID": supplier["SupplierID"],
            "UnitCost": unit_cost,
            "RetailPrice": retail_price,
            "Currency": CURRENCY,
            "IsActive": True
        })

        product_counter += 1

products = products[:100]

# Add one bad product record intentionally
products.append({
    "ProductID": "",
    "SKU": "SKU-BAD-001",
    "ProductName": "Invalid Product Missing ID",
    "Category": "",
    "SubCategory": "Unknown",
    "Brand": "Unknown",
    "SupplierID": "SUP999",
    "UnitCost": -10,
    "RetailPrice": 5,
    "Currency": "USD",
    "IsActive": True
})


# -----------------------------
# Calendar data
# -----------------------------

calendar_rows = []
current_date = START_DATE

while current_date <= END_DATE:
    calendar_rows.append({
        "DateKey": int(current_date.strftime("%Y%m%d")),
        "CalendarDate": date_str(current_date),
        "Year": current_date.year,
        "Quarter": (current_date.month - 1) // 3 + 1,
        "Month": current_date.month,
        "MonthName": current_date.strftime("%B"),
        "WeekOfYear": int(current_date.strftime("%U")),
        "DayName": current_date.strftime("%A"),
        "IsWeekend": current_date.weekday() >= 5
    })
    current_date += timedelta(days=1)


# -----------------------------
# Transaction data
# -----------------------------

physical_stores = [store for store in stores if store["StoreType"] == "Physical Store"]

sales_rows = []
transaction_ids = []

for i in range(1, 1201):
    transaction_id = f"T{i:06d}"
    transaction_ids.append(transaction_id)

    product = random.choice(products[:-1])
    store = random.choice(physical_stores)
    quantity = random.randint(1, 5)
    unit_price = float(product["RetailPrice"])
    gross_sales = round(quantity * unit_price, 2)
    discount = round(gross_sales * random.choice([0, 0, 0.05, 0.10, 0.15]), 2)
    net_sales = round(gross_sales - discount, 2)

    sales_rows.append({
        "TransactionID": transaction_id,
        "TransactionDate": datetime_str(random_date(START_DATE, END_DATE)),
        "StoreID": store["StoreID"],
        "ProductID": product["ProductID"],
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "DiscountAmount": discount,
        "GrossSales": gross_sales,
        "NetSales": net_sales,
        "PaymentMethod": random.choice(["Cash", "Card", "Wallet"]),
        "SalesChannel": "Store"
    })

# Bad sales records intentionally
sales_rows.append({
    "TransactionID": "T_BAD_001",
    "TransactionDate": datetime_str(END_DATE + timedelta(days=20)),
    "StoreID": "S999",
    "ProductID": "P9999",
    "Quantity": -2,
    "UnitPrice": 20,
    "DiscountAmount": 5,
    "GrossSales": -40,
    "NetSales": -45,
    "PaymentMethod": "Card",
    "SalesChannel": "Store"
})

# Duplicate transaction intentionally
sales_rows.append(sales_rows[0].copy())


inventory_rows = []

for store in stores:
    for product in products[:100]:
        stock_on_hand = random.randint(0, 300)
        reserved_qty = random.randint(0, 30)
        reorder_point = random.randint(15, 60)
        safety_stock = random.randint(10, 40)

        inventory_rows.append({
            "SnapshotDate": date_str(END_DATE),
            "StoreID": store["StoreID"],
            "ProductID": product["ProductID"],
            "StockOnHand": stock_on_hand,
            "ReservedQty": reserved_qty,
            "AvailableQty": stock_on_hand - reserved_qty,
            "ReorderPoint": reorder_point,
            "SafetyStock": safety_stock
        })

# Bad inventory record intentionally
inventory_rows.append({
    "SnapshotDate": date_str(END_DATE),
    "StoreID": "S999",
    "ProductID": "P9999",
    "StockOnHand": "",
    "ReservedQty": -5,
    "AvailableQty": -10,
    "ReorderPoint": 20,
    "SafetyStock": 10
})


purchase_order_rows = []

for i in range(1, 301):
    po_id = f"PO{i:06d}"
    supplier = random.choice(suppliers)
    product = random.choice(products[:100])
    order_date = random_date(START_DATE - timedelta(days=20), END_DATE)
    expected_date = order_date + timedelta(days=supplier["LeadTimeDays"])

    is_received = random.choice([True, True, True, False])
    actual_date = expected_date + timedelta(days=random.randint(-2, 8)) if is_received else None

    ordered_qty = random.randint(50, 500)
    received_qty = ordered_qty if is_received else random.randint(0, ordered_qty - 1)

    if not is_received:
        status = "Open"
    elif received_qty < ordered_qty:
        status = "Partially Received"
    elif actual_date > expected_date:
        status = "Delayed"
    else:
        status = "Closed"

    purchase_order_rows.append({
        "POID": po_id,
        "SupplierID": supplier["SupplierID"],
        "ProductID": product["ProductID"],
        "WarehouseID": "W001",
        "OrderDate": date_str(order_date),
        "ExpectedDeliveryDate": date_str(expected_date),
        "ActualDeliveryDate": date_str(actual_date) if actual_date else "",
        "OrderedQty": ordered_qty,
        "ReceivedQty": received_qty,
        "POStatus": status
    })

# Bad PO record intentionally
purchase_order_rows.append({
    "POID": "PO_BAD_001",
    "SupplierID": "SUP999",
    "ProductID": "P9999",
    "WarehouseID": "W999",
    "OrderDate": "2026-06-10",
    "ExpectedDeliveryDate": "2026-05-01",
    "ActualDeliveryDate": "2026-04-30",
    "OrderedQty": -100,
    "ReceivedQty": 200,
    "POStatus": "Unknown"
})


stock_transfer_rows = []

for i in range(1, 401):
    transfer_id = f"TR{i:06d}"
    product = random.choice(products[:100])
    to_store = random.choice(physical_stores)
    transfer_date = random_date(START_DATE, END_DATE)
    expected_arrival = transfer_date + timedelta(days=random.randint(1, 5))

    status = random.choice(["Created", "In Transit", "Received", "Delayed"])
    transfer_qty = random.randint(5, 80)

    if status == "Received":
        actual_arrival = expected_arrival + timedelta(days=random.randint(-1, 3))
        received_qty = random.randint(max(1, transfer_qty - 5), transfer_qty)
    elif status == "Delayed":
        actual_arrival = ""
        received_qty = 0
    else:
        actual_arrival = ""
        received_qty = 0

    stock_transfer_rows.append({
        "TransferID": transfer_id,
        "ProductID": product["ProductID"],
        "FromLocationID": "W001",
        "ToLocationID": to_store["StoreID"],
        "TransferDate": date_str(transfer_date),
        "ExpectedArrivalDate": date_str(expected_arrival),
        "ActualArrivalDate": date_str(actual_arrival) if actual_arrival else "",
        "TransferQty": transfer_qty,
        "ReceivedQty": received_qty,
        "TransferStatus": status
    })

# Bad transfer record intentionally
stock_transfer_rows.append({
    "TransferID": "TR_BAD_001",
    "ProductID": "P9999",
    "FromLocationID": "S001",
    "ToLocationID": "S001",
    "TransferDate": "2026-05-20",
    "ExpectedArrivalDate": "2026-05-10",
    "ActualArrivalDate": "2026-05-09",
    "TransferQty": -10,
    "ReceivedQty": 20,
    "TransferStatus": "InvalidStatus"
})


return_rows = []

for i in range(1, 251):
    original_sale = random.choice(sales_rows[:-2])
    return_qty = random.randint(1, max(1, int(original_sale["Quantity"])))
    refund_amount = round((float(original_sale["NetSales"]) / int(original_sale["Quantity"])) * return_qty, 2)

    return_rows.append({
        "ReturnID": f"R{i:06d}",
        "TransactionID": original_sale["TransactionID"],
        "ReturnDate": date_str(random_date(START_DATE, END_DATE)),
        "StoreID": original_sale["StoreID"],
        "ProductID": original_sale["ProductID"],
        "ReturnQty": return_qty,
        "ReturnReason": random.choice(["Size Issue", "Damaged", "Customer Changed Mind", "Wrong Item", "Quality Issue"]),
        "RefundAmount": refund_amount
    })

# Bad return record intentionally
return_rows.append({
    "ReturnID": "R_BAD_001",
    "TransactionID": "T999999",
    "ReturnDate": "2026-06-15",
    "StoreID": "S999",
    "ProductID": "P9999",
    "ReturnQty": -1,
    "ReturnReason": "",
    "RefundAmount": -50
})


# -----------------------------
# Online orders nested JSON
# -----------------------------

online_orders = []

for i in range(1, 301):
    order_date = random_date(START_DATE, END_DATE)
    item_count = random.randint(1, 4)
    selected_products = random.sample(products[:100], item_count)

    items = []
    order_total = 0

    for product in selected_products:
        quantity = random.randint(1, 3)
        unit_price = float(product["RetailPrice"])
        line_total = round(quantity * unit_price, 2)
        order_total += line_total

        items.append({
            "product_id": product["ProductID"],
            "sku": product["SKU"],
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total
        })

    discount_amount = round(order_total * random.choice([0, 0, 0.05, 0.10]), 2)
    net_total = round(order_total - discount_amount, 2)

    order = {
        "order_id": f"WEB{i:06d}",
        "order_date": datetime_str(order_date),
        "customer": {
            "customer_id": f"CUST{random.randint(1, 500):06d}",
            "customer_name": random.choice(["Anna Muller", "Lucas Schmidt", "Sofia Rossi", "Emma Dubois", "Jan Kowalski"]),
            "country": random.choice(["Germany", "France", "Italy", "Netherlands", "Spain", "Sweden"])
        },
        "payment": {
            "payment_method": random.choice(["Card", "PayPal", "Wallet"]),
            "payment_status": random.choice(["Paid", "Paid", "Paid", "Pending", "Failed"]),
            "gross_total": round(order_total, 2),
            "discount_amount": discount_amount,
            "net_total": net_total,
            "currency": CURRENCY
        },
        "shipping": {
            "address": {
                "city": random.choice(["Berlin", "Paris", "Milan", "Amsterdam", "Madrid", "Stockholm"]),
                "country": random.choice(["Germany", "France", "Italy", "Netherlands", "Spain", "Sweden"])
            },
            "shipping_method": random.choice(["Standard", "Express"]),
            "shipping_status": random.choice(["Packed", "Dispatched", "Delivered", "Delayed"])
        },
        "items": items,
        "discounts": [
            {
                "discount_type": random.choice(["Promotion", "Loyalty", "Seasonal"]),
                "discount_amount": discount_amount
            }
        ] if discount_amount > 0 else [],
        "delivery_events": [
            {"event_time": datetime_str(order_date + timedelta(hours=3)), "event_status": "Order Confirmed"},
            {"event_time": datetime_str(order_date + timedelta(days=1)), "event_status": "Packed"},
            {"event_time": datetime_str(order_date + timedelta(days=2)), "event_status": "Dispatched"}
        ]
    }

    online_orders.append(order)

# Bad online order intentionally
online_orders.append({
    "order_id": "",
    "order_date": "2026-07-01 10:00:00",
    "customer": {
        "customer_id": "",
        "customer_name": "Invalid Customer",
        "country": "Unknown"
    },
    "payment": {
        "payment_method": "Unknown",
        "payment_status": "InvalidStatus",
        "gross_total": -100,
        "discount_amount": 200,
        "net_total": -300,
        "currency": "USD"
    },
    "shipping": {
        "address": {
            "city": "",
            "country": ""
        },
        "shipping_method": "Unknown",
        "shipping_status": "Unknown"
    },
    "items": [],
    "discounts": [],
    "delivery_events": []
})


# -----------------------------
# Write files
# -----------------------------

write_csv("products.csv", list(products[0].keys()), products)
write_csv("stores.csv", list(stores[0].keys()), stores)
write_csv("suppliers.csv", list(suppliers[0].keys()), suppliers)
write_csv("calendar.csv", list(calendar_rows[0].keys()), calendar_rows)
write_csv("sales_transactions.csv", list(sales_rows[0].keys()), sales_rows)
write_csv("inventory_snapshot.csv", list(inventory_rows[0].keys()), inventory_rows)
write_csv("purchase_orders.csv", list(purchase_order_rows[0].keys()), purchase_order_rows)
write_csv("stock_transfers.csv", list(stock_transfer_rows[0].keys()), stock_transfer_rows)
write_csv("returns.csv", list(return_rows[0].keys()), return_rows)
write_json("online_orders.json", online_orders)

print("\nAll Project 4 sample source files generated successfully.")
print(f"Output folder: {OUTPUT_DIR}")