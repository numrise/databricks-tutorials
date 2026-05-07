# Performance Tuning

## Query Optimization Techniques

### Predicate Pushdown

Filter early to reduce data processed:

```python
# Inefficient - processes all data then filters
df = spark.read.parquet("large_file")
df.filter(df.year == 2024).show()

# Efficient - filters during read
df = spark.read.parquet("large_file").filter(df.year == 2024).show()
```

### Column Pruning

Select only needed columns:

```python
# Inefficient
df = spark.read.csv("data.csv")
result = df.select("id", "name").show()

# Efficient
df = spark.read.csv("data.csv", select=["id", "name"])
result = df.show()
```

### Broadcast Join

Small table broadcasts to all executors:

```python
from pyspark.sql.functions import broadcast

result = large_df.join(broadcast(small_df), "id")
```

### Bucketing

Organize data for efficient joins:

```python
df.write \
    .bucketBy(10, "id") \
    .mode("overwrite") \
    .saveAsTable("employees")
```

## Configuration Tuning

```python
spark = SparkSession.builder \
    .appName("Tuned") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()
```

## Partitioning Strategy

```python
# Write partitioned by common filters
df.write \
    .partitionBy("year", "month") \
    .mode("overwrite") \
    .parquet("output/")

# Subsequent queries are faster
spark.read.parquet("output/year=2024/").count()
```

## Caching

```python
df = spark.read.csv("data.csv").filter(df.amount > 1000)

# Cache for reuse
df.cache()

# Use cached data
df.count()
df.show()

# Remove from cache
df.unpersist()
```

## Explain Plans

```python
# Show execution plan
df.explain()

# Show extended plan
df.explain(extended=True)

# Show costs
df.explain(mode="cost")
```

## Best Practices

1. **Filter early** - Reduce data before transformations
2. **Use Parquet** - Columnar format is efficient
3. **Partition data** - Improves query performance
4. **Cache strategically** - Only when reused multiple times
5. **Broadcast small tables** - For efficient joins
6. **Monitor performance** - Use web UI at port 4040

## Monitoring

Access Spark UI at `http://localhost:4040` (or driver hostname:4040) to:
- View job execution
- Check task distribution
- Monitor memory usage
- Debug performance issues

## Next Steps

- Explore Databricks platform
- Learn advanced streaming patterns
- Study machine learning workflows
