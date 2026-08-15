# \# Reusable Data Quality Framework

# 

# A metadata-driven Data Quality Framework for Databricks Lakehouse built using Python, PySpark and Unity Catalog.

# 

# \---

# 

# \## Overview

# 

# The Reusable Data Quality Framework provides a configurable and extensible approach for validating datasets using metadata rather than hardcoded business rules.

# 

# The framework separates configuration, metadata, validation logic and orchestration into independent components, allowing new datasets and validation rules to be added with minimal code changes.

# 

# \---

# 

# \## Objectives

# 

# \- Metadata-driven validation

# \- Reusable across multiple datasets

# \- Unity Catalog compatible

# \- Serverless compatible

# \- Enterprise architecture

# \- Extensible rule engine

# \- Production-ready code structure

# 

# \---

# 

# \## Current Features

# 

# \- Metadata-driven execution

# \- Rule-based validation

# \- Framework configuration

# \- Centralized logging

# \- Validation orchestration

# \- Execution audit

# \- Failed record quarantine

# \- Multiple execution plans

# \- Multiple rule sets

# 

# \---

# 

# \## Supported Rule Types

# 

# | Rule | Description |

# |-------|-------------|

# | NOT\_NULL | Mandatory column validation |

# | UNIQUE | Duplicate value detection |

# | RANGE | Numeric range validation |

# | EMAIL | Email format validation |

# | SET | Allowed value validation |

# 

# \---

# 

# \## Repository Structure

# 

# ```text

# reusable-data-quality-framework-v0

# │

# ├── config

# ├── deployment

# ├── docs

# ├── examples

# ├── logs

# ├── notebooks

# ├── sample\_data

# ├── scripts

# ├── sql

# ├── src

# │   └── dqframework

# └── tests

# ```

# 

# \---

# 

# \## Framework Components

# 

# \- FrameworkConfig

# \- FrameworkUtils

# \- FrameworkLogger

# \- MetadataRepository

# \- ValidationEngine

# \- QuarantineRepository

# \- AuditRepository

# \- FrameworkOrchestrator

# 

# \---

# 

# \## Metadata Tables

# 

# | Table | Purpose |

# |--------|---------|

# | dq\_rule\_master | Validation rule definitions |

# | dq\_execution\_master | Execution plan definitions |

# | dq\_execution\_audit | Execution history |

# | dq\_quarantine\_data | Failed records |

# 

# \---

# 

# \## Technology Stack

# 

# \- Databricks

# \- Unity Catalog

# \- Python

# \- PySpark

# \- SQL

# \- Delta Lake

# \- Git

# \- VS Code

# 

# \---

# 

# \## Development Workflow

# 

# ```text

# VS Code

# 

# ↓

# 

# GitHub

# 

# ↓

# 

# Databricks Repo

# 

# ↓

# 

# Run SQL

# 

# ↓

# 

# Run Notebooks

# 

# ↓

# 

# Validate

# 

# ↓

# 

# Release

# ```

# 

# \---

# 

# \## Project Status

# 

# Current Version

# 

# ```text

# v0

# ```

# 

# Current Phase

# 

# ```text

# Framework Development

# ```

# 

# \---

# 

# \## Roadmap

# 

# \### Release 1

# 

# \- Repository

# \- Framework

# \- SQL

# 

# \### Release 2

# 

# \- Documentation

# 

# \### Release 3

# 

# \- Databricks Deployment

# 

# \### Release 4

# 

# \- Testing

# \- Final Release

# 

# \---

# 

# \## License

# 

# This project is released under the MIT License.

