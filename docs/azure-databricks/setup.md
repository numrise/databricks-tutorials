# Setting Up Azure Databricks

## Prerequisites

- Azure subscription with Contributor or Owner role
- Azure CLI (optional, for automation)

## Deployment Steps

### Via Azure Portal

1. **Search for Azure Databricks**
   - Go to Azure Portal
   - Search "Azure Databricks"
   - Click "Create"

2. **Configure Basics**
   - Subscription: Select your subscription
   - Resource Group: Create or select existing
   - Workspace Name: Give it a unique name
   - Region: Choose nearest region

3. **Configure Networking** (if desired)
   - VNet: Use custom VNet for security
   - Subnets: Configure public/private subnets
   - Security: Enable network security groups

4. **Review and Create**
   - Click "Review + create"
   - Click "Create"

### Via Azure CLI

```bash
az login
az group create --name myResourceGroup --location eastus
az databricks workspace create \
  --resource-group myResourceGroup \
  --name myWorkspace \
  --location eastus \
  --sku standard
```

## Launching Workspace

1. Go to resource group in Azure Portal
2. Click your Databricks workspace
3. Click "Launch Workspace"
4. Sign in with your Azure account

## Creating Clusters

1. In workspace, click **Clusters**
2. Click **Create Cluster**
3. Configure:
   - Cluster name
   - Runtime: Latest LTS recommended
   - Worker type: Choose based on workload
   - Number of workers
4. Click **Create Cluster**

## Connecting to Azure Storage

### Access Keys Method

```python
storage_account = "mystorageaccount"
container = "mycontainer"
key = "your-storage-key"

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    key
)

# Read from storage
df = spark.read.parquet(
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/data/"
)
```

### Service Principal Method

```python
client_id = "your-client-id"
tenant_id = "your-tenant-id"
client_secret = "your-client-secret"

spark.conf.set(f"fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{storage_account}.dfs.core.windows.net", 
               "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{storage_account}.dfs.core.windows.net", client_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{storage_account}.dfs.core.windows.net", client_secret)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{storage_account}.dfs.core.windows.net",
               f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token")
```

## Connecting to SQL Database

```python
server = "myserver.database.windows.net"
database = "mydb"
user = "admin@myserver"
password = "your-password"

df = spark.read.format("jdbc") \
    .option("url", f"jdbc:sqlserver://{server}:1433;database={database}") \
    .option("dbtable", "dbo.mytable") \
    .option("user", user) \
    .option("password", password) \
    .load()
```

## Cost Considerations

- **Compute**: Price per DBU (Databricks Unit)
- **Storage**: Standard Azure Storage costs
- **Network**: Standard Azure network charges
- **Optimize with**: Spot instances, auto-scaling, auto-termination

## Next Steps

- Explore [Integration options](integration.md)
- Learn [Cost optimization](cost.md)
