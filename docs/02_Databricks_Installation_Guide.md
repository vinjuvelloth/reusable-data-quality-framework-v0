# Databricks Installation Guide

## Reusable Data Quality Framework

Version : v0

---

# Purpose

This document describes the complete installation and deployment procedure for the Reusable Data Quality Framework in a Databricks Unity Catalog environment.

The steps below reflect the validated MVP deployment process.

---

# Prerequisites

## Databricks

- Unity Catalog Enabled Workspace
- Git Integration Enabled
- Serverless or Standard Compute
- SQL Editor Access
- Unity Catalog Permissions

---

## GitHub

Create a GitHub repository containing the project.

Example

```
reusable-data-quality-framework-v0
```

Push the latest project into GitHub.

---

# Step 1 - Clone Repository

Open

Workspace

↓

Repos

↓

Create Repo

Select

- Git Provider
- Repository URL

Clone the repository.

Expected structure

```
Repos/

    reusable-data-quality-framework-v0/

        config/

        docs/

        notebooks/

        sample_data/

        scripts/

        sql/

        src/

        tests/
```

---

# Step 2 - Create Framework Objects

Execute

```
sql/01_create_framework_tables.sql
```

This script creates

- Catalog
- Schemas
- Volume
- Metadata Tables
- Audit Tables
- Quarantine Tables

Verify

```
SHOW CATALOGS;

SHOW SCHEMAS IN dq_framework;
```

---

# Step 3 - Load Framework Metadata

Execute

```
sql/02_load_sample_metadata.sql
```

This loads

- Execution Plans
- Validation Rules

Verify

```
SELECT COUNT(*)
FROM dq_framework.framework.dq_execution_master;
```

Expected

```
4
```

Verify

```
SELECT COUNT(*)
FROM dq_framework.framework.dq_rule_master;
```

Expected

```
21
```

---

# Step 4 - Upload Sample Files

Upload the contents of

```
sample_data/
```

to

```
/Volumes/dq_framework/framework/demo_files/
```

Files

```
customer_master.csv

employee_master.csv

sales_orders.csv

product_master.csv
```

---

# Step 5 - Execute Setup Notebook

Run

```
notebooks/setup/01_setup_environment.py
```

Expected

- Repository located
- Framework tables found
- Volume found
- Environment verification completed

---

# Step 6 - Execute Ingestion Notebook

Run

```
notebooks/ingestion/02_load_source_data.py
```

Purpose

Loads every configured CSV file into Bronze tables.

The notebook reads metadata from

```
dq_execution_master
```

No code changes are required to onboard new datasets.

---

# Step 7 - Execute Framework

Run

```
notebooks/execution/03_execute_framework.py
```

Framework Activities

- Load execution plans
- Load validation rules
- Validate records
- Write valid records to Silver
- Write failed records to Quarantine
- Write Execution Audit

---

# Step 8 - View Results

Run

```
notebooks/reporting/04_view_results.py
```

Displays

- Execution Audit
- Rule Summary
- Quarantine Records
- Quarantine Summary
- Bronze Tables
- Silver Tables

---

# Step 9 - Verify Execution Audit

Run

```sql
SELECT
    source_table,
    status,
    total_records,
    passed_records,
    failed_records
FROM dq_framework.framework.dq_execution_audit;
```

Expected

| Dataset | Status |
|----------|---------|
| Customer | SUCCESS |
| Employee | SUCCESS |
| Sales | SUCCESS |
| Product | SUCCESS |

---

# Step 10 - Verify Silver Tables

Run

```sql
SELECT 'customer_master',COUNT(*) FROM dq_framework.silver.customer_master
UNION ALL
SELECT 'employee_master',COUNT(*) FROM dq_framework.silver.employee_master
UNION ALL
SELECT 'sales_orders',COUNT(*) FROM dq_framework.silver.sales_orders
UNION ALL
SELECT 'product_master',COUNT(*) FROM dq_framework.silver.product_master;
```

Expected

| Table | Records |
|--------|---------|
| customer_master | 3 |
| employee_master | 1 |
| sales_orders | 3 |
| product_master | 2 |

---

# Step 11 - Verify Quarantine

```sql
SELECT *
FROM dq_framework.framework.dq_quarantine_data;
```

Expected

Failed records should be available together with

- Run ID
- Source Table
- Failed Rule
- Failed Column
- Failed Reason
- Record JSON

---

# Step 12 - Verify Audit

```sql
SELECT *
FROM dq_framework.framework.dq_execution_audit;
```

Expected

One audit record for every execution plan.

---

# MVP Results

The framework successfully demonstrated

- Metadata Driven Validation
- Multiple Dataset Processing
- Dynamic Rule Loading
- Bronze to Silver Processing
- Failed Record Quarantine
- Execution Audit
- Unity Catalog Integration
- Delta Lake Integration
- Databricks Repos Integration

---

# Repository Execution Order

```
GitHub

↓

Databricks Repo

↓

Execute SQL

↓

Upload CSV Files

↓

Setup Notebook

↓

Ingestion Notebook

↓

Execution Notebook

↓

Reporting Notebook

↓

Validate Results
```

---

# MVP Status

```
SUCCESS
```