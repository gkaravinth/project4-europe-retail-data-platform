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