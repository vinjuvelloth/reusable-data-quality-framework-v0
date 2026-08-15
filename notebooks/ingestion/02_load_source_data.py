# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# Databricks notebook source
"""
==================================================
Reusable Data Quality Framework
Notebook    : 02_load_source_data.py
Purpose     : Load source CSV files into Bronze tables
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
from dqframework.metadata_repository import MetadataRepository

logger = FrameworkLogger.get_logger(__name__)
config = FrameworkConfig.get()

catalog = config["environment"]["catalog"]
framework_schema = config["environment"]["schema"]
volume = config["environment"]["volume"]

metadata_repository = MetadataRepository(spark)

logger.info("Starting Bronze data ingestion.")

execution_plans = (
    metadata_repository
    .get_active_execution_plans()
    .collect()
)

if len(execution_plans) == 0:
    print("No active execution plans found.")
else:

    for plan in execution_plans:

        source_file = (
            f"/Volumes/"
            f"{catalog}/"
            f"{framework_schema}/"
            f"{volume}/"
            f"{plan.source_table}.csv"
        )

        bronze_table = (
            f"{plan.source_catalog}."
            f"{plan.source_schema}."
            f"{plan.source_table}"
        )

        print("=" * 70)
        print(f"Source File : {source_file}")
        print(f"Bronze Table: {bronze_table}")

        df = (
            spark.read
                 .option("header", True)
                 .option("inferSchema", True)
                 .csv(source_file)
        )

        (
            df.write
              .mode("overwrite")
              .saveAsTable(bronze_table)
        )

        record_count = df.count()

        print(f"Records Loaded : {record_count}")

        logger.info(
            "Loaded %s records into %s.",
            record_count,
            bronze_table
        )

print("=" * 70)
print("Bronze ingestion completed.")

logger.info("Bronze ingestion completed.")