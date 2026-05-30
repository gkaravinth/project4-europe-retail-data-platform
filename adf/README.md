# Azure Data Factory Artifacts

This folder contains Azure Data Factory artifacts for Project 4 - Europe Retail Data Platform.

## Pipelines

### DEV Pipeline

`pl_dev_project4_ingest_landing_to_gold`

Purpose:

- Validate source files in the landing zone
- Copy valid files from landing to raw
- Trigger Databricks Bronze notebook
- Trigger Databricks Silver notebook
- Trigger Databricks Gold notebook

### PROD Pipeline

`pl_prod_project4_ingest_landing_to_gold`

Purpose:

- Production-style orchestration pipeline
- Runs the same end-to-end flow from landing validation to Gold table creation
- Used to demonstrate DEV and PROD pipeline separation

## Pipeline Flow

```text
Landing Zone
    ↓
Get Metadata file checks
    ↓
If Condition: all required files exist
    ↓
Copy Data activities: landing to raw
    ↓
Databricks Notebook: Bronze ingestion
    ↓
Databricks Notebook: Silver cleaning
    ↓
Databricks Notebook: Gold business tables


Linked Services
Azure Blob Storage

ls_p4_blob_europedata

Used by ADF to access the Azure Storage container for landing and raw files.

Azure Databricks

AzureDatabricks1

Used by ADF to trigger Databricks notebooks for Bronze, Silver, and Gold processing.

Security Note

Real Azure Storage keys and Databricks access tokens are not stored in this repository.

Secrets are replaced with placeholders such as:

<REPLACE_WITH_SECRET>
<REPLACE_WITH_DATABRICKS_TOKEN>
<REPLACE_WITH_CLUSTER_ID>

In production, credentials should be managed through:

Azure Key Vault
Managed Identity
Databricks Secret Scope
Service Principal authentication
Role-based access control