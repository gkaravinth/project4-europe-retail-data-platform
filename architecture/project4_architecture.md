# Project 4 Architecture - Europe Retail Data Platform

## 1. Architecture Overview

This project follows a production-style Azure data engineering architecture for a European retail business.

The platform ingests data from multiple retail source systems, validates the files using Azure Data Factory, processes the data using Azure Databricks, stores curated outputs in Azure Data Lake, and loads final fact and dimension tables into Azure SQL Database for analytics and reporting.

## 2. High-Level Architecture Flow

```text
Source Systems
    ↓
Azure Data Lake - Landing Zone
    ↓
Azure Data Factory - File Validation and Ingestion
    ↓
Azure Data Lake - Raw Zone
    ↓
Azure Databricks - Bronze Layer
    ↓
Azure Databricks - Silver Layer
    ↓
Azure Databricks - Gold Layer
    ↓
Azure Data Lake - Processed Zone
    ↓
Azure Data Factory - Copy Activity
    ↓
Azure SQL Database - Data Warehouse Layer
    ↓
Power BI / Reporting Layer


3. Source Systems

The project simulates the following retail source systems:

POS sales system
E-commerce order system
Warehouse inventory system
Supplier purchase order system
Store transfer system
Returns management system
Product master system
Store master system
Supplier master system
4. Data Lake Zones
Landing Zone

The landing zone is the initial file arrival area. Source files are placed here before validation.

Raw Zone

The raw zone stores validated source files copied from the landing zone. These files are used by Databricks for Bronze ingestion.

Archive Zone

The archive zone stores successfully processed source files for audit and reprocessing if needed.

Rejected Zone

The rejected zone stores invalid files or records that fail data quality checks.

Processed Zone

The processed zone stores curated Bronze, Silver, and Gold outputs.

5. Azure Data Factory Layer

Azure Data Factory is used as the orchestration layer.

ADF responsibilities:

Validate mandatory files using Get Metadata
Use If Condition to control processing
Use ForEach to process multiple files
Copy files from landing to raw zone
Archive successfully processed files
Trigger Databricks notebooks
Copy Gold outputs into Azure SQL Database
Run validation checks after SQL load
Support manual, scheduled, or event-based triggers
6. Azure Databricks Layer

Azure Databricks is used as the transformation and processing engine.

Databricks responsibilities:

Read validated raw files
Create Bronze Delta tables
Clean and standardize data in Silver layer
Flatten nested online order JSON
Apply data quality checks
Build Gold fact and dimension tables
Write curated outputs to processed zone
7. Medallion Architecture
Bronze Layer

Bronze stores raw ingested data as Delta tables with minimal transformation.

Examples:

bronze_sales_transactions
bronze_inventory_snapshot
bronze_products
bronze_stores
bronze_suppliers
bronze_purchase_orders
bronze_stock_transfers
bronze_returns
bronze_online_orders_raw
Silver Layer

Silver stores cleaned, typed, deduplicated, and validated data.

Examples:

silver_sales_clean
silver_inventory_clean
silver_products_clean
silver_stores_clean
silver_suppliers_clean
silver_purchase_orders_clean
silver_stock_transfers_clean
silver_returns_clean
silver_online_orders_flat
Gold Layer

Gold stores business-ready fact and dimension tables.

Dimensions:

gold_dim_product
gold_dim_store
gold_dim_supplier
gold_dim_date

Facts:

gold_fact_sales
gold_fact_inventory_snapshot
gold_fact_returns
gold_fact_purchase_orders
gold_fact_stock_transfers
gold_fact_replenishment_risk
8. Azure SQL Database Layer

Azure SQL Database acts as the analytics serving layer.

The Gold fact and dimension tables are loaded into Azure SQL using ADF Copy Activity.

Planned SQL tables:

dbo.dim_product
dbo.dim_store
dbo.dim_supplier
dbo.dim_date
dbo.fact_sales
dbo.fact_inventory_snapshot
dbo.fact_returns
dbo.fact_purchase_orders
dbo.fact_stock_transfers
dbo.fact_replenishment_risk
9. GitHub and Version Control

GitHub is used for version control and project documentation.

Repository structure:

project4-europe-retail-data-platform/
    adf/
    architecture/
    data/
    docs/
    notebooks/
    sql/
    README.md

Branch strategy:

dev branch for development
main branch for stable project version
10. Development and Production Pattern
Development
Develop code in PyCharm
Save project files locally
Commit and push changes to GitHub
Develop and test notebooks in Databricks using a development cluster
Production-Style Execution
Publish ADF pipeline
Use Trigger Now or scheduled trigger
Run Databricks notebooks through ADF
Load Gold tables to Azure SQL
Validate output using SQL queries
Monitor pipeline runs in ADF Monitor
11. Monitoring and Validation

Validation will include:

Source file existence checks
Row count validation
Duplicate transaction validation
Null key validation
Sales total validation
Inventory risk validation
PO delay validation
Transfer delay validation
SQL warehouse load validation
12. Security Considerations

Production improvements should include:

Azure Key Vault for secrets
Managed identities or service principals
Role-based access control
Private endpoints where required
No hardcoded passwords or access keys
GitHub should not contain secrets
13. Final Architecture Summary

This project demonstrates a production-style Azure retail data platform using Azure Data Lake, Azure Data Factory, Azure Databricks, Azure SQL Database, PySpark, Delta Lake, GitHub, and Power BI-ready warehouse tables.