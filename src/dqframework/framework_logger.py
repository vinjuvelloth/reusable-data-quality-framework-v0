"""
==================================================
Reusable Data Quality Framework
Module      : framework_logger.py
Purpose     : Central logging utility
Author      : Vinju Velloth
Version     : v0
==================================================
"""

from __future__ import annotations

import logging

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_utils import FrameworkUtils


class FrameworkLogger:
    """
    Creates framework loggers.
    """

    @staticmethod
    def get_logger(name: str) -> logging.Logger:

        config = FrameworkConfig.get()

        log_directory = (
            FrameworkUtils.get_project_root()
            / config["logging"]["log_directory"]
        )

        log_directory.mkdir(parents=True, exist_ok=True)

        log_file = log_directory / "framework.log"

        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(
            getattr(logging, config["logging"]["level"])
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.propagate = False

        return logger