# Azure Databricks Setup Guide

## Prerequisites

- Azure account with **Contributor** or **Owner** role.
- Azure subscription.

## Step 1: Create a Workspace

1. Go to the [Azure Portal](https://portal.azure.com/).
2. Click **Create a resource** > **Analytics** > **Azure Databricks**.
3. Fill in the details (e.g., workspace name, region, pricing tier).
4. Click **Review + create** > **Create**.

## Step 2: Launch the Workspace

1. After deployment, click **Go to resource**.
2. Click **Launch Workspace** to open the Databricks portal.

## Step 3: Create a Cluster

1. In the Databricks workspace, click **Clusters** > **Create Cluster**.
2. Select a **Databricks Runtime Version** (e.g., `14.3 LTS`).
3. Configure the cluster (e.g., node type, number of workers).
4. Click **Create Cluster**.

## Step 4: Run a Sample Notebook

1. Click **Workspace** > **Create** > **Notebook**.
2. Attach the notebook to your cluster.
3. Run the following code to test:

```python
# Example: Read data from Azure Blob Storage
df = spark.read.csv("wasbs://container@storageaccount.blob.core.windows.net/path/to/file.csv", header=True)
display(df)
```
