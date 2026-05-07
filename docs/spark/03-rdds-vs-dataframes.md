# RDDs vs DataFrames

## Quick Comparison

| Aspect | RDD | DataFrame |
|--------|-----|-----------|
| Type | Generic collection | Structured collection with schema |
| Schema | No schema | Has schema |
| Optimization | No built-in optimization | Catalyst optimizer |
| SQL | No SQL support | Full SQL support |
| Performance | Generally slower | Much faster |
| Ease of Use | More functional | More SQL-like |
| Memory | Store objects | Columnar format |
| Use Case | Unstructured data | Structured data |

## When to Use Each

### Use RDD When:
- Working with unstructured data
- Need low-level transformations
- Data doesn't fit tabular format
- Need fine-grained control

### Use DataFrame When:
- Working with structured/semi-structured data
- Need SQL operations
- Performance is critical
- Working with large datasets

## Examples

### RDD Approach

```python
from pyspark import SparkContext

sc = SparkContext("local", "RDD Example")

logs = sc.parallelize([
    "2024-01-01 ERROR: Connection failed",
    "2024-01-01 INFO: User login",
    "2024-01-02 ERROR: Memory exceeded"
])

errors = (logs
    .filter(lambda x: "ERROR" in x)
    .map(lambda x: x.split(" ")[1:])
)

errors.collect()
```

### DataFrame Approach

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("DataFrame Example").getOrCreate()

logs = spark.createDataFrame([
    ("2024-01-01", "ERROR", "Connection failed"),
    ("2024-01-01", "INFO", "User login"),
    ("2024-01-02", "ERROR", "Memory exceeded")
], ["date", "level", "message"])

logs.filter(col("level") == "ERROR").select("date", "message").show()
```

## Performance Comparison

DataFrame is typically **10-100x faster** than RDD for most operations!

## Interoperability

### Convert RDD to DataFrame

```python
rdd = spark.sparkContext.parallelize([(1, "a"), (2, "b")])
df = rdd.toDF(["id", "value"])
```

### Convert DataFrame to RDD

```python
rdd = df.rdd
```

## Best Practices

1. **Use DataFrames by default** - They're faster and easier
2. **Use RDDs only when necessary** - Unstructured data only
3. **Avoid RDD ↔ DataFrame cycles** - Stick with one format
4. **Cache strategically** - Cache intermediate results
5. **Use SQL when possible** - Highly optimized

## Next Steps

- Continue with [Working with DataFrames](04-working-with-dataframes.md)
- Explore [Spark SQL](05-spark-sql-basics.md)
