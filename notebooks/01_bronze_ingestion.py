# Project 4 - Europe Retail Data Platform
# Notebook: 01_bronze_ingestion
# Purpose: Ingest raw source files into Bronze Delta tables with ingestion metadata.

# Databricks notebook source
# Project 4 - Europe Retail Data Platform
# Notebook: 01_bronze_ingestion
# Purpose: Read raw files from Azure Storage and write Bronze Delta tables

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, col

# COMMAND ----------

# ============================================================
# 1. Project configuration + Azure Storage access
# ============================================================

storage_account_name = "europedata"

# IMPORTANT:
# Paste your real Azure Storage account key below.
# Azure Portal → Storage accounts → europedata → Access keys → key1 → Show → Copy key
# DO NOT commit this real key to GitHub.
storage_account_key = "PASTE_YOUR_STORAGE_ACCOUNT_KEY_HERE"

spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
    storage_account_key
)

print("Azure Storage access key configured for Databricks session.")

container_name = "project4-retail-data-platform"

raw_base_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/raw"

raw_products_path = f"{raw_base_path}/products/products.csv"
raw_stores_path = f"{raw_base_path}/stores/stores.csv"
raw_suppliers_path = f"{raw_base_path}/suppliers/suppliers.csv"
raw_calendar_path = f"{raw_base_path}/calendar/calendar.csv"
raw_sales_path = f"{raw_base_path}/sales/sales_transactions.csv"
raw_inventory_path = f"{raw_base_path}/inventory/inventory_snapshot.csv"
raw_purchase_orders_path = f"{raw_base_path}/purchase_orders/purchase_orders.csv"
raw_stock_transfers_path = f"{raw_base_path}/stock_transfers/stock_transfers.csv"
raw_returns_path = f"{raw_base_path}/returns/returns.csv"
raw_online_orders_path = f"{raw_base_path}/online_orders/online_orders.json"

bronze_database = "project4_bronze"

bronze_products_table = f"{bronze_database}.bronze_products"
bronze_stores_table = f"{bronze_database}.bronze_stores"
bronze_suppliers_table = f"{bronze_database}.bronze_suppliers"
bronze_calendar_table = f"{bronze_database}.bronze_calendar"
bronze_sales_table = f"{bronze_database}.bronze_sales_transactions"
bronze_inventory_table = f"{bronze_database}.bronze_inventory_snapshot"
bronze_purchase_orders_table = f"{bronze_database}.bronze_purchase_orders"
bronze_stock_transfers_table = f"{bronze_database}.bronze_stock_transfers"
bronze_returns_table = f"{bronze_database}.bronze_returns"
bronze_online_orders_table = f"{bronze_database}.bronze_online_orders_raw"

print("Project 4 configuration loaded successfully.")
print(f"Raw base path: {raw_base_path}")
print(f"Bronze database: {bronze_database}")

# COMMAND ----------

# ============================================================
# 2. Create Bronze database
# ============================================================

spark.sql(f"CREATE DATABASE IF NOT EXISTS {bronze_database}")

print(f"Bronze database ready: {bronze_database}")

# COMMAND ----------

# ============================================================
# 3. Helper functions
# ============================================================

def read_csv_from_raw(file_path):
    """
    Read CSV file from raw zone.
    Bronze layer keeps source data mostly as-is.
    Unity Catalog does not support input_file_name(), so we use _metadata.file_path.
    """
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(file_path)
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_file_name", col("_metadata.file_path"))
    )
    return df


def read_json_from_raw(file_path):
    """
    Read nested JSON file from raw zone.
    Bronze layer keeps nested JSON structure.
    Unity Catalog does not support input_file_name(), so we use _metadata.file_path.
    """
    df = (
        spark.read
        .option("multiline", "true")
        .json(file_path)
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_file_name", col("_metadata.file_path"))
    )
    return df


def write_bronze_table(df, table_name):
    """
    Write DataFrame as Delta table in Bronze database.
    Overwrite mode is acceptable for this development project.
    """
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )

    row_count = df.count()
    print(f"Written table: {table_name} | Rows: {row_count}")
    return row_count

# COMMAND ----------

# ============================================================
# 4. Read raw files from Azure Storage
# ============================================================

df_products = read_csv_from_raw(raw_products_path)
df_stores = read_csv_from_raw(raw_stores_path)
df_suppliers = read_csv_from_raw(raw_suppliers_path)
df_calendar = read_csv_from_raw(raw_calendar_path)
df_sales = read_csv_from_raw(raw_sales_path)
df_inventory = read_csv_from_raw(raw_inventory_path)
df_purchase_orders = read_csv_from_raw(raw_purchase_orders_path)
df_stock_transfers = read_csv_from_raw(raw_stock_transfers_path)
df_returns = read_csv_from_raw(raw_returns_path)

df_online_orders = read_json_from_raw(raw_online_orders_path)

print("All raw files read successfully.")

# COMMAND ----------

# ============================================================
# 5. Quick raw row count check before writing Bronze
# ============================================================

print("Raw row counts before Bronze write:")

print(f"products: {df_products.count()}")
print(f"stores: {df_stores.count()}")
print(f"suppliers: {df_suppliers.count()}")
print(f"calendar: {df_calendar.count()}")
print(f"sales_transactions: {df_sales.count()}")
print(f"inventory_snapshot: {df_inventory.count()}")
print(f"purchase_orders: {df_purchase_orders.count()}")
print(f"stock_transfers: {df_stock_transfers.count()}")
print(f"returns: {df_returns.count()}")
print(f"online_orders: {df_online_orders.count()}")

# COMMAND ----------

# ============================================================
# 6. Write Bronze Delta tables
# ============================================================

row_counts = {}

row_counts["bronze_products"] = write_bronze_table(df_products, bronze_products_table)
row_counts["bronze_stores"] = write_bronze_table(df_stores, bronze_stores_table)
row_counts["bronze_suppliers"] = write_bronze_table(df_suppliers, bronze_suppliers_table)
row_counts["bronze_calendar"] = write_bronze_table(df_calendar, bronze_calendar_table)
row_counts["bronze_sales_transactions"] = write_bronze_table(df_sales, bronze_sales_table)
row_counts["bronze_inventory_snapshot"] = write_bronze_table(df_inventory, bronze_inventory_table)
row_counts["bronze_purchase_orders"] = write_bronze_table(df_purchase_orders, bronze_purchase_orders_table)
row_counts["bronze_stock_transfers"] = write_bronze_table(df_stock_transfers, bronze_stock_transfers_table)
row_counts["bronze_returns"] = write_bronze_table(df_returns, bronze_returns_table)
row_counts["bronze_online_orders_raw"] = write_bronze_table(df_online_orders, bronze_online_orders_table)

print("All Bronze tables created successfully.")

# COMMAND ----------

# ============================================================
# 7. Bronze row count validation summary
# ============================================================

print("Bronze row count validation summary:")

for table_name, count_value in row_counts.items():
    print(f"{table_name}: {count_value}")

# COMMAND ----------

# ============================================================
# 8. Show Bronze database tables
# ============================================================

spark.sql(f"SHOW TABLES IN {bronze_database}").show(truncate=False)

# COMMAND ----------

# ============================================================
# 9. Sample data checks
# ============================================================

print("Sample products:")
spark.sql(f"SELECT * FROM {bronze_products_table} LIMIT 5").show(truncate=False)

print("Sample sales transactions:")
spark.sql(f"SELECT * FROM {bronze_sales_table} LIMIT 5").show(truncate=False)

print("Sample online orders raw:")
spark.sql(f"SELECT * FROM {bronze_online_orders_table} LIMIT 5").show(truncate=False)

# COMMAND ----------

print("Project 4 Bronze ingestion completed successfully.")