# Databricks Permissions & Access Control

Unity Catalog uses a privilege model where access to securable objects is granted via SQL `GRANT` statements, the Databricks UI, or Terraform. This page covers the full model: object types, privilege types, group concepts, and common patterns.

- [Unity Catalog privileges reference](https://docs.databricks.com/en/data-governance/unity-catalog/manage-privileges/privileges.html)
- [Groups documentation](https://docs.databricks.com/en/admin/users-groups/groups.html)

---

## Securable Object Hierarchy

Privileges flow down the hierarchy. A privilege granted on a catalog is not automatically inherited by schemas or tables — each level must be granted separately (with the exception of `ALL PRIVILEGES`).

```text
Metastore
  └── Catalog         ← USE CATALOG, CREATE SCHEMA, CREATE CATALOG, ...
        └── Schema    ← USE SCHEMA, CREATE TABLE, CREATE VIEW, ...
              ├── Table    ← SELECT, MODIFY, ...
              ├── View     ← SELECT
              ├── Volume   ← READ VOLUME, WRITE VOLUME
              └── Function ← EXECUTE
```

---

## Privilege Reference

### Catalog privileges

| Privilege | Description |
| --------- | ----------- |
| `USE CATALOG` | Required to access any object within the catalog |
| `CREATE SCHEMA` | Create new schemas in the catalog |
| `CREATE CONNECTION` | Create connections to external systems |
| `ALL PRIVILEGES` | Grants all current and future privileges |

### Schema privileges

| Privilege | Description |
| --------- | ----------- |
| `USE SCHEMA` | Required to access any object within the schema |
| `CREATE TABLE` | Create managed or external tables |
| `CREATE VIEW` | Create views |
| `CREATE VOLUME` | Create volumes |
| `CREATE FUNCTION` | Create SQL or Python functions |
| `EXECUTE` | Run functions in the schema |
| `ALL PRIVILEGES` | Grants all schema-level privileges |

### Table privileges

| Privilege | Description |
| --------- | ----------- |
| `SELECT` | Read rows from the table |
| `MODIFY` | Insert, update, delete rows |
| `ALL PRIVILEGES` | SELECT + MODIFY |

### Other privileges

| Privilege | Object | Description |
| --------- | ------ | ----------- |
| `READ VOLUME` | Volume | Read files from a volume |
| `WRITE VOLUME` | Volume | Write files to a volume |
| `EXECUTE` | Function | Call the function |
| `CREATE CATALOG` | Metastore | Create new catalogs |
| `CREATE EXTERNAL LOCATION` | Metastore | Define external locations |
| `CREATE STORAGE CREDENTIAL` | Metastore | Add storage credentials |
| `MANAGE` | Any object | Grant or revoke privileges on behalf of others |

---

## GRANT Statement

```sql
GRANT <privilege> [, <privilege> ...]
ON <object_type> <object_name>
TO <principal>;
```

`<principal>` can be a user (`user@domain.com`), a group name, or `account users` (all users in the account).

### Typical access pattern

To give a group read access to a table, grant privileges at every level:

```sql
-- 1. Allow entering the catalog
GRANT USE CATALOG ON CATALOG finance TO `data_analysts`;

-- 2. Allow entering the schema
GRANT USE SCHEMA ON SCHEMA finance.transactions TO `data_analysts`;

-- 3. Allow reading the table
GRANT SELECT ON TABLE finance.transactions.payments TO `data_analysts`;
```

### Grant on a schema (all tables)

```sql
GRANT USE SCHEMA, SELECT ON SCHEMA finance.transactions TO `data_scientists`;
```

### Grant CREATE privileges for data engineers

```sql
GRANT USE CATALOG ON CATALOG finance TO `data_engineers`;
GRANT USE SCHEMA, CREATE TABLE, CREATE VIEW, MODIFY
  ON SCHEMA finance.transactions
  TO `data_engineers`;
```

### Grant ALL PRIVILEGES

```sql
GRANT ALL PRIVILEGES ON CATALOG finance TO `catalog_owners`;
```

---

## REVOKE Statement

```sql
REVOKE SELECT ON TABLE finance.transactions.payments FROM `data_analysts`;
REVOKE ALL PRIVILEGES ON SCHEMA finance.transactions FROM `temp_users`;
```

---

## SHOW GRANTS

```sql
-- Who has privileges on a specific object?
SHOW GRANTS ON TABLE finance.transactions.payments;

-- What privileges does a principal hold?
SHOW GRANTS TO `data_analysts`;
SHOW GRANTS TO `user@example.com`;
```

---

## MANAGE Privilege

`MANAGE` allows the holder to grant and revoke privileges on an object to others, **without needing to be a metastore admin**. It is the delegation mechanism in Unity Catalog.

```sql
-- Grant ownership-like delegation on a schema
GRANT MANAGE ON SCHEMA finance.transactions TO `schema_stewards`;

-- The schema_stewards group can now:
-- GRANT SELECT ON TABLE finance.transactions.payments TO <anyone>
-- REVOKE SELECT ON TABLE finance.transactions.payments FROM <anyone>
```

`MANAGE` does not grant data access itself — combine it with `SELECT`/`MODIFY` if the manager also needs to read data.

---

## USE CATALOG and USE SCHEMA

These are gateway privileges. Without them, a user cannot see or access anything inside the object, even if they have `SELECT` on a table within it.

```sql
-- Required to run: USE CATALOG finance
GRANT USE CATALOG ON CATALOG finance TO `data_analysts`;

-- Required to run: USE SCHEMA finance.transactions
GRANT USE SCHEMA ON SCHEMA finance.transactions TO `data_analysts`;
```

A common mistake is granting `SELECT` on a table but forgetting `USE CATALOG` and `USE SCHEMA`, which results in `PERMISSION_DENIED` errors.

---

## Groups

### Account Groups vs Workspace-Local Groups

Databricks has two distinct group scopes:

| | Account Groups | Workspace-Local Groups |
| - | -------------- | ---------------------- |
| **Managed in** | Databricks Account Console | Individual workspace |
| **Scope** | Entire account, all workspaces | Single workspace only |
| **Synced to workspace** | Yes (automatically or on demand) | No — local only |
| **Use in Unity Catalog** | Yes | **No** — Unity Catalog only honours account-level groups |
| **Use in workspace ACLs** | Yes | Yes |
| **Recommended** | Yes, for all new projects | Legacy — avoid for UC |

**Unity Catalog only recognises account-level groups.** If you try to GRANT to a workspace-local group in a Unity Catalog context, it will fail.

### Creating Account Groups (UI)

1. Go to `account.azuredatabricks.net` → **User Management** → **Groups**.
2. Click **Add Group**, name it (e.g. `finance_analysts`).
3. Add users or nest other groups.
4. Assign the group to one or more workspaces.

### Creating Groups via Databricks CLI

```bash
# Account-level group
databricks account groups create --json '{"displayName": "finance_analysts"}'

# Add a member
databricks account groups add-member <group-id> --json '{"value": "<user-id>"}'

# List groups
databricks account groups list
```

### Nesting Groups

Account groups can be nested. Privileges granted to a parent group are inherited by child group members.

```sql
-- Grant to parent group; members of child groups also benefit
GRANT SELECT ON TABLE finance.transactions.payments TO `finance_team`;
```

### Workspace-Local Groups

Still used for **workspace-level ACLs** (notebook, cluster, job, secret scope permissions) where Unity Catalog is not involved.

```bash
# Workspace-local group
databricks groups create --profile my-workspace --json '{"displayName": "local_admins"}'
```

---

## Common Patterns

### Read-only analyst role

```sql
GRANT USE CATALOG          ON CATALOG prod            TO `analysts`;
GRANT USE SCHEMA           ON SCHEMA prod.sales        TO `analysts`;
GRANT SELECT               ON TABLE prod.sales.orders  TO `analysts`;
GRANT SELECT               ON VIEW prod.sales.summary  TO `analysts`;
```

### Data engineer role (write access)

```sql
GRANT USE CATALOG                      ON CATALOG prod     TO `engineers`;
GRANT USE SCHEMA, CREATE TABLE, MODIFY ON SCHEMA prod.raw  TO `engineers`;
GRANT READ VOLUME, WRITE VOLUME        ON VOLUME prod.raw.uploads TO `engineers`;
```

### Data owner / steward (can delegate)

```sql
GRANT MANAGE ON SCHEMA prod.sales TO `sales_stewards`;
```

### Service principal for a pipeline

```sql
GRANT USE CATALOG              ON CATALOG prod               TO `sp_etl_pipeline`;
GRANT USE SCHEMA               ON SCHEMA prod.raw            TO `sp_etl_pipeline`;
GRANT SELECT, MODIFY           ON TABLE prod.raw.events      TO `sp_etl_pipeline`;
GRANT CREATE TABLE             ON SCHEMA prod.curated        TO `sp_etl_pipeline`;
```

---

## Row and Column Security

For more granular control use dynamic views (see [unity_catalog.md](unity_catalog.md#views)) or **row filters** and **column masks** (Unity Catalog Premium).

```sql
-- Column mask function
CREATE FUNCTION finance.security.mask_card_number(card STRING)
RETURNS STRING
RETURN CASE
    WHEN is_account_group_member('card_auditors') THEN card
    ELSE CONCAT('****-****-****-', RIGHT(card, 4))
END;

-- Apply the mask to a column
ALTER TABLE finance.transactions.card_payments
ALTER COLUMN card_number
SET MASK finance.security.mask_card_number;
```

---

## Related

- [unity_catalog.md](unity_catalog.md) — Object hierarchy and DDL
- [terraform.md](terraform.md) — Automate grants with Terraform
