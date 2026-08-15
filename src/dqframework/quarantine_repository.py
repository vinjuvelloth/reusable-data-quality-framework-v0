"""
==================================================
Reusable Data Quality Framework
Module      : quarantine_repository.py
Purpose     : Persists failed records to the quarantine table
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, current_timestamp, lit, struct, to_json

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_logger import FrameworkLogger


class QuarantineRepository:

    def __init__(self, spark: SparkSession) -> None:

        self.spark = spark
        self.config = FrameworkConfig.get()
        self.logger = FrameworkLogger.get_logger(__name__)

        self.catalog = self.config["environment"]["catalog"]
        self.schema = self.config["environment"]["schema"]

        self.quarantine_table = (
            f"{self.catalog}.{self.schema}."
            f"{self.config['metadata']['quarantine']}"
        )

    def save_failed_records(
        self,
        run_id: str,
        source_table: str,
        failed_df: DataFrame | None
    ) -> None:

        if failed_df is None:
            self.logger.info("No failed records found.")
            return

        failed_count = failed_df.count()

        if failed_count == 0:
            self.logger.info("No failed records found.")
            return

        self.logger.info(
            "Writing %s failed records to %s.",
            failed_count,
            self.quarantine_table
        )

        metadata_columns = {
            "failed_rule",
            "failed_column",
            "failed_reason"
        }

        source_columns = [
            c for c in failed_df.columns
            if c not in metadata_columns
        ]

        quarantine_df = (
            failed_df
            .select(
                lit(run_id).alias("run_id"),
                lit(source_table).alias("source_table"),
                col("failed_rule"),
                col("failed_column"),
                col("failed_reason"),
                to_json(struct(*[col(c) for c in source_columns])).alias("record_data_json"),
                current_timestamp().alias("created_timestamp")
            )
        )

        (
            quarantine_df.write
            .mode("append")
            .saveAsTable(self.quarantine_table)
        )

        self.logger.info("Quarantine write completed.")