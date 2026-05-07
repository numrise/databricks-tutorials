# Databricks

Complete guides for working with the Databricks platform.

## What is Databricks?

Databricks is a unified analytics platform built on Apache Spark that simplifies:
- **Data Engineering** - Build reliable pipelines
- **Data Analytics** - Query data with SQL
- **Machine Learning** - Train and deploy models
- **Collaboration** - Work as a team

## Key Features

- Collaborative Notebooks
- Managed Clusters
- Delta Lake for ACID transactions
- MLflow for ML lifecycle
- Workflows for orchestration
- Unity Catalog for data governance

## Getting Started

- [Getting Started](index.md) - Platform overview
- [Setup Guide](setup.md) - Initial configuration
- [Workspace & Clusters](workspace.md) - Managing infrastructure
- [Notebooks](notebooks.md) - Writing and executing code

## Quick Start

1. Sign up at https://community.cloud.databricks.com/
2. Create a cluster
3. Create a notebook
4. Start writing code

## Example Notebook Code

```python
# Read built-in dataset
df = spark.read.csv("/databricks-datasets/iris/iris.csv", header=True, inferSchema=True)

# Display results
display(df)

# Run SQL
spark.sql("SELECT * FROM iris WHERE sepal_length > 5.0").show()
```

## Topics

- [Setup](setup.md) - Account and workspace setup
- [Workspace & Clusters](workspace.md) - Infrastructure management
- [Notebooks](notebooks.md) - Development environment
