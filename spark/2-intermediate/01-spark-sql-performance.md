# Spark SQL Performance Tuning

## Query Optimization Techniques

### 1. Predicate Pushdown

Filter early to reduce data processed:

```python
# ❌ Inefficient - processes all data then filters
df = spark.read.parquet("large_file")
df.filter(df.year == 2024).show()

# ✅ Efficient - filters during read
df = spark.read.parquet("large_file")
    .filter(df.year == 2024)
    .show()
```

### 2. Column Pruning

Select only needed columns:

```python
# ❌ Inefficient
df = spark.read.csv("data.csv")
result = df.select("id", "name").show()

# ✅ Efficient
df = spark.read.csv("data.csv", select=["id", "name"]).show()
```

### 3. Broadcast Join

Small table broadcasts to all executors:

```python
from pyspark.sql.functions import broadcast

# Automatic for small tables
result = large_df.join(broadcast(small_df), "id")

# Manual specification
result = large_df.join(
    broadcast(small_df),
    "id",
    "inner"
)
```

### 4. Bucketing

Organize data for efficient joins:

```python
# Write bucketed data
df.write \
    .bucketBy(10, "id") \
    .mode("overwrite") \
    .saveAsTable("employees")

# Subsequent joins are faster
spark.sql("""
    SELECT * FROM employees e
    JOIN salaries s ON e.id = s.emp_id
""")
```

## Query Plans

### Explain Plans

```python
# Show execution plan
df.explain()

# Show extended plan
df.explain(extended=True)

# Show costs
df.explain(mode="cost")
```

### Catalyst Optimizer

Spark automatically optimizes:
- Join order
- Predicate pushdown
- Column pruning
- Constant folding

## Partitioning Strategy

### Partition by Common Filters

```python
# Write partitioned by year
df.write \
    .partitionBy("year", "month") \
    .mode("overwrite") \
    .parquet("output/")

# Queries by year are much faster
spark.read.parquet("output/year=2024/").count()
```

## Caching Strategy

### When to Cache

```python
df = (spark.read.csv("data.csv")
    .filter(df.amount > 1000)
)

# Cache for reuse
df.cache()

# Use cached data
df.count()
df.show()

# Remove from cache
df.unpersist()
```

## Performance Monitoring

### View Metrics

```python
# Get metrics from SparkContext
metrics = spark.sparkContext._jvm.org.apache.spark.metrics.MetricsSystem

# View web UI
# http://localhost:4040 (or driver hostname:4040)
```

## Advanced Techniques

### Salting for Skewed Joins

```python
from pyspark.sql.functions import col, concat, rand

# Add salt to right table
df_right_salted = df_right.withColumn(
    "salt",
    (rand() * 10).cast("integer")
)

# Explode left table with multiple salts
from pyspark.sql.functions import explode, array, lit
df_left_salted = df_left.withColumn(
    "salt",
    explode(array([lit(i) for i in range(10)]))
)

# Join on both key and salt
result = df_left_salted.join(
    df_right_salted,
    (col("id") == col("r_id")) & (col("salt") == col("r_salt"))
)
```

## Configuration Tuning

```python
spark = SparkSession.builder \
    .appName("Tuned") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

## Practice Exercise

Optimize this slow query:

```python
# Slow version
result = (spark.read.csv("customers.csv")
    .join(spark.read.csv("orders.csv"), "id")
    .filter(col("year") == 2024)
    .groupBy("region")
    .agg({"amount": "sum"})
    .show()
)

# TODO: Optimize using techniques above
```

## Next Steps

- Continue with [Window Functions](02-window-functions.md)
- Explore [Complex Transformations](03-complex-transformations.md)
