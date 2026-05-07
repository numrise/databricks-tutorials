# Workspace & Clusters

## Understanding Workspaces

A Databricks workspace is your personal analytics environment containing:
- Notebooks for code development
- Clusters for computation
- Data connections
- Collaborators

## Managing Clusters

### Cluster Types

**All-Purpose Cluster**
- Use for ad-hoc analysis
- Shareable with team members
- Good for interactive development

**Job Cluster**
- Dedicated for scheduled jobs
- Auto-terminates after job completes
- Cost-effective for batch processing

### Cluster Configuration

When creating a cluster, configure:

1. **Runtime** - Databricks Runtime version
2. **Worker Type** - Machine size for workers
3. **Workers** - Number of worker nodes
4. **Auto-termination** - Idle time before shutdown
5. **Availability Zones** - For multi-zone deployments

### Cost Optimization

```
Tips for reducing costs:
- Enable auto-termination (15-30 minutes idle)
- Use smaller node types for testing
- Terminate unused clusters
- Schedule jobs during off-peak hours
- Use Spot instances (where available)
```

## Notebook Attachments

Attach notebooks to clusters:

1. Click the cluster selector (usually top-right)
2. Select your cluster
3. Wait for connection to establish

When attached, you can:
- Run Python, SQL, Scala, R code
- Access cluster-wide libraries
- Collaborate in real-time

## Workspace Navigation

| Location | Purpose |
|----------|---------|
| Workspace | Personal notebooks and projects |
| Shared | Team shared notebooks |
| Repos | Git-integrated repositories |
| Recents | Recently accessed items |

## Best Practices

1. **Organize by project** - Create folders for each project
2. **Name clearly** - Use descriptive notebook names
3. **Share appropriately** - Use permission controls
4. **Clean up** - Delete unused clusters to save costs
5. **Version control** - Use Repos for Git integration

## Next Steps

- Learn about [Notebooks](notebooks.md)
- Explore collaborative features
