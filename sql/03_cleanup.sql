--==================================================
-- Reusable Data Quality Framework
-- Cleanup Script
-- Version : v0
--==================================================

USE CATALOG dq_framework;
USE SCHEMA framework;

-- Clear Framework Tables
TRUNCATE TABLE dq_execution_audit;
TRUNCATE TABLE dq_quarantine_data;
TRUNCATE TABLE dq_execution_master;
TRUNCATE TABLE dq_rule_master;

-- Remove Sample Silver Tables
DROP TABLE IF EXISTS dq_framework.silver.customer_master;
DROP TABLE IF EXISTS dq_framework.silver.employee_master;
DROP TABLE IF EXISTS dq_framework.silver.sales_orders;
DROP TABLE IF EXISTS dq_framework.silver.product_master;

-- Remove Sample Bronze Tables
DROP TABLE IF EXISTS dq_framework.bronze.customer_master;
DROP TABLE IF EXISTS dq_framework.bronze.employee_master;
DROP TABLE IF EXISTS dq_framework.bronze.sales_orders;
DROP TABLE IF EXISTS dq_framework.bronze.product_master;

-- Verification
SELECT 'Framework cleanup completed.' AS status;