# Project 4 Video Script - Europe Retail Data Platform

## Introduction

In this project, I built a production-style Azure data engineering platform for a fictional European retail company called EuroSport Retail Group.

The company operates 10 physical stores, 1 online store, and 1 central warehouse across Europe. The business needs a reliable data platform to monitor sales, inventory, returns, purchase orders, stock transfers, and replenishment risk.

## Business Problem

The main business problem is to create a single trusted data platform that can answer questions such as:

- Which stores are at stockout risk?
- Which SKUs are overstocked?
- Which products have high sales but low inventory?
- Which purchase orders are delayed?
- Which stock transfers are stuck in transit?
- Which products have high return rates?
- Which stores and products are most profitable?

## Architecture Explanation

The project follows a production-style Azure architecture.

Source files are first placed in the landing zone of Azure Data Lake. Azure Data Factory validates the required files using metadata checks and control flow logic. Valid files are moved into the raw zone.

Azure Databricks processes the data using the Medallion Architecture. The Bronze layer stores raw ingested data. The Silver layer cleans, validates, deduplicates, and flattens the data. The Gold layer creates business-ready fact and dimension tables.

The final Gold tables are loaded into Azure SQL Database, which acts as the analytics serving layer for reporting and Power BI.

## Technologies Used

This project uses:

- Azure Data Lake / Blob Storage
- Azure Data Factory
- Azure Databricks
- PySpark
- Delta Lake
- Azure SQL Database
- GitHub
- Power BI-ready warehouse design

## Data Engineering Features

The project includes:

- Source file validation
- Landing, raw, archive, rejected, and processed zones
- Bronze, Silver, and Gold layers
- Nested JSON flattening
- Data quality rules
- Fact and dimension modeling
- SQL validation queries
- GitHub version control
- Production-style pipeline design

## Final Summary

This project demonstrates how to build a production-style retail data platform on Azure. It shows cloud storage design, orchestration with Azure Data Factory, transformation with Azure Databricks, warehouse modeling with Azure SQL, and documentation through GitHub.