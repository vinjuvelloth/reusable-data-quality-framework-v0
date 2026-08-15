"""
==================================================
Reusable Data Quality Framework
Module      : audit_repository.py
Purpose     : Persists framework execution audit
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    DoubleType,
    TimestampType
)

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_logger import FrameworkLogger
from dqframework.framework_utils import FrameworkUtils


class AuditRepository:
    """
    Repository responsible for writing execution audit.
    """

    def __init__(self, spark: SparkSession) -> None:

        self.spark = spark
        self.config = FrameworkConfig.get()
        self.logger = FrameworkLogger.get_logger(__name__)

        self.catalog = self.config["environment"]["catalog"]
        self.schema = self.config["environment"]["schema"]

        self.audit_table = (
            f"{self.catalog}.{self.schema}."
            f"{self.config['metadata']['execution_audit']}"
        )

    def save_execution_audit(
        self,
        run_id: str,
        source_table: str,
        summary: dict,
        execution_time_seconds: float,
        status: str
    ) -> None:
        """
        Writes execution audit into audit table.
        """

        schema = StructType([
            StructField("run_id", StringType(), False),
            StructField("source_table", StringType(), False),
            StructField("total_records", LongType(), False),
            StructField("passed_records", LongType(), False),
            StructField("failed_records", LongType(), False),
            StructField("status", StringType(), False),
            StructField("execution_time_seconds", DoubleType(), False),
            StructField("created_timestamp", TimestampType(), False)
        ])

        data = [(
            run_id,
            source_table,
            summary["total_records"],
            summary["passed_records"],
            summary["failed_records"],
            status,
            execution_time_seconds,
            FrameworkUtils.current_timestamp()
        )]

        audit_df = self.spark.createDataFrame(
            data=data,
            schema=schema
        )

        self.logger.info(
            "Writing execution audit for run %s.",
            run_id
        )

        (
            audit_df.write
            .mode("append")
            .saveAsTable(self.audit_table)
        )

        self.logger.info("Execution audit completed.")