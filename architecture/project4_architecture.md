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