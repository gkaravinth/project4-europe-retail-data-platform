# Project 4 - Europe Retail Data Platform

## Project Overview

This project demonstrates a production-style Azure data engineering platform for a fictional European retail company called EuroSport Retail Group.

The company operates 10 physical stores, 1 online store, and 1 central warehouse across Europe. The business needs a reliable data platform to monitor sales, inventory, returns, purchase orders, stock transfers, supplier delivery performance, and replenishment risk.

## Business Objective

The objective of this project is to build an end-to-end cloud data platform that can answer key business questions such as:

- Which stores generate the highest sales?
- Which products are most profitable?
- Which products and stores are at reorder risk?
- Which purchase orders are delayed?
- Which suppliers have delivery or receipt issues?
- Which products have high return activity?
- Which online orders contribute to overall sales performance?

## Technology Stack

- Azure Blob Storage / Azure Data Lake style folder structure
- Azure Data Factory
- Azure Databricks
- PySpark
- Delta Lake
- Databricks Unity Catalog
- GitHub
- PyCharm
- Power BI-ready Gold tables

## Architecture Summary

The pipeline follows a production-style data engineering architecture:

1. Source files are generated locally using Python.
2. Source files are uploaded into the Azure Storage landing zone.
3. Azure Data Factory validates required files using Get Metadata activities.
4. Azure Data Factory uses an If Condition to confirm all required landing files exist.
5. Valid files are copied from the landing zone into the raw zone.
6. Azure Databricks reads raw CSV and JSON files.
7. Databricks creates Bronze Delta tables with ingestion metadata.
8. Databricks creates Silver cleaned and standardized Delta tables.
9. Databricks creates Gold business-ready tables for analytics.
10. Gold tables are validated in Databricks Catalog.
11. Gold tables are ready for Power BI reporting.

## Data Sources

The project includes the following source datasets:

- products.csv
- stores.csv
- suppliers.csv
- calendar.csv
- sales_transactions.csv
- inventory_snapshot.csv
- purchase_orders.csv
- stock_transfers.csv
- returns.csv
- online_orders.json

## Data Lake Zones

The Azure Storage container follows a lake-style folder structure:

- landing: initial file arrival zone
- raw: validated files copied by Azure Data Factory
- processed: reserved for curated or exported outputs
- archive: reserved for successfully processed files
- rejected: reserved for invalid or failed files

## Azure Data Factory Pipeline

Pipeline name:

```text
pl_dev_project4_ingest_landing_to_raw

Pipeline logic:

10 Get Metadata activities
        ↓
If Condition: all required files exist
        ↓
10 Copy Data activities
        ↓
Raw zone output

ADF was used to validate and move files from the landing zone to the raw zone.

Databricks Medallion Architecture
Bronze Layer

The Bronze layer stores raw source data as Delta tables with technical metadata.

Bronze tables created:

bronze_products
bronze_stores
bronze_suppliers
bronze_calendar
bronze_sales_transactions
bronze_inventory_snapshot
bronze_purchase_orders
bronze_stock_transfers
bronze_returns
bronze_online_orders_raw

Bronze features:

Reads raw CSV and JSON files from Azure Storage
Stores data as Delta tables
Adds ingestion timestamp
Adds source file path metadata
Preserves raw data structure for audit and reprocessing
Silver Layer

The Silver layer cleans and standardizes Bronze data.

Silver tables created:

silver_products
silver_stores
silver_suppliers
silver_calendar
silver_sales_transactions
silver_inventory_snapshot
silver_purchase_orders
silver_stock_transfers
silver_returns
silver_online_orders
silver_online_order_items

Silver features:

Data type casting
Date conversion
Duplicate removal
Invalid record filtering
Stock status classification
Purchase order delivery status calculation
Receipt status calculation
Online order item flattening

Example stock status rule:

AvailableQty <= 0              → Stockout
AvailableQty <= ReorderPoint   → Reorder Risk
Otherwise                      → Healthy

Example delivery status rule:

ActualDeliveryDate is null                  → Pending
ActualDeliveryDate > ExpectedDeliveryDate   → Delayed
Otherwise                                   → On Time
Gold Layer

The Gold layer creates business-ready reporting tables.

Gold tables created:

gold_dim_products
gold_dim_stores
gold_dim_suppliers
gold_fact_sales
gold_store_sales_summary
gold_product_performance
gold_inventory_risk
gold_supplier_delivery_performance
gold_returns_analysis
gold_online_order_summary

Gold features:

Dimension tables
Sales fact table
Store sales summary
Product performance analysis
Inventory risk analysis
Supplier delivery performance
Returns analysis
Online order summary
Validation Results
Bronze Row Counts
Table	Row Count
bronze_products	101
bronze_stores	12
bronze_suppliers	8
bronze_calendar	25
bronze_sales_transactions	1202
bronze_inventory_snapshot	1201
bronze_purchase_orders	301
bronze_stock_transfers	401
bronze_returns	251
bronze_online_orders_raw	301
Silver Row Counts
Table	Row Count
silver_products	101
silver_stores	12
silver_suppliers	8
silver_calendar	25
silver_sales_transactions	1200
silver_inventory_snapshot	1201
silver_purchase_orders	301
silver_stock_transfers	401
silver_returns	250
silver_online_orders	301
silver_online_order_items	750
Gold Row Counts
Table	Row Count
gold_dim_products	101
gold_dim_stores	12
gold_dim_suppliers	8
gold_fact_sales	1200
gold_store_sales_summary	10
gold_product_performance	100
gold_inventory_risk	1201
gold_supplier_delivery_performance	301
gold_returns_analysis	250
gold_online_order_summary	301
Key Business Metrics

The Gold layer supports the following business metrics:

Gross Sales
Net Sales
Discount Amount
Estimated Cost
Estimated Profit
Profit Margin %
Total Units Sold
Stock on Hand
Available Quantity
Stock Status
Reorder Risk
Purchase Order Delay Status
Receipt Status
Return Quantity
Refund Amount
Supplier Delivery Performance
Security Considerations

During Databricks development, Azure Storage access was tested using a storage account key.

Before pushing code to GitHub, the real key was removed and replaced with a placeholder:

storage_account_key = "PASTE_YOUR_STORAGE_ACCOUNT_KEY_HERE"

In a production environment, secrets should be managed using:

Azure Key Vault
Databricks Secret Scope
Managed Identity
Service Principal authentication
Role-based access control

No real secrets or access keys should be committed to GitHub.

Project Status
Day	Completed Work
Day 1	Project structure, GitHub repository, and documentation setup
Day 2	Sample retail source data generated, profiled, and uploaded to Azure landing zone
Day 3	Azure Data Factory landing-to-raw ingestion pipeline completed
Day 4	Databricks Bronze, Silver, and Gold Delta tables completed using Medallion Architecture
Current Status

Completed:

Source data generation
Azure Storage landing zone upload
Azure Data Factory file validation
Azure Data Factory landing-to-raw copy pipeline
Databricks Bronze Delta tables
Databricks Silver cleaned Delta tables
Databricks Gold business-ready tables
Databricks Catalog validation
GitHub-safe notebook versioning

Next planned step:

Connect Power BI to Gold tables and build a business dashboard.
Portfolio Summary

This project demonstrates hands-on cloud data engineering experience using Azure and Databricks.

It includes:

Data lake folder design
Pipeline orchestration
File validation logic
Delta Lake table creation
Medallion Architecture implementation
Data cleaning and transformation
Business KPI table creation
Databricks Unity Catalog validation
Security awareness
GitHub version control
Power BI readiness

The project is designed to represent a real-world retail and supply chain analytics platform.


Commit message:

```text
Update README with completed medallion architecture pipeline