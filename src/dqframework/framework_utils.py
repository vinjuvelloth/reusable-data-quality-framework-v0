"""
==================================================
Reusable Data Quality Framework
Module      : framework_utils.py
Purpose     : Common utility functions used across the framework
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

from dqframework.framework_config import FrameworkConfig


class FrameworkUtils:
    """
    Common utility functions used across the framework.
    """

    @staticmethod
    def get_project_root() -> Path:
        """
        Returns project root folder.
        """
        return Path(__file__).resolve().parents[2]

    @staticmethod
    def generate_run_id() -> str:
        """
        Generates unique framework execution id.
        """
        return uuid.uuid4().hex.upper()

    @staticmethod
    def current_timestamp() -> datetime:
        """
        Returns current timestamp.
        """
        return datetime.now()

    @staticmethod
    def get_framework_name() -> str:
        """
        Returns framework name.
        """
        config = FrameworkConfig.get()
        return config["framework"]["name"]

    @staticmethod
    def get_framework_version() -> str:
        """
        Returns framework version.
        """
        config = FrameworkConfig.get()
        return config["framework"]["version"]