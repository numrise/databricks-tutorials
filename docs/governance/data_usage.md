# Data Usage

Data usage governance defines the rules, processes, and controls that determine how data assets may be accessed, processed, and distributed across an organisation. It translates abstract policies into operational controls.

---

## Why Data Usage Governance?

- **Regulatory compliance**: GDPR, HIPAA, CCPA, PCI DSS impose specific obligations on how data is handled.
- **Risk management**: uncontrolled data use creates exposure to breaches, fines, and reputational harm.
- **Trust**: data consumers know what they are allowed to do; data owners retain control.
- **Efficiency**: clear policies reduce the time spent resolving access disputes.

---

## Data Classification

Classification is the foundation of data usage governance. Every data asset should have a classification that drives the controls applied to it.

| Level | Description | Example Data | Typical Controls |
| ----- | ----------- | ------------ | ---------------- |
| **Public** | Safe for external release | Marketing copy, public reports | No special controls |
| **Internal** | For employees only | Internal KPIs, org charts | Authentication, no external sharing |
| **Confidential** | Restricted to specific roles | Customer PII, financial records | RBAC, column masking, audit logging |
| **Restricted** | Highest sensitivity | Health data, credentials, legal holds | Strict RBAC, encryption, MFA, DSA required |

Apply classification in Databricks using Unity Catalog tags:

```sql
ALTER TABLE prod.customers.profiles
SET TAGS ('classification' = 'confidential', 'pii' = 'true');

ALTER TABLE prod.customers.profiles
ALTER COLUMN email
SET TAGS ('pii_type' = 'email', 'classification' = 'restricted');
```

---

## Data Usage Purposes

A **purpose** describes why data is being accessed. Limiting use to stated purposes is required by GDPR's *purpose limitation* principle and is good practice regardless of jurisdiction.

Common purposes:

| Purpose Code | Description |
| ------------ | ----------- |
| `analytics` | Aggregate analysis, no individual-level output |
| `reporting` | Producing scheduled business reports |
| `ml-training` | Training machine learning models |
| `operations` | Operational processing (order fulfilment, billing) |
| `audit` | Compliance and internal audit activities |
| `product` | Building or improving a product or service |
| `research` | Academic or market research (anonymised or consented) |

---

## Access Control Principles

### Least privilege

Grant only the privileges needed for the stated purpose. Never grant `ALL PRIVILEGES` to routine service accounts or analyst users.

```sql
-- Correct: read-only for analytics
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA  ON SCHEMA prod.sales TO `analysts`;
GRANT SELECT      ON TABLE prod.sales.orders TO `analysts`;

-- Avoid: over-provisioned
GRANT ALL PRIVILEGES ON CATALOG prod TO `analysts`;
```

### Need-to-know

Access should be limited to those with a legitimate business need, not based on seniority or convenience.

### Time-limited access

Temporary access for a project should be revoked when the project ends. Use Databricks service principals with rotating credentials rather than permanent personal tokens.

### Separation of duties

The team that owns data should not also be the team that approves their own access requests. Use a data steward or governance committee as an independent approver.

---

## PII and Sensitive Data Handling

### Identifying PII

PII (Personally Identifiable Information) includes any data that can identify a natural person: name, email, address, phone number, IP address, device ID, national ID number, health data, biometric data.

Tag PII columns in Unity Catalog:

```sql
ALTER TABLE prod.customers.profiles
ALTER COLUMN email
SET TAGS ('pii_type' = 'email');

ALTER TABLE prod.customers.profiles
ALTER COLUMN national_id
SET TAGS ('pii_type' = 'national_id', 'classification' = 'restricted');
```

### Pseudonymisation

Replace direct identifiers with a reversible token. The mapping table is held separately under strict access control.

```sql
-- Pseudonymised table (safe for analytics)
CREATE TABLE prod.analytics.customer_events AS
SELECT
    sha2(customer_id, 256) AS customer_token,  -- hashed, not reversible
    event_type,
    event_timestamp
FROM prod.raw.customer_events;
```

