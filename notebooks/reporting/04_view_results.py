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

# --------------------------------------------------
# Execution Audit
# --------------------------------------------------

print("\nExecution Audit")
print("-" * 70)

display(
    spark.sql(f"""
        SELECT *
        FROM {catalog}.{framework_schema}.dq_execution_audit
        ORDER BY created_timestamp DESC
    """)
)

# --------------------------------------------------
# Execution Summary
# --------------------------------------------------

print("\nExecution Summary")
print("-" * 70)

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

# --------------------------------------------------
# Rule Summary
# --------------------------------------------------

print("\nValidation Rule Summary")
print("-" * 70)

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

# --------------------------------------------------
# Quarantine Records
# --------------------------------------------------

print("\nQuarantine Records")
print("-" * 70)

display(
    spark.sql(f"""
        SELECT *
        FROM {catalog}.{framework_schema}.dq_quarantine_data
        ORDER BY created_timestamp DESC
    """)
)

# --------------------------------------------------
# Quarantine Summary
# --------------------------------------------------

print("\nQuarantine Summary")
print("-" * 70)

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

# --------------------------------------------------
# Bronze Tables
# --------------------------------------------------

print("\nBronze Tables")
print("-" * 70)

display(
    spark.sql(f"SHOW TABLES IN {catalog}.bronze")
)

# --------------------------------------------------
# Silver Tables
# --------------------------------------------------

print("\nSilver Tables")
print("-" * 70)

display(
    spark.sql(f"SHOW TABLES IN {catalog}.silver")
)

logger.info("Framework reporting completed successfully.")

print("=" * 70)
print("Reporting completed.")
print("=" * 70)