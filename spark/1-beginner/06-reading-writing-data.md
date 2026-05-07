# Reading & Writing Data

## Data Formats

### CSV Files

**Reading CSV**:
```python
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# With options
df = spark.read.options(
    header=True,
    inferSchema=True,
    delimiter=",",
    encoding="UTF-8"
).csv("data.csv")
```

**Writing CSV**:
```python
df.write.csv("output.csv", header=True, mode="overwrite")
```

### JSON Files

**Reading JSON**:
```python
df = spark.read.json("data.json")

# Multi-line JSON
df = spark.read.option("multiLine", True).json("data.json")
```

**Writing JSON**:
```python
df.write.json("output.json", mode="overwrite")
```

### Parquet Files

**Reading Parquet**:
```python
df = spark.read.parquet("data.parquet")
```

**Writing Parquet**:
```python
df.write.parquet("output.parquet", mode="overwrite")
```

Parquet is:
- Columnar format (efficient storage)
- Compressed
- Schema preserved
- **Best for large datasets**

### Text Files

**Reading Text**:
```python
df = spark.read.text("data.txt")
```

**Writing Text**:
```python
df.write.text("output.txt")
```

### Database Tables

**Reading from JDBC**:
```python
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "employees") \
    .option("user", "username") \
    .option("password", "password") \
    .load()
```

**Writing to JDBC**:
```python
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

```python
df.write.mode("overwrite").csv("output.csv")
df.write.mode("append").csv("output.csv")
df.write.mode("ignore").csv("output.csv")
```

## Partitioning

Partition data for better performance:

```python
# Write partitioned by department
df.write \
    .partitionBy("department") \
    .mode("overwrite") \
    .csv("output/")

# Output structure:
# output/
#   department=Engineering/
#     part-00000.csv
#   department=Sales/
#     part-00000.csv
```

**Reading partitioned data**:
```python
df = spark.read.csv("output/")
```

## Schema Inference vs Definition

**Automatic inference (slower)**:
```python
df = spark.read.csv("data.csv", inferSchema=True)
```

**Explicit schema (faster, recommended)**:
```python
from pyspark.sql.types import *

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
df = df.na.fill(0)  # Fill all with 0
df = df.na.fill({"age": 0, "salary": 50000})  # Fill specific columns

# Drop nulls
df = df.na.drop()  # Drop any row with null
df = df.na.drop(how="any", subset=["id", "email"])  # Drop if specific columns null
df = df.na.drop(how="all")  # Drop only if all columns null

# Replace values
df = df.na.replace(to_replace=["NA", ""], value="Unknown")
```

## Example: Read & Transform Pipeline

```python
from pyspark.sql.functions import col, when, upper

# Read CSV
raw_df = spark.read.csv("raw_data.csv", header=True, inferSchema=True)

# Clean and transform
clean_df = (raw_df
    # Remove duplicates
    .dropDuplicates(["email"])
    
    # Fill missing values
    .na.fill({"age": 0, "country": "Unknown"})
    
    # Standardize columns
    .withColumn("name", upper(col("name")))
    
    # Filter
    .filter(col("age") > 0)
    
    # Drop unnecessary columns
    .drop("internal_id")
)

# Write transformed data
clean_df.write \
    .mode("overwrite") \
    .partitionBy("country") \
    .parquet("clean_data/")

# Verify
spark.read.parquet("clean_data/").show()
```

## Performance Tips

1. **Choose right format**: Parquet > CSV/JSON > Text
2. **Partition data**: Improves query performance
3. **Compress files**: Reduces storage (gzip, snappy)
4. **Validate schema**: Use explicit schema vs inference
5. **Handle nulls early**: Clean data before processing

## Next Steps

- Review all [Beginner](README.md) tutorials
- Move to [Intermediate](../../2-intermediate/README.md)
- Try combining multiple skills
