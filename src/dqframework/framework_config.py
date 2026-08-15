"""
==================================================
Reusable Data Quality Framework
Module      : framework_config.py
Purpose     : Framework configuration manager
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class FrameworkConfig:
    """Loads and caches framework configuration."""

    _config: dict[str, Any] | None = None

    @staticmethod
    def get() -> dict[str, Any]:
        """
        Returns framework configuration.

        Returns
        -------
        dict
        """

        if FrameworkConfig._config is None:

            project_root = Path(__file__).resolve().parents[2]

            config_file = (
                project_root
                / "config"
                / "framework.yml"
            )

            with open(config_file, "r", encoding="utf-8") as file:
                FrameworkConfig._config = yaml.safe_load(file)

        return FrameworkConfig._config

    @staticmethod
    def reload() -> None:
        """
        Reload configuration.
        """

        FrameworkConfig._config = None