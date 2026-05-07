# Azure Integration

## Connecting to Azure Services

### Azure Data Lake Storage Gen2

```python
# Using storage account name and key
storage_account = "mystorageaccount"
container = "mycontainer"
key = "your-storage-key"

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    key
)

# Read Parquet
df = spark.read.parquet(
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/data/"
)

# Write Delta
df.write.format("delta").mode("overwrite").save(
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/delta/"
)
```

### Azure Blob Storage

```python
storage_account = "mystorageaccount"
container = "mycontainer"
key = "your-storage-key"

spark.conf.set(f"fs.azure.account.key.{storage_account}.blob.core.windows.net", key)

df = spark.read.csv(f"wasbs://{container}@{storage_account}.blob.core.windows.net/data.csv")
```

### Azure SQL Database

```python
server = "myserver.database.windows.net"
database = "mydb"
table = "dbo.mytable"
user = "admin@myserver"
password = "password"
url = f"jdbc:sqlserver://{server}:1433;database={database};user={user}@{server};password={password};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"

df = spark.read.format("jdbc") \
    .option("url", url) \
    .option("dbtable", table) \
    .load()
```

### Azure Cosmos DB

```python
cosmos_endpoint = "https://myaccount.documents.azure.com:443/"
cosmos_masterkey = "your-key"
cosmos_database = "mydb"
cosmos_container = "mycontainer"

df = spark.read.format("cosmos.oltp") \
    .option("spark.cosmos.account.endpoint", cosmos_endpoint) \
    .option("spark.cosmos.account.key", cosmos_masterkey) \
    .option("spark.cosmos.database", cosmos_database) \
    .option("spark.cosmos.container", cosmos_container) \
    .load()
```

## Data Factory Integration

Use Azure Data Factory to orchestrate Databricks jobs:

```python
# In your Databricks notebook
dbutils.widgets.text("pipeline_param", "default_value")
param = dbutils.widgets.get("pipeline_param")

print(f"Received parameter: {param}")
```

In Azure Data Factory:
1. Create linked service for Databricks
2. Add "Databricks Notebook" activity
3. Configure notebook path and parameters
4. Schedule pipeline

## Power BI Integration

Connect Power BI to Databricks:

1. In Power BI Desktop: **Get Data** → **More...**
2. Search for "Databricks"
3. Configure connection:
   - Server hostname
   - HTTP path
   - Personal access token
4. Create visualizations

## Authentication Methods

### Personal Access Token

```python
# Create token in Databricks
# Settings → User Settings → Access Tokens

token = "dapi123456..."
workspace_url = "https://myworkspace.azuredatabricks.net"

# Use in API calls
headers = {"Authorization": f"Bearer {token}"}
```

### Azure AD Integration

Databricks automatically integrates with Azure AD for authentication. All workspace access uses Azure AD credentials.

## Best Practices

1. **Use Managed Identities** - For service-to-service authentication
2. **Store Secrets in Azure Key Vault** - Not in code
3. **Enable VNet Integration** - For network security
4. **Use Service Principals** - For automation
5. **Enable Azure Logging** - For audit trails

## Accessing Secrets

From Azure Key Vault:

```python
from databricks.sdk import WorkspaceClient
import os

# Store Key Vault URL as environment variable
kv_url = os.environ.get("KEYVAULT_URL")

# Or use Databricks secrets:
token = dbutils.secrets.get(scope="myscope", key="mykey")
```

## Next Steps

- Learn [Cost Optimization](cost.md)
- Explore data pipeline patterns
