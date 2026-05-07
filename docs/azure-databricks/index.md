# Azure Databricks

Deploy and use Databricks on Microsoft Azure.

## What is Azure Databricks?

Azure Databricks is Databricks running natively on Azure, providing:
- Native Azure integration
- Enterprise security
- Compliance certifications
- Seamless Azure data services connection

## Key Benefits

- **Azure Integration** - Connect to Azure Data Lake, Blob Storage, SQL Database
- **Enterprise Security** - VNet, firewall, private endpoints
- **Compliance** - SOC 2, HIPAA, PCI DSS, GDPR
- **Cost Optimization** - Spot instances, reserved capacity
- **Data Governance** - Unity Catalog, row/column level security

## Getting Started

- [Setup on Azure](setup.md) - Initial deployment
- [Integration](integration.md) - Connect to Azure services
- [Cost Optimization](cost.md) - Reduce expenses

## Architecture

```
┌─────────────────────────────────┐
│     Azure Databricks Workspace  │
├─────────────────────────────────┤
│   Spark Clusters running on VMs │
├─────────────────────────────────┤
│   Connected Services:           │
│   - Data Lake Storage Gen2      │
│   - Blob Storage                │
│   - SQL Database                │
│   - Azure Data Factory          │
│   - Power BI                    │
└─────────────────────────────────┘
```

## Next Steps

- Follow [Setup on Azure](setup.md)
- Explore [Integration options](integration.md)
- Learn [Cost optimization](cost.md)
