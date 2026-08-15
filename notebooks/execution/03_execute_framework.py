# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# Databricks notebook source
"""
==================================================
Reusable Data Quality Framework
Notebook    : 03_execute_framework.py
Purpose     : Execute the Data Quality Framework
Author      : Vinju Velloth
Version     : v0
==================================================
"""

import os
import sys

# --------------------------------------------------
# Add project src folder to Python path
# --------------------------------------------------

repo_root = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
src_path = os.path.join(repo_root, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"Repository : {repo_root}")
print(f"Source Path: {src_path}")

from dqframework.framework_config import FrameworkConfig
from dqframework.framework_logger import FrameworkLogger
from dqframework.framework_orchestrator import FrameworkOrchestrator

logger = FrameworkLogger.get_logger(__name__)
config = FrameworkConfig.get()

print("=" * 60)
print(config["framework"]["name"])
print(f"Version : {config['framework']['version']}")
print("=" * 60)

logger.info("Framework execution started.")

framework = FrameworkOrchestrator(spark)

framework.run()

logger.info("Framework execution completed.")

print("=" * 60)
print("Framework execution completed successfully.")
print("=" * 60)