"""
==================================================
Reusable Data Quality Framework
Module      : metadata_repository.py
Purpose     : Read framework metadata from Databricks
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_logger import FrameworkLogger


class MetadataRepository:
    """
    Repository responsible for reading framework metadata.
    """

    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark
        self.config = FrameworkConfig.get()
        self.logger = FrameworkLogger.get_logger(__name__)

        self.catalog = self.config["environment"]["catalog"]
        self.schema = self.config["environment"]["schema"]

        self.rule_master_table = (
            f"{self.catalog}.{self.schema}."
            f"{self.config['metadata']['rule_master']}"
        )

        self.execution_master_table = (
            f"{self.catalog}.{self.schema}."
            f"{self.config['metadata']['execution_master']}"
        )

    def get_active_execution_plans(self) -> DataFrame:
        """
        Returns all active execution plans.

        Returns
        -------
        DataFrame
        """

        self.logger.info("Loading active execution plans.")

        query = f"""
        SELECT *
        FROM {self.execution_master_table}
        WHERE active='Y'
        ORDER BY execution_id
        """

        return self.spark.sql(query)

    def get_rules(self, rule_set: str) -> DataFrame:
        """
        Returns active rules for a rule set.

        Parameters
        ----------
        rule_set : str

        Returns
        -------
        DataFrame
        """

        self.logger.info(
            "Loading rules for rule set: %s",
            rule_set
        )

        query = f"""
        SELECT
            rule_id,
            rule_set,
            column_name,
            rule_type,
            rule_value,
            severity,
            active
        FROM {self.rule_master_table}
        WHERE rule_set='{rule_set}'
          AND active='Y'
        ORDER BY rule_id
        """

        return self.spark.sql(query)