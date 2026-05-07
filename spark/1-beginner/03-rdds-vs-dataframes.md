# RDDs vs DataFrames

## Comparison

| Aspect | RDD | DataFrame |
|--------|-----|-----------|
| **Type** | Generic collection of objects | Structured collection with named columns |
| **Schema** | No schema | Has schema |
| **Optimization** | No built-in optimization | Uses Catalyst optimizer |
| **SQL** | No SQL support | Full SQL support |
| **Performance** | Generally slower | Much faster (optimized) |
| **Ease of Use** | More functional | More SQL-like, easier |
| **Type Safety** | Runtime type checks | Compile-time (Scala/Java) |
| **Memory** | Store objects in memory | Columnar format, compressed |
| **Use Case** | Unstructured data, complex operations | Structured data, analytics |

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

### RDD Example

```python
from pyspark import SparkContext

sc = SparkContext("local", "RDD Example")

# Create RDD of logs
logs = sc.parallelize([
    "2024-01-01 ERROR: Connection failed",
    "2024-01-01 INFO: User login",
    "2024-01-01 ERROR: Memory exceeded",
    "2024-01-02 INFO: Job completed"
])

# Extract errors only
errors = (logs
    .filter(lambda x: "ERROR" in x)
    .map(lambda x: x.split(" ")[1:])
)

errors.collect()
# [['ERROR:', 'Connection', 'failed'], 
#  ['ERROR:', 'Memory', 'exceeded']]
```

### DataFrame Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month

spark = SparkSession.builder.appName("DataFrame Example").getOrCreate()

# Create DataFrame
logs = spark.createDataFrame([
    ("2024-01-01", "ERROR", "Connection failed"),
    ("2024-01-01", "INFO", "User login"),
    ("2024-01-01", "ERROR", "Memory exceeded"),
    ("2024-01-02", "INFO", "Job completed")
], ["date", "level", "message"])

# Filter and select
logs.filter(col("level") == "ERROR").select("date", "message").show()

# Output:
# +----------+------------------+
# |      date|           message|
# +----------+------------------+
# |2024-01-01|  Connection failed|
# |2024-01-01|   Memory exceeded|
# +----------+------------------+
```

## Performance Comparison

```python
# RDD approach
rdd_result = (spark.sparkContext.parallelize(range(1000000))
    .map(lambda x: (x % 10, x))
    .reduceByKey(lambda a, b: a + b)
    .collect()
)

# DataFrame approach
df_result = (spark.range(1000000)
    .withColumn("key", col("id") % 10)
    .groupBy("key")
    .sum("id")
    .collect()
)

# DataFrame is typically 10-100x faster!
```

## Interoperability

### Convert RDD to DataFrame

```python
# From RDD of tuples
rdd = spark.sparkContext.parallelize([(1, "a"), (2, "b")])
df = rdd.toDF(["id", "value"])

# From RDD with schema
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

schema = StructType([
    StructField("id", IntegerType()),
    StructField("value", StringType())
])
df = spark.createDataFrame(rdd, schema=schema)
```

### Convert DataFrame to RDD

```python
# Convert to RDD of rows
rdd = df.rdd

# Convert to RDD of tuples
rdd = df.rdd.map(lambda row: (row.id, row.value))
```

## Best Practices

1. **Use DataFrames by default** - They're faster and easier
2. **Use RDDs only when necessary** - Unstructured data, low-level operations
3. **Avoid RDD -> DataFrame -> RDD cycles** - Stick with one format
4. **Cache strategically** - Cache intermediate results that are reused
5. **Use SQL when possible** - Highly optimized for DataFrames

## Practice Exercise

Convert the following RDD operations to DataFrame operations and compare performance:

```python
# RDD version
rdd = spark.sparkContext.parallelize([
    (1, "Alice", 25),
    (2, "Bob", 30),
    (3, "Charlie", 25),
    (4, "David", 30),
    (5, "Eve", 25)
])

result = (rdd
    .filter(lambda x: x[2] > 26)
    .map(lambda x: (x[2], 1))
    .reduceByKey(lambda a, b: a + b)
    .collect()
)

# TODO: Write DataFrame equivalent
# Expected output: [(30, 2)]
```

**Solution**: See `../../scripts/data_processing/rdd_vs_dataframe.py`

## Next Steps

- Continue with [Working with DataFrames](04-working-with-dataframes.md)
- Explore [Spark SQL Basics](05-spark-sql-basics.md)
