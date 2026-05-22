# Unity Catalog

Unity Catalog is Databricks' unified governance layer for all data and AI assets across workspaces and clouds. It provides a single place to manage access control, data lineage, auditing, and data discovery.

- [Unity Catalog documentation](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)
- [Unity Catalog overview (video)](https://www.youtube.com/watch?v=3BbFz4YpUeU)

---

## Object Hierarchy

Unity Catalog organises objects in a three-level namespace:

```text
Metastore
  └── Catalog
        └── Schema (Database)
              ├── Table
              ├── View
              ├── Volume
              └── Function
```

Reference objects with the fully qualified name:

```sql
catalog_name.schema_name.table_name
```

### Metastore

The top-level container for all Unity Catalog metadata in a region. One metastore per region per account. It is linked to one or more workspaces.

### Catalog

The first level of the namespace. Organises schemas (databases) by subject area, environment, or business domain.

```sql
-- List catalogs
SHOW CATALOGS;

-- Create a catalog
CREATE CATALOG IF NOT EXISTS finance;

-- Set the active catalog for the session
USE CATALOG finance;

-- Drop a catalog (must be empty)
DROP CATALOG finance;
```

### Schema (Database)

The second level. Groups related tables, views, and functions within a catalog. The terms *schema* and *database* are interchangeable in Databricks SQL.

```sql
-- List schemas in the active catalog
SHOW SCHEMAS;
SHOW DATABASES;               -- alias

-- Create
CREATE SCHEMA IF NOT EXISTS finance.transactions;

-- Set active schema
USE SCHEMA finance.transactions;
USE DATABASE finance.transactions;   -- alias

-- Drop (must be empty unless CASCADE)
DROP SCHEMA finance.transactions CASCADE;
```

### Tables

Tables hold structured data. Unity Catalog supports **managed tables** (lifecycle owned by Databricks) and **external tables** (data in customer-controlled storage).

```sql
-- Create a managed table
CREATE TABLE finance.transactions.payments (
    id        BIGINT NOT NULL,
    amount    DECIMAL(18, 2),
    currency  STRING,
    paid_at   TIMESTAMP
)
USING DELTA;

-- Create an external table
CREATE TABLE finance.transactions.raw_events
USING PARQUET
LOCATION 'abfss://raw@mystorageaccount.dfs.core.windows.net/events/';

-- List tables in current schema
SHOW TABLES;
SHOW TABLES IN finance.transactions;

-- Describe a table
DESCRIBE TABLE EXTENDED finance.transactions.payments;

-- Drop
DROP TABLE IF EXISTS finance.transactions.payments;
```

### Views

Views are virtual tables defined by a SQL query. They do not store data.

```sql
-- Standard view
CREATE VIEW finance.transactions.monthly_totals AS
SELECT
    DATE_TRUNC('month', paid_at) AS month,
    SUM(amount)                  AS total_amount,
    currency
FROM finance.transactions.payments
GROUP BY 1, 3;

-- Drop
DROP VIEW IF EXISTS finance.transactions.monthly_totals;
```

**Dynamic views** enforce row- and column-level security using `current_user()` and `is_account_group_member()`:

```sql
CREATE VIEW finance.transactions.payments_masked AS
SELECT
    id,
    CASE
        WHEN is_account_group_member('finance_analysts')
        THEN amount
        ELSE NULL
    END AS amount,
    currency,
    paid_at
FROM finance.transactions.payments;
```

### Columns

Columns belong to tables and views. Unity Catalog supports column-level security and tagging.

```sql
-- Add a column
ALTER TABLE finance.transactions.payments
ADD COLUMN merchant_id STRING;

-- Rename a column (Delta only)
ALTER TABLE finance.transactions.payments
RENAME COLUMN merchant_id TO merchant_ref;

-- Apply a tag to a column (requires APPLY TAG privilege)
ALTER TABLE finance.transactions.payments
ALTER COLUMN amount SET TAGS ('pii' = 'true', 'classification' = 'confidential');
```

### Volumes

Volumes are Unity Catalog objects that govern access to non-tabular files (CSV, JSON, images, binaries).

```sql
-- Managed volume (Databricks controls storage)
CREATE VOLUME finance.transactions.raw_files;

-- External volume
CREATE EXTERNAL VOLUME finance.transactions.archive
LOCATION 'abfss://archive@mystorageaccount.dfs.core.windows.net/';

-- Read a file from a volume
SELECT * FROM read_files('/Volumes/finance/transactions/raw_files/data.csv');
```

---

## Delta Sharing

Unity Catalog enables sharing data with external recipients without copying it.

```sql
-- Create a share
CREATE SHARE finance_external_share;

-- Add a table to the share
ALTER SHARE finance_external_share
ADD TABLE finance.transactions.monthly_totals;

-- Create a recipient
CREATE RECIPIENT external_partner
USING ID 'recipient@partner.com';

-- Grant access
GRANT SELECT ON SHARE finance_external_share TO RECIPIENT external_partner;
```

---

## Data Lineage

Unity Catalog automatically tracks column-level lineage for tables and views. View lineage in:

- Catalog Explorer → table → **Lineage** tab
- REST API: `GET /api/2.0/lineage-tracking/table-lineage`

---

## Tags and Classification

```sql
-- Tag a table
ALTER TABLE finance.transactions.payments
SET TAGS ('domain' = 'finance', 'env' = 'prod');

-- Tag a schema
ALTER SCHEMA finance.transactions
SET TAGS ('pii_present' = 'true');

-- Tag a catalog
ALTER CATALOG finance
SET TAGS ('owner' = 'finance-team');
```

---

## Storage Credentials and External Locations

Unity Catalog uses **storage credentials** (Azure Managed Identity or Service Principal) and **external locations** to grant access to cloud storage.

```sql
-- Create a storage credential (usually done via Terraform or UI)
CREATE STORAGE CREDENTIAL my_adls_cred
WITH AZURE_MANAGED_IDENTITY (
    CONNECTOR_ID = '/subscriptions/.../connectors/my-connector'
);

-- Create an external location
CREATE EXTERNAL LOCATION finance_raw
URL 'abfss://raw@mystorageaccount.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL my_adls_cred);
```

---

## Related

- [permissions.md](permissions.md) — GRANT, MANAGE, account groups
- [terraform.md](terraform.md) — Managing Unity Catalog with Terraform
- [workspace.md](workspace.md) — Workspace and cluster configuration
