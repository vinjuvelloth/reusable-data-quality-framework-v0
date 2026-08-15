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