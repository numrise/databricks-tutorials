# Cost Optimization

## Understanding DBUs

Databricks pricing is based on DBUs (Databricks Units):

- 1 DBU = 1 virtual processor per hour
- Different workload types have different DBU costs
- All-purpose clusters: ~0.4 DBU/vCPU/hour
- Jobs clusters: ~0.25 DBU/vCPU/hour

## Cost Optimization Strategies

### 1. Right-Size Clusters

```
Cluster Size Impact:
- Small cluster (2 workers): Lower cost, slower
- Large cluster (20+ workers): Higher cost, faster
- Find balance for your workload
```

Use cluster auto-scaling:

```
Min workers: 2
Max workers: 10  # Auto-scales based on demand
```

### 2. Enable Auto-Termination

Set idle timeout to automatically stop clusters:

```
Auto-terminate after: 15-30 minutes
```

This prevents costly idle clusters.

### 3. Use Job Clusters

Job clusters are 50% cheaper than all-purpose:

```python
# For scheduled jobs, use job clusters
# For interactive development, use all-purpose
```

### 4. Use Spot Instances

Spot instances can save 60-80% on compute:

```
Availability: Azure Spot instances
Configuration: Enable spot in cluster settings
```

### 5. Batch Processing

Group jobs to run during off-peak hours:

```python
# Run expensive jobs at night
# Schedule multiple jobs together
```

## Monitoring Costs

### View Compute Hours

1. Go to Admin Settings
2. Click "Compute" tab
3. View DBU consumption by cluster

### Set Budget Alerts

1. In Azure Portal: **Cost Management + Billing**
2. Set up **Budget** alerts
3. Get notified when spending exceeds threshold

## Cost Breakdown Example

```
Monthly costs (sample):
- Compute (100 DBUs/day): $1,500
- Storage (1TB): $20
- Data transfer: $50
Total: ~$1,570/month

With optimization (30% reduction):
- Use spot instances: -30%
- Auto-terminate: -10%
- Smaller clusters: -20%
Total savings: ~$470/month (30%)
```

## Optimization Checklist

- [ ] Enable auto-termination on all clusters
- [ ] Use spot instances where possible
- [ ] Right-size cluster configurations
- [ ] Use job clusters for scheduled work
- [ ] Consolidate data processing jobs
- [ ] Archive old data to cold storage
- [ ] Remove unused clusters
- [ ] Monitor spending regularly

## Example: Cost-Optimized Workflow

```python
# Create small, ephemeral cluster for job
spark = SparkSession.builder \
    .appName("OptimizedJob") \
    .config("spark.executor.instances", "3") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()

# Process data efficiently
df = spark.read.parquet("data/")
result = df.groupBy("category").count()
result.write.parquet("output/")

# Cluster auto-terminates after 15 minutes idle
```

## Next Steps

- Review your current Databricks spend
- Implement top 3 optimization strategies
- Set up budget monitoring
