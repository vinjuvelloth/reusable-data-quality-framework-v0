--==================================================
-- Reusable Data Quality Framework
-- Validation Queries
-- Version : v0
--==================================================

USE CATALOG dq_framework;
USE SCHEMA framework;

-- Metadata
SELECT * FROM dq_execution_master ORDER BY execution_id;
SELECT * FROM dq_rule_master ORDER BY rule_set,rule_id;

-- Metadata Summary
SELECT rule_set,COUNT(*) AS total_rules
FROM dq_rule_master
GROUP BY rule_set
ORDER BY rule_set;

SELECT source_table,target_table,rule_set,active
FROM dq_execution_master
ORDER BY execution_id;

-- Audit
SELECT *
FROM dq_execution_audit
ORDER BY created_timestamp DESC;

SELECT
status,
COUNT(*) AS executions,
SUM(total_records) AS total_records,
SUM(passed_records) AS passed_records,
SUM(failed_records) AS failed_records
FROM dq_execution_audit
GROUP BY status;

-- Quarantine
SELECT *
FROM dq_quarantine_data
ORDER BY created_timestamp DESC;

SELECT
source_table,
failed_rule,
COUNT(*) AS failed_records
FROM dq_quarantine_data
GROUP BY source_table,failed_rule
ORDER BY source_table,failed_rule;

-- Silver Tables
SHOW TABLES IN dq_framework.silver;

SELECT COUNT(*) AS customer_count
FROM dq_framework.silver.customer_master;

SELECT COUNT(*) AS employee_count
FROM dq_framework.silver.employee_master;

SELECT COUNT(*) AS sales_count
FROM dq_framework.silver.sales_orders;

SELECT COUNT(*) AS product_count
FROM dq_framework.silver.product_master;