# Project 4 - Europe Retail Data Platform
# Notebook: 00_config
# Purpose: Store common configuration values such as storage paths, database names, and table names.

# Databricks notebook source
# Project 4 - Europe Retail Data Platform
# Notebook: 00_config
# Purpose: Common configuration values for Project 4 Bronze ingestion

# Azure Storage configuration
storage_account_name = "europedata"
container_name = "project4-retail-data-platform"

# Raw zone paths
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

# Bronze database/schema
bronze_database = "project4_bronze"

# Bronze table names
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

print("Project 4 config loaded successfully.")
print(f"Raw base path: {raw_base_path}")
print(f"Bronze database: {bronze_database}")