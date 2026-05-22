# Terraform for Databricks

The [Databricks Terraform Provider](https://registry.terraform.io/providers/databricks/databricks/latest/docs) lets you manage Databricks workspaces, Unity Catalog, clusters, jobs, secrets, groups, and permissions as infrastructure-as-code.

- [Provider documentation](https://registry.terraform.io/providers/databricks/databricks/latest/docs)
- [GitHub repo](https://github.com/databricks/terraform-provider-databricks)
- [Azure Databricks Terraform module](https://registry.terraform.io/modules/Azure/databricks/azurerm/latest)

---

## Provider Setup

### Install and configure

```hcl
terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.40"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

provider "azurerm" {
  features {}
}

# Workspace-level provider (manage clusters, jobs, notebooks)
provider "databricks" {
  alias               = "workspace"
  host                = azurerm_databricks_workspace.this.workspace_url
  azure_workspace_resource_id = azurerm_databricks_workspace.this.id
}

# Account-level provider (manage Unity Catalog, groups, metastore)
provider "databricks" {
  alias      = "account"
  host       = "https://accounts.azuredatabricks.net"
  account_id = var.databricks_account_id
}
```

### Authentication options

| Method | When to use |
| ------ | ----------- |
| Azure CLI (`az login`) | Local development |
| Service Principal + client secret | CI/CD pipelines |
| Service Principal + Azure Managed Identity | Terraform running on Azure compute |
| Personal Access Token | Quick scripts (avoid in production) |

```hcl
# Service principal authentication
provider "databricks" {
  host              = var.databricks_workspace_url
  azure_tenant_id   = var.tenant_id
  azure_client_id   = var.client_id
  azure_client_secret = var.client_secret
}
```

---

## Azure Databricks Workspace

```hcl
resource "azurerm_resource_group" "databricks" {
  name     = "rg-databricks-prod"
  location = "westeurope"
}

resource "azurerm_databricks_workspace" "this" {
  name                = "dbw-prod"
  resource_group_name = azurerm_resource_group.databricks.name
  location            = azurerm_resource_group.databricks.location
  sku                 = "premium"    # Required for Unity Catalog

  tags = {
    environment = "prod"
    team        = "data-engineering"
  }
}

output "workspace_url" {
  value = "https://${azurerm_databricks_workspace.this.workspace_url}"
}
```

---

## Unity Catalog

### Metastore and assignment

```hcl
# Create a Unity Catalog metastore (one per region per account)
resource "databricks_metastore" "this" {
  provider      = databricks.account
  name          = "prod-metastore-westeurope"
  region        = "westeurope"
  storage_root  = "abfss://metastore@${azurerm_storage_account.metastore.name}.dfs.core.windows.net/"
  force_destroy = false
}

# Assign the metastore to a workspace
resource "databricks_metastore_assignment" "this" {
  provider     = databricks.account
  metastore_id = databricks_metastore.this.id
  workspace_id = azurerm_databricks_workspace.this.workspace_id
}
```

### Catalogs

```hcl
resource "databricks_catalog" "finance" {
  provider     = databricks.workspace
  metastore_id = databricks_metastore.this.id
  name         = "finance"
  comment      = "Finance domain data"

  properties = {
    purpose = "production"
  }
}
```

### Schemas (Databases)

```hcl
resource "databricks_schema" "transactions" {
  provider     = databricks.workspace
  catalog_name = databricks_catalog.finance.name
  name         = "transactions"
  comment      = "Transaction data"
}
```

### External Locations and Storage Credentials

```hcl
# Storage credential using Azure Managed Identity
resource "databricks_storage_credential" "adls" {
  provider = databricks.workspace
  name     = "adls-managed-identity"

  azure_managed_identity {
    access_connector_id = azurerm_databricks_access_connector.this.id
  }
}

# External location backed by ADLS Gen2
resource "databricks_external_location" "raw" {
  provider        = databricks.workspace
  name            = "finance-raw"
  url             = "abfss://raw@${azurerm_storage_account.datalake.name}.dfs.core.windows.net/"
  credential_name = databricks_storage_credential.adls.name
}
```

---

## Groups

### Account-level groups

```hcl
# Account group (visible across workspaces, usable in Unity Catalog)
resource "databricks_group" "data_analysts" {
  provider     = databricks.account
  display_name = "data_analysts"
}

resource "databricks_group" "data_engineers" {
  provider     = databricks.account
  display_name = "data_engineers"
}

# Add a user to a group
resource "databricks_group_member" "analyst_alice" {
  provider  = databricks.account
  group_id  = databricks_group.data_analysts.id
  member_id = databricks_user.alice.id
}

# Nest groups
resource "databricks_group_member" "analysts_in_readers" {
  provider  = databricks.account
  group_id  = databricks_group.all_readers.id
  member_id = databricks_group.data_analysts.id
}
```

### Users and service principals

```hcl
resource "databricks_user" "alice" {
  provider  = databricks.account
  user_name = "alice@example.com"
}

resource "databricks_service_principal" "etl_pipeline" {
  provider     = databricks.account
  display_name = "etl-pipeline-sp"
}
```

---

## Permissions (Grants)

```hcl
# Allow analysts to use the catalog
resource "databricks_grants" "finance_catalog" {
  provider = databricks.workspace
  catalog  = databricks_catalog.finance.name

  grant {
    principal  = databricks_group.data_analysts.display_name
    privileges = ["USE_CATALOG"]
  }

  grant {
    principal  = databricks_group.data_engineers.display_name
    privileges = ["USE_CATALOG", "CREATE_SCHEMA"]
  }
}

# Schema-level grants
resource "databricks_grants" "transactions_schema" {
  provider = databricks.workspace
  schema   = "${databricks_catalog.finance.name}.${databricks_schema.transactions.name}"

  grant {
    principal  = databricks_group.data_analysts.display_name
    privileges = ["USE_SCHEMA", "SELECT"]
  }

  grant {
    principal  = databricks_group.data_engineers.display_name
    privileges = ["USE_SCHEMA", "CREATE_TABLE", "CREATE_VIEW", "MODIFY"]
  }
}

# Table-level grant
resource "databricks_grants" "payments_table" {
  provider = databricks.workspace
  table    = "${databricks_catalog.finance.name}.${databricks_schema.transactions.name}.payments"

  grant {
    principal  = "reporting_sp"
    privileges = ["SELECT"]
  }
}
```

---

## Clusters

```hcl
data "databricks_spark_version" "latest_lts" {
  provider          = databricks.workspace
  long_term_support = true
}

data "databricks_node_type" "smallest" {
  provider   = databricks.workspace
  local_disk = true
}

resource "databricks_cluster" "shared_autoscaling" {
  provider                = databricks.workspace
  cluster_name            = "shared-autoscaling"
  spark_version           = data.databricks_spark_version.latest_lts.id
  node_type_id            = data.databricks_node_type.smallest.id
  autotermination_minutes = 30

  autoscale {
    min_workers = 1
    max_workers = 4
  }

  spark_conf = {
    "spark.databricks.io.cache.enabled" = true
  }

  custom_tags = {
    team = "data-engineering"
  }
}
```

---

## Jobs

```hcl
resource "databricks_job" "etl_pipeline" {
  provider = databricks.workspace
  name     = "nightly-etl"

  task {
    task_key = "ingest"

    new_cluster {
      num_workers   = 2
      spark_version = data.databricks_spark_version.latest_lts.id
      node_type_id  = data.databricks_node_type.smallest.id
    }

    notebook_task {
      notebook_path = "/Shared/pipelines/ingest"
    }
  }

  task {
    task_key = "transform"
    depends_on { task_key = "ingest" }

    existing_cluster_id = databricks_cluster.shared_autoscaling.id

    notebook_task {
      notebook_path = "/Shared/pipelines/transform"
    }
  }

  schedule {
    quartz_cron_expression = "0 0 2 * * ?"   # 02:00 daily
    timezone_id            = "UTC"
  }
}
```

---

## Secrets

```hcl
resource "databricks_secret_scope" "app_secrets" {
  provider = databricks.workspace
  name     = "app-secrets"

  # Use Azure Key Vault as the backend
  keyvault_metadata {
    resource_id = azurerm_key_vault.this.id
    dns_name    = azurerm_key_vault.this.vault_uri
  }
}

resource "databricks_secret" "db_password" {
  provider     = databricks.workspace
  key          = "db-password"
  string_value = var.db_password
  scope        = databricks_secret_scope.app_secrets.name
}

# Grant access to the scope
resource "databricks_secret_acl" "analysts_read" {
  provider   = databricks.workspace
  scope      = databricks_secret_scope.app_secrets.name
  principal  = databricks_group.data_analysts.display_name
  permission = "READ"
}
```

---

## Notebooks

```hcl
resource "databricks_notebook" "ingest" {
  provider = databricks.workspace
  path     = "/Shared/pipelines/ingest"
  language = "PYTHON"
  source   = "${path.module}/notebooks/ingest.py"
}
```

---

## Workspace Permissions (non-UC ACLs)

For workspace objects (notebooks, clusters, jobs) that are not governed by Unity Catalog:

```hcl
resource "databricks_permissions" "cluster_access" {
  provider   = databricks.workspace
  cluster_id = databricks_cluster.shared_autoscaling.id

  access_control {
    group_name       = databricks_group.data_engineers.display_name
    permission_level = "CAN_RESTART"
  }

  access_control {
    group_name       = databricks_group.data_analysts.display_name
    permission_level = "CAN_ATTACH_TO"
  }
}
```

---

## State and CI/CD Tips

- Store Terraform state in Azure Blob Storage (`azurerm` backend) with state locking via Azure Storage.
- Separate providers into `providers.tf`, resources by domain (`catalog.tf`, `groups.tf`, `jobs.tf`).
- Use `terraform plan` output as a PR review artefact.
- Avoid hardcoding secrets — pass via environment variables (`TF_VAR_client_secret`) or Azure Key Vault data sources.

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "stterraformstate"
    container_name       = "tfstate"
    key                  = "databricks/prod.tfstate"
  }
}
```

---

## Related

- [unity_catalog.md](unity_catalog.md) — Unity Catalog concepts
- [permissions.md](permissions.md) — SQL-based GRANT reference
- [Azure Databricks setup](../azure-databricks/setup.md) — Manual workspace setup
