# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# Databricks notebook source
"""
==================================================
Reusable Data Quality Framework
Notebook    : 04_view_results.py
Purpose     : Display framework execution results
Author      : Vinju Velloth
Version     : v0
==================================================
"""

import os
import sys

# --------------------------------------------------
# Add project src folder to Python path
# --------------------------------------------------

repo_root = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
src_path = os.path.join(repo_root, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"Repository : {repo_root}")
print(f"Source Path: {src_path}")

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_logger import FrameworkLogger

logger = FrameworkLogger.get_logger(__name__)
config = FrameworkConfig.get()

catalog = config["environment"]["catalog"]
framework_schema = config["environment"]["schema"]

print("=" * 70)
print(config["framework"]["name"])
print("Execution Results")
print("=" * 70)

print("\nExecution Audit")
display(
    spark.sql(f"""
        SELECT *
        FROM {catalog}.{framework_schema}.dq_execution_audit
        ORDER BY created_timestamp DESC
    """)
)

print("\nExecution Summary")
display(
    spark.sql(f"""
        SELECT
            status,
            COUNT(*) AS executions,
            SUM(total_records) AS total_records,
            SUM(passed_records) AS passed_records,
            SUM(failed_records) AS failed_records
        FROM {catalog}.{framework_schema}.dq_execution_audit
        GROUP BY status
    """)
)

print("\nValidation Rule Summary")
display(
    spark.sql(f"""
        SELECT
            rule_set,
            COUNT(*) AS total_rules
        FROM {catalog}.{framework_schema}.dq_rule_master
        GROUP BY rule_set
        ORDER BY rule_set
    """)
)

print("\nQuarantine Records")
display(
    spark.sql(f"""
        SELECT *
        FROM {catalog}.{framework_schema}.dq_quarantine_data
        ORDER BY created_timestamp DESC
    """)
)

print("\nQuarantine Summary")
display(
    spark.sql(f"""
        SELECT
            source_table,
            failed_rule,
            COUNT(*) AS failed_records
        FROM {catalog}.{framework_schema}.dq_quarantine_data
        GROUP BY source_table, failed_rule
        ORDER BY source_table, failed_rule
    """)
)

print("\nBronze Tables")
display(
    spark.sql(f"SHOW TABLES IN {catalog}.bronze")
)

print("\nSilver Tables")
display(
    spark.sql(f"SHOW TABLES IN {catalog}.silver")
)

logger.info("Framework reporting completed successfully.")

print("=" * 70)
print("Reporting completed.")
print("=" * 70)