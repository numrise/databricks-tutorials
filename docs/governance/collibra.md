# Collibra

[Collibra](https://www.collibra.com/) is an enterprise data intelligence platform that provides data cataloguing, business glossary management, data lineage, data quality monitoring, and policy governance.

- [Collibra documentation](https://productresources.collibra.com/)
- [Collibra University](https://university.collibra.com/)
- [Collibra REST API](https://developer.collibra.com/)

---

## Core Concepts

### Community

The highest organisational unit in Collibra. Represents a business domain or department (e.g. Finance, HR, Data Engineering).

```
Community
  └── Domain
        └── Asset
```

### Domain

A container within a community that groups related assets. Domains have a type (e.g. Business Glossary, Data Dictionary, Policy Domain).

| Domain Type | Purpose |
| ----------- | ------- |
| Business Glossary | Business terms and definitions |
| Data Dictionary | Technical data asset documentation |
| Policy Domain | Data policies and rules |
| Technology Asset Domain | Databases, systems, applications |

### Asset

The fundamental object in Collibra. An asset has a type, attributes, relations, and a workflow status.

Common asset types:

| Asset Type | Description |
| ---------- | ----------- |
| Business Term | Defined business concept (e.g. "Net Revenue") |
| Data Element | A column or field in a system |
| Data Set | A table, file, or API response |
| Report | A BI report or dashboard |
| System | A source or target application |
| Data Policy | A governance rule |

---

## Business Glossary

The Business Glossary stores approved, defined business terms. Each term has:

- **Name** and **Definition**
- **Owner** (accountable person)
- **Steward** (day-to-day manager)
- **Status** (Draft → Under Review → Approved → Deprecated)
- **Related terms** (synonyms, broader/narrower terms)
- **Mapped data elements** (the physical columns that represent this term)

### Why it matters

A consistent glossary removes ambiguity. When a report says "Active Customers", the glossary definition specifies exactly which rows qualify — preventing different teams from computing the same metric differently.

---

## Data Catalog

The Data Catalog provides a searchable inventory of all data assets. Users can:

- Search and discover datasets by keyword, tag, or domain.
- See data lineage from source systems to BI reports.
- Review data quality scores.
- Request access directly from the catalog.

### Connecting Collibra to Databricks Unity Catalog

Collibra provides a native **Databricks Unity Catalog connector** that auto-harvests:

- Catalogs, schemas, tables, views, and columns from Unity Catalog.
- Column-level data lineage tracked by Unity Catalog.
- Tags and classifications applied in Databricks.

**Setup steps:**

1. In Collibra, go to **Connect** → **Connections** → **Add Connection**.
2. Select **Databricks Unity Catalog** connector.
3. Provide: workspace URL, personal access token (or service principal), catalog scope.
4. Schedule ingestion (full or incremental).
5. Map harvested assets to Collibra domains and communities.

---

## Data Lineage

Collibra visualises end-to-end lineage: from raw source tables through transformations to final reports.

- **Technical lineage**: column-to-column mapping captured by connectors (Databricks, dbt, JDBC).
- **Business lineage**: logical flow from source systems to business reports.
- **Impact analysis**: see what downstream assets are affected when an upstream table changes.

---

## Data Stewardship

Data stewards are responsible for the quality and governance of a set of assets.

| Role | Responsibility |
| ---- | -------------- |
| Data Owner | Accountable for the data domain; approves policy changes |
| Data Steward | Day-to-day curation; approves asset definitions |
| Data Custodian | Technical owner; manages access and storage |

Stewards work through **workflows** (approval chains) in Collibra to promote assets from Draft to Approved.

---

## Data Quality

Collibra DQ (formerly Owl Analytics) integrates data quality rules with catalog assets.

- Define rules on datasets (completeness, uniqueness, range checks, regex patterns).
- Run quality scans on a schedule or triggered by pipeline completion.
- Attach quality scores to catalog assets — visible to consumers.
- Set thresholds that trigger alerts or block pipeline promotion.

---

## Policies and Data Usage

Collibra Policy Manager defines:

- **Data classifications** (Public, Internal, Confidential, Restricted).
- **Retention policies** (how long data is kept).
- **Usage policies** (who can use data, for what purpose).
- **Privacy policies** (GDPR, CCPA obligations).

See [data_usage.md](data_usage.md) and [dsa.md](dsa.md) for how policies translate into access agreements.

---

## REST API

```bash
# Authenticate (basic auth or OAuth)
TOKEN=$(curl -s -X POST https://your-org.collibra.com/rest/2.0/auth/sessions \
  -H "Content-Type: application/json" \
  -d '{"username":"api_user","password":"<password>"}' | jq -r '.csrfToken')

# Search assets
curl -X GET "https://your-org.collibra.com/rest/2.0/assets?name=payments&nameMatchMode=ANYWHERE" \
  -H "Authorization: Bearer $TOKEN"

# Get asset details
curl -X GET "https://your-org.collibra.com/rest/2.0/assets/<asset-id>" \
  -H "Authorization: Bearer $TOKEN"
```

Python SDK:

```python
from collibra_core import ApiClient, Configuration, AssetsApi

config = Configuration(host="https://your-org.collibra.com/rest/2.0")
config.username = "api_user"
config.password = "<password>"

with ApiClient(config) as client:
    api = AssetsApi(client)
    result = api.find_assets(name="payments", name_match_mode="ANYWHERE")
    for asset in result.results:
        print(asset.name, asset.type.name)
```

---

## Related

- [dsa.md](dsa.md) — Data Sharing / Stewardship Agreements
- [data_usage.md](data_usage.md) — Data usage policies and classifications
- [unity_catalog.md](../databricks/unity_catalog.md) — Databricks Unity Catalog
- [permissions.md](../databricks/permissions.md) — Unity Catalog GRANT model
