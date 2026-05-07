# Working with DataFrames

## Creating DataFrames

### From Python Collections

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrames").getOrCreate()

# From list of tuples
data = [
    (1, "Alice", 25, "Engineering"),
    (2, "Bob", 30, "Sales"),
    (3, "Charlie", 35, "Marketing"),
    (4, "David", 28, "Engineering")
]

columns = ["id", "name", "age", "department"]
df = spark.createDataFrame(data, columns)
df.show()
```

### From Dictionary

```python
data = [
    {"id": 1, "name": "Alice", "salary": 50000},
    {"id": 2, "name": "Bob", "salary": 60000},
    {"id": 3, "name": "Charlie", "salary": 55000}
]

df = spark.createDataFrame(data)
df.show()
```

### From Pandas DataFrame

```python
import pandas as pd

pdf = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "David"],
    "age": [25, 30, 35, 28]
})

df = spark.createDataFrame(pdf)
df.show()
```

### From Files

```python
# CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# JSON
df = spark.read.json("data.json")

# Parquet
df = spark.read.parquet("data.parquet")

# Text file
df = spark.read.text("data.txt")
```

## DataFrame Operations

### Display & Inspection

```python
# Show first n rows (default 20)
df.show()
df.show(5)

# Show with truncation disabled
df.show(truncate=False)

# Print schema
df.printSchema()

# Get column names
df.columns

# Get row count
df.count()

# Get data types
df.dtypes

# Get summary statistics
df.describe().show()
df.describe(["age", "salary"]).show()

# Get summary for numeric columns
df.summary().show()
```

### Selection

```python
# Select single column
df.select("name").show()

# Select multiple columns
df.select("id", "name", "age").show()

# Select using expressions
from pyspark.sql.functions import col
df.select(col("name"), col("age")).show()

# Select with aliases
df.select(col("name").alias("employee_name")).show()

# Drop columns
df.drop("salary").show()
```

### Filtering

```python
# Simple filter
df.filter(df.age > 25).show()

# Filter with AND
df.filter((df.age > 25) & (df.department == "Engineering")).show()

# Filter with OR
df.filter((df.age > 35) | (df.salary > 55000)).show()

# Filter with NOT
df.filter(~(df.department == "HR")).show()

# Filter with IN
df.filter(df.department.isin(["Sales", "Marketing"])).show()

# Filter with LIKE
df.filter(df.name.like("Al%")).show()

# Filter with NULL
df.filter(df.email.isNull()).show()
df.filter(df.email.isNotNull()).show()
```

### Transformations

```python
# Add column
from pyspark.sql.functions import col, when, lit

df_new = df.withColumn("salary_doubled", df.salary * 2)

# Rename column
df_renamed = df.withColumnRenamed("age", "years_old")

# Drop column
df_dropped = df.drop("email")

# Update column value
df_updated = df.withColumn(
    "age",
    when(df.name == "Alice", 26).otherwise(df.age)
)

# Add constant column
df_const = df.withColumn("company", lit("TechCorp"))
```

### Aggregation

```python
from pyspark.sql.functions import count, sum, avg, min, max, collect_list

# Count rows
df.count()

# Count distinct values
df.select("department").distinct().count()

# Group by
df.groupBy("department").count().show()

# Multiple aggregations
df.groupBy("department").agg(
    count("*").alias("count"),
    avg("salary").alias("avg_salary"),
    max("age").alias("max_age")
).show()

# Multiple group by columns
df.groupBy("department", "age").count().show()

# Collect values into list
df.groupBy("department").agg(
    collect_list("name").alias("employees")
).show()
```

### Sorting

```python
from pyspark.sql.functions import desc, asc

# Sort ascending (default)
df.sort("age").show()

# Sort descending
df.sort(desc("salary")).show()

# Sort multiple columns
df.sort(asc("department"), desc("age")).show()

# Using orderBy (same as sort)
df.orderBy("age").show()
```

### Joins

```python
# Join on column
df1.join(df2, "employee_id").show()

# Join with condition
df1.join(df2, df1.emp_id == df2.id).show()

# Inner join (default)
df1.join(df2, "id", "inner").show()

# Left outer join
df1.join(df2, "id", "left").show()

# Right outer join
df1.join(df2, "id", "right").show()

# Full outer join
df1.join(df2, "id", "outer").show()

# Anti-join (rows not in right)
df1.join(df2, "id", "left_anti").show()
```

### Set Operations

```python
# Union (keeps duplicates)
df_combined = df1.union(df2)

# Union all
df_combined = df1.unionByName(df2)  # Match by column names

# Intersect (common rows)
df_common = df1.intersect(df2)

# Except (rows in df1 but not df2)
df_diff = df1.except(df2)

# Distinct
df_unique = df.distinct()
```

### Caching

```python
# Cache DataFrame in memory
df.cache()

# Remove from cache
df.unpersist()

# Check cache status
df.is_cached
```

## Schema & Data Types

### Working with Schema

```python
from pyspark.sql.types import *

# Define schema explicitly
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", DoubleType(), True)
])

df = spark.createDataFrame(data, schema)

# Get schema
schema = df.schema
print(schema)

# Get schema as string
schema_str = df.schema.simpleString()
```

### Data Type Conversions

```python
from pyspark.sql.functions import col, cast

# Cast to different type
df = df.withColumn("age_int", col("age").cast(IntegerType()))
df = df.withColumn("salary_string", col("salary").cast(StringType()))

# Cast multiple columns
df = df.select(
    col("id").cast(IntegerType()),
    col("name").cast(StringType()),
    col("salary").cast(DoubleType())
)
```

## Writing DataFrames

```python
# Write to CSV
df.write.csv("output.csv", header=True, mode="overwrite")

# Write to JSON
df.write.json("output.json", mode="overwrite")

# Write to Parquet
df.write.parquet("output.parquet", mode="overwrite")

# Write to table
df.write.mode("overwrite").saveAsTable("my_table")

# Write modes: overwrite, append, ignore, error (default)
```

## Practice Exercise

Given sample employee data, perform these operations:

```python
# Create sample data
employees = spark.createDataFrame([
    (101, "Alice", 28, "Engineering", 85000),
    (102, "Bob", 32, "Sales", 72000),
    (103, "Charlie", 26, "Engineering", 78000),
    (104, "David", 35, "Management", 95000),
    (105, "Eve", 29, "Sales", 68000)
], ["emp_id", "name", "age", "department", "salary"])

# TODO: 
# 1. Select employees in Engineering department
# 2. Calculate average salary by department
# 3. Find employees with salary > 75000
# 4. Add 10% bonus column
# 5. Sort by department and salary
```

**Solution**: See `../../scripts/data_processing/dataframe_operations.py`

## Next Steps

- Continue with [Spark SQL Basics](05-spark-sql-basics.md)
- Explore [Reading & Writing Data](06-reading-writing-data.md)
- Practice with example scripts
