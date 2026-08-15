"""
==================================================
Reusable Data Quality Framework
Module      : validation_engine.py
Purpose     : Executes metadata-driven validation rules
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit

from dqframework.framework_logger import FrameworkLogger
from dqframework.models.validation_result import ValidationResult


class ValidationEngine:
    """
    Executes data quality validation rules.
    """

    def __init__(self) -> None:
        self.logger = FrameworkLogger.get_logger(__name__)

    def validate(
        self,
        dataframe: DataFrame,
        rules: DataFrame
    ) -> ValidationResult:
        """
        Executes all validation rules.

        Parameters
        ----------
        dataframe : DataFrame
        rules : DataFrame

        Returns
        -------
        ValidationResult
        """

        self.logger.info("Starting validation.")

        valid_df = dataframe
        failed_df = None

        for rule in rules.collect():

            column_name = rule.column_name
            rule_type = rule.rule_type
            rule_value = rule.rule_value

            if rule_type == "NOT_NULL":

                invalid = valid_df.filter(col(column_name).isNull())
                valid_df = valid_df.filter(col(column_name).isNotNull())

            elif rule_type == "UNIQUE":

                duplicate_keys = (
                    valid_df
                    .groupBy(column_name)
                    .count()
                    .filter("count > 1")
                    .select(column_name)
                )

                invalid = valid_df.join(
                    duplicate_keys,
                    column_name
                )

                valid_df = valid_df.join(
                    duplicate_keys,
                    column_name,
                    "left_anti"
                )

            elif rule_type == "RANGE":

                minimum, maximum = [
                    int(value)
                    for value in rule_value.split(",")
                ]

                invalid = valid_df.filter(
                    (col(column_name) < minimum) |
                    (col(column_name) > maximum)
                )

                valid_df = valid_df.filter(
                    (col(column_name) >= minimum) &
                    (col(column_name) <= maximum)
                )

            elif rule_type == "EMAIL":

                invalid = valid_df.filter(
                    ~col(column_name).contains("@")
                )

                valid_df = valid_df.filter(
                    col(column_name).contains("@")
                )

            elif rule_type == "SET":

                values = [
                    value.strip()
                    for value in rule_value.split(",")
                ]

                invalid = valid_df.filter(
                    ~col(column_name).isin(values)
                )

                valid_df = valid_df.filter(
                    col(column_name).isin(values)
                )

            else:
                self.logger.warning(
                    "Unsupported rule type: %s",
                    rule_type
                )
                continue

            invalid = (
                invalid
                .withColumn("failed_rule", lit(rule_type))
                .withColumn("failed_column", lit(column_name))
                .withColumn(
                    "failed_reason",
                    lit(f"{rule_type} validation failed")
                )
            )

            if failed_df is None:
                failed_df = invalid
            else:
                failed_df = failed_df.unionByName(
                    invalid,
                    allowMissingColumns=True
                )

        summary = {
            "total_records": dataframe.count(),
            "passed_records": valid_df.count(),
            "failed_records": (
                0
                if failed_df is None
                else failed_df.count()
            )
        }

        self.logger.info("Validation completed.")

        return ValidationResult(
            valid_df=valid_df,
            failed_df=failed_df,
            summary=summary
        )