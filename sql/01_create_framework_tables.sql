--==================================================
-- Reusable Data Quality Framework
-- Framework Setup
-- Version : v0
--==================================================

CREATE CATALOG IF NOT EXISTS dq_framework;

CREATE SCHEMA IF NOT EXISTS dq_framework.framework;
CREATE SCHEMA IF NOT EXISTS dq_framework.bronze;
CREATE SCHEMA IF NOT EXISTS dq_framework.silver;

USE CATALOG dq_framework;
USE SCHEMA framework;

CREATE VOLUME IF NOT EXISTS demo_files;

CREATE TABLE IF NOT EXISTS dq_rule_master(
rule_id BIGINT GENERATED ALWAYS AS IDENTITY,
rule_set STRING,
column_name STRING,
rule_type STRING,
rule_value STRING,
severity STRING,
active STRING,
created_timestamp TIMESTAMP,
updated_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dq_execution_master(
execution_id BIGINT GENERATED ALWAYS AS IDENTITY,
source_catalog STRING,
source_schema STRING,
source_table STRING,
target_catalog STRING,
target_schema STRING,
target_table STRING,
rule_set STRING,
write_mode STRING,
active STRING,
created_timestamp TIMESTAMP,
updated_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dq_execution_audit(
run_id STRING,
source_table STRING,
total_records BIGINT,
passed_records BIGINT,
failed_records BIGINT,
status STRING,
execution_time_seconds DOUBLE,
created_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dq_quarantine_data(
run_id STRING,
source_table STRING,
failed_rule STRING,
failed_column STRING,
failed_reason STRING,
record_data_json STRING,
created_timestamp TIMESTAMP
);

SHOW SCHEMAS;
SHOW TABLES;
SHOW VOLUMES;