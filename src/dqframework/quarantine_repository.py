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

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_logger import FrameworkLogger


class QuarantineRepository:
    """
    Repository responsible for writing failed records
    to the quarantine table.
    """

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
        failed_df: DataFrame | None
    ) -> None:
        """
        Saves failed records into the quarantine table.

        Parameters
        ----------
        failed_df : DataFrame | None
            DataFrame containing failed records.
        """

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

        (
            failed_df.write
            .mode("append")
            .saveAsTable(self.quarantine_table)
        )

        self.logger.info("Quarantine write completed.")