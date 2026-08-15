# Databricks notebook source
"""
==================================================
Reusable Data Quality Framework
Notebook    : 01_setup_environment.py
Purpose     : Verify framework environment
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_logger import FrameworkLogger

logger = FrameworkLogger.get_logger(__name__)
config = FrameworkConfig.get()

catalog = config["environment"]["catalog"]
schema = config["environment"]["schema"]
volume = config["environment"]["volume"]

spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

print("=" * 60)
print("Reusable Data Quality Framework")
print("=" * 60)
print(f"Catalog : {catalog}")
print(f"Schema  : {schema}")
print(f"Volume  : {volume}")
print("=" * 60)

required_tables = [
    config["metadata"]["rule_master"],
    config["metadata"]["execution_master"],
    config["metadata"]["execution_audit"],
    config["metadata"]["quarantine"]
]

tables = [
    row.tableName
    for row in spark.sql("SHOW TABLES").collect()
]

print("\nFramework Tables")
print("-" * 60)

for table in required_tables:
    status = "FOUND" if table in tables else "MISSING"
    print(f"{table:<35} {status}")

print("\nVolumes")
print("-" * 60)

volumes = [
    row.volume_name
    for row in spark.sql("SHOW VOLUMES").collect()
]

status = "FOUND" if volume in volumes else "MISSING"
print(f"{volume:<35} {status}")

print("\nEnvironment verification completed.")

logger.info("Framework environment verified successfully.")