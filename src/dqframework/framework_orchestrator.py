"""
==================================================
Reusable Data Quality Framework
Module      : framework_orchestrator.py
Purpose     : Coordinates framework execution
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

import time

from pyspark.sql import SparkSession

from dqframework.framework_logger import FrameworkLogger
from dqframework.framework_utils import FrameworkUtils
from dqframework.metadata_repository import MetadataRepository
from dqframework.validation_engine import ValidationEngine
from dqframework.quarantine_repository import QuarantineRepository
from dqframework.audit_repository import AuditRepository


class FrameworkOrchestrator:
    """
    Coordinates the execution of the Data Quality Framework.
    """

    def __init__(self, spark: SparkSession) -> None:

        self.spark = spark
        self.logger = FrameworkLogger.get_logger(__name__)

        self.metadata_repository = MetadataRepository(spark)
        self.validation_engine = ValidationEngine()
        self.quarantine_repository = QuarantineRepository(spark)
        self.audit_repository = AuditRepository(spark)

    def run(self) -> None:
        """
        Executes all active execution plans.
        """

        self.logger.info("Framework execution started.")

        execution_plans = (
            self.metadata_repository
            .get_active_execution_plans()
            .collect()
        )

        if len(execution_plans) == 0:
            self.logger.warning("No active execution plans found.")
            return

        for plan in execution_plans:

            run_id = FrameworkUtils.generate_run_id()

            source_table = (
                f"{plan.source_catalog}."
                f"{plan.source_schema}."
                f"{plan.source_table}"
            )

            target_table = (
                f"{plan.target_catalog}."
                f"{plan.target_schema}."
                f"{plan.target_table}"
            )

            rule_set = plan.rule_set

            self.logger.info("------------------------------------------")
            self.logger.info("Run Id      : %s", run_id)
            self.logger.info("Source      : %s", source_table)
            self.logger.info("Target      : %s", target_table)
            self.logger.info("Rule Set    : %s", rule_set)

            start_time = time.time()

            status = "SUCCESS"

            try:

                source_df = self.spark.table(source_table)

                rules_df = self.metadata_repository.get_rules(rule_set)

                result = self.validation_engine.validate(
                    source_df,
                    rules_df
                )

                (
                    result.valid_df.write
                    .mode("overwrite")
                    .saveAsTable(target_table)
                )

                self.quarantine_repository.save_failed_records(run_id=run_id,source_table=source_table,
                    failed_df=result.failed_df
                ) 

            except Exception as ex:

                status = "FAILED"

                self.logger.exception(ex)

                result = None

            execution_time = round(
                time.time() - start_time,
                2
            )

            summary = (
                result.summary
                if result
                else {
                    "total_records": 0,
                    "passed_records": 0,
                    "failed_records": 0
                }
            )

            self.audit_repository.save_execution_audit(
                run_id=run_id,
                source_table=source_table,
                summary=summary,
                execution_time_seconds=execution_time,
                status=status
            )

        self.logger.info("Framework execution completed.")