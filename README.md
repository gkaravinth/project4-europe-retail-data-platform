# Project 4 - Europe Retail Data Platform

## Project Overview

This project demonstrates a production-style Azure data engineering platform for a fictional European retail company called EuroSport Retail Group.

The company operates 10 physical stores, 1 online store, and 1 central warehouse across Europe. The business needs a reliable data platform to monitor sales, inventory, returns, purchase orders, stock transfers, and replenishment risk.

## Business Objective

The objective of this project is to build an end-to-end cloud data platform that can answer key business questions such as:

- Which stores are at stockout risk?
- Which SKUs are overstocked?
- Which products have high sales but low inventory?
- Which purchase orders are delayed?
- Which stock transfers are stuck in transit?
- Which products have high return rates?
- Which stores and products are most profitable?

## Technology Stack

- Azure Blob Storage / Azure Data Lake
- Azure Data Factory
- Azure Databricks
- PySpark
- Delta Lake
- Azure SQL Database
- GitHub
- Power BI

## Architecture Summary

The pipeline follows a production-style data engineering architecture:

1. Source files are placed in the landing zone.
2. Azure Data Factory validates required files using metadata checks.
3. Valid files are copied into the raw zone.
4. Azure Databricks processes the data using Bronze, Silver, and Gold layers.
5. Gold-level fact and dimension tables are written to the processed zone.
6. Azure Data Factory loads curated Gold data into Azure SQL Database.
7. SQL validation queries are used to check record counts, totals, and business rules.
8. Power BI can connect to Azure SQL for reporting and dashboarding.

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

- landing: initial file arrival zone
- raw: validated raw files
- archive: successfully processed files
- rejected: invalid or failed records/files
- processed: Bronze, Silver, and Gold outputs

## Databricks Processing Layers

### Bronze Layer
Raw data ingestion into Delta tables with ingestion metadata.

### Silver Layer
Cleaned, typed, deduplicated, and validated data.

### Gold Layer
Business-ready fact and dimension tables for analytics and reporting.

## Warehouse Tables

Planned Azure SQL warehouse tables:

- dim_product
- dim_store
- dim_supplier
- dim_date
- fact_sales
- fact_inventory_snapshot
- fact_returns
- fact_purchase_orders
- fact_stock_transfers
- fact_replenishment_risk

## Key Business Metrics

- Gross Sales
- Net Sales
- Discount Amount
- Cost
- Profit
- Profit Margin %
- Stock on Hand
- Stockout Risk
- Overstock Flag
- Return Rate
- PO Delay Days
- Transfer Delay Days
- Days of Supply
- Reorder Quantity

## Project Status

Day 1: Project structure, GitHub repository, and documentation setup.