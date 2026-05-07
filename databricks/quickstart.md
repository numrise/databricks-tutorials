# Getting Started with Databricks

## Step 1: Sign Up

1. Go to [Databricks Community Edition](https://community.cloud.databricks.com/).
2. Create a free account.

## Step 2: Create a Cluster

1. In the Databricks workspace, click **Clusters** > **Create Cluster**.
2. Select a runtime (e.g., `Databricks Runtime 14.3 LTS`).
3. Click **Create Cluster**.

## Step 3: Create a Notebook

1. Click **Workspace** > **Create** > **Notebook**.
2. Attach the notebook to your cluster.
3. Write and run code in cells (Python, Scala, SQL, or R).

## Example: PySpark in Databricks

```python
# Read a CSV file
df = spark.read.csv("/databricks-datasets/iris/iris.csv", header=True, inferSchema=True)
display(df)
```
