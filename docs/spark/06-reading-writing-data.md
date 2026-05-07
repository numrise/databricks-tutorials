# Reading & Writing Data

## Supported Formats

### CSV

```python
# Read CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# Read with options
df = spark.read.options(
    header=True,
    inferSchema=True,
    delimiter=",",
    encoding="UTF-8"
).csv("data.csv")

# Write CSV
df.write.csv("output.csv", header=True, mode="overwrite")
```

### JSON

```python
# Read JSON
df = spark.read.json("data.json")

# Multi-line JSON
df = spark.read.option("multiLine", True).json("data.json")

# Write JSON
df.write.json("output.json", mode="overwrite")
```

### Parquet

```python
# Read Parquet
df = spark.read.parquet("data.parquet")

# Write Parquet
df.write.parquet("output.parquet", mode="overwrite")
```

Parquet advantages:
- Columnar format (efficient storage)
- Compressed by default
- Schema preserved
- Best for large datasets

### Text

```python
# Read text
df = spark.read.text("data.txt")

# Write text
df.write.text("output.txt")
```

### Database (JDBC)

```python
# Read from database
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "employees") \
    .option("user", "username") \
    .option("password", "password") \
    .load()

# Write to database
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "employees") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("overwrite") \
    .save()
```

## Write Modes

| Mode | Behavior |
|------|----------|
| `overwrite` | Replace existing data |
| `append` | Add to existing data |
| `ignore` | Skip if exists |
| `error` | Error if exists (default) |

## Partitioning

Partition data for better performance:

```python
# Write partitioned by column
df.write \
    .partitionBy("year", "month") \
    .mode("overwrite") \
    .csv("output/")

# Output structure:
# output/
#   year=2024/
#     month=01/
#       part-00000.csv
```

## Schema Management

### Automatic Inference (slower)
```python
df = spark.read.csv("data.csv", inferSchema=True)
```

### Explicit Schema (faster, recommended)
```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

schema = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("age", IntegerType())
])

df = spark.read.schema(schema).csv("data.csv")
```

## Handling Missing Data

```python
# Replace nulls
df = df.na.fill(0)
df = df.na.fill({"age": 0, "salary": 50000})

# Drop nulls
df = df.na.drop()
df = df.na.drop(how="any", subset=["id", "email"])

# Replace values
df = df.na.replace(to_replace=["NA", ""], value="Unknown")
```

## Example: Read, Transform, Write Pipeline

```python
from pyspark.sql.functions import col, when, upper

# Read
raw_df = spark.read.csv("raw_data.csv", header=True, inferSchema=True)

# Transform
clean_df = (raw_df
    .dropDuplicates(["email"])
    .na.fill({"age": 0})
    .withColumn("name", upper(col("name")))
    .filter(col("age") > 0)
)

# Write
clean_df.write \
    .mode("overwrite") \
    .partitionBy("country") \
    .parquet("clean_data/")
```

## Performance Tips

1. **Choose right format** - Parquet > CSV/JSON > Text
2. **Partition data** - Improves query performance
3. **Compress files** - Reduces storage (gzip, snappy)
4. **Use explicit schema** - Avoids inference overhead
5. **Handle nulls early** - Clean data before processing

## Next Steps

- Explore [Performance Tuning](performance-tuning.md)
