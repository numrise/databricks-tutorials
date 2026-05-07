# Getting Started with Databricks - Beginner

Welcome to Databricks! This guide covers essential concepts.

## Table of Contents

1. [Account Setup](01-account-setup.md)
2. [Workspace & Clusters](02-workspace-clusters.md)
3. [Notebooks & Programming](03-notebooks-programming.md)
4. [Data Management](04-data-management.md)
5. [Collaboration Features](05-collaboration.md)

## What is Databricks?

Databricks is a unified analytics platform built on Apache Spark that simplifies:
- **Data Engineering**: Build reliable pipelines
- **Data Analytics**: Query data with SQL
- **Machine Learning**: Train and deploy models
- **Collaboration**: Work as a team

## Key Features

✅ **Collaborative Notebooks** - Like Jupyter but better
✅ **Managed Clusters** - No infrastructure management
✅ **Delta Lake** - ACID transactions on data lake
✅ **MLflow** - Machine learning lifecycle
✅ **Workflows** - Schedule and orchestrate jobs

## Prerequisites

- Web browser
- Email address for account creation
- Basic Python or SQL knowledge

## Quick Start

1. Sign up: https://community.cloud.databricks.com/
2. Create cluster
3. Create notebook
4. Write and execute code

## Common Workflows

### Data Analysis
```python
df = spark.read.csv("/databricks-datasets/iris/iris.csv", header=True, inferSchema=True)
display(df)
```

### SQL Queries
```sql
SELECT * FROM iris WHERE sepal_length > 5.0
```

### Machine Learning
Use MLflow to track experiments and models

## Next Steps

- Follow tutorials in order
- Explore sample notebooks in workspace
- Join Databricks community forums
