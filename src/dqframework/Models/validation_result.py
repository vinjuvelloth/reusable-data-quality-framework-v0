"""
==================================================
Reusable Data Quality Framework
Module      : validation_result.py
Purpose     : Validation result model
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pyspark.sql import DataFrame


@dataclass
class ValidationResult:
    """
    Stores the outcome of a validation execution.
    """

    valid_df: DataFrame
    failed_df: DataFrame | None
    summary: dict[str, Any]