### Anonymisation

Remove or generalise data to the point where re-identification is not reasonably possible. Anonymised data is outside GDPR scope.

Techniques: generalisation (age band instead of DOB), suppression, noise addition, k-anonymity.

### Column masking (Unity Catalog)

See [permissions.md](../databricks/permissions.md#row-and-column-security) for implementation.

---

## Data Retention

Retaining data longer than necessary increases compliance risk and storage cost.

| Data type | Suggested retention |
| --------- | ------------------- |
| Transaction records | 7 years (financial regulations) |
| Web/app logs | 90 days (operational) to 2 years (security) |
| Marketing consent records | Duration of consent + 3 years |
| Employee data | Duration of employment + statutory period |
| Anonymised analytics | No limit |

Implement retention in Delta Lake:

```sql
-- Set table property for retention awareness
ALTER TABLE prod.raw.events
SET TBLPROPERTIES ('retention_days' = '90');

-- Clean up old data
DELETE FROM prod.raw.events
WHERE event_date < CURRENT_DATE - INTERVAL 90 DAYS;

-- VACUUM removes files no longer referenced (set delta.deletedFileRetentionDuration first)
VACUUM prod.raw.events RETAIN 168 HOURS;
```

---

## Audit Logging

All access to sensitive data should be logged. Databricks workspace audit logs capture:

- Who accessed which table and when.
- What query was executed.
- Whether downloads occurred.

Enable and route audit logs:

```hcl
# Terraform: enable diagnostic settings on the Databricks workspace
resource "azurerm_monitor_diagnostic_setting" "databricks" {
  name                       = "databricks-audit"
  target_resource_id         = azurerm_databricks_workspace.this.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.this.id

  enabled_log {
    category = "dbfs"
  }

  enabled_log {
    category = "clusters"
  }

  enabled_log {
    category = "accounts"
  }
}
```

Query audit logs in Log Analytics:

```kusto
DatabricksAccounts
| where ActionName == "getData" or ActionName == "runCommand"
| where TimeGenerated > ago(7d)
| project TimeGenerated, UserIdentity, ActionName, RequestParams
| order by TimeGenerated desc
```

---

## Data Usage Request Process

A standard process for approving data access requests:

```text
1. Requestor submits request
   - Dataset / table requested
   - Purpose (from approved purpose list)
   - Duration
   - Justification

2. Data steward reviews
   - Is the stated purpose valid?
   - Is there a DSA in place if cross-team/external?
   - Is the request within the data classification policy?

3. Approval / rejection
   - Approved: access provisioned via Databricks GRANT or group membership
   - Rejected: reason documented

4. Access provisioned (automated where possible)

5. Periodic re-certification
   - Access reviewed every 90 days or on project completion

6. Revocation
   - Access removed; deletion confirmed if required by DSA
```

---

## Data Usage Policy: Summary Checklist

- [ ] All tables have a classification tag (`public`, `internal`, `confidential`, `restricted`).
- [ ] PII columns tagged with `pii_type`.
- [ ] Column masks applied to restricted columns.
- [ ] No user has `ALL PRIVILEGES` without documented justification.
- [ ] Service principal tokens rotated at least every 90 days.
- [ ] Retention periods defined and enforced for all confidential/restricted tables.
- [ ] Audit logging enabled and retained for minimum 1 year.
- [ ] A DSA is in place for all cross-team or external data sharing.
- [ ] Access requests documented and approved before provisioning.
- [ ] Quarterly access re-certification scheduled.

---

## Related

- [dsa.md](dsa.md) — Data Sharing & Stewardship Agreements
- [collibra.md](collibra.md) — Enforcing usage policies in Collibra
- [permissions.md](../databricks/permissions.md) — Unity Catalog GRANT reference
- [unity_catalog.md](../databricks/unity_catalog.md) — Tagging and classification in Unity Catalog
