# Working with DataFrames

## Creating DataFrames

### From Python Collections

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrames").getOrCreate()

data = [
    (1, "Alice", 25),
    (2, "Bob", 30),
    (3, "Charlie", 35)
]

columns = ["id", "name", "age"]
df = spark.createDataFrame(data, columns)
df.show()
```

### From Pandas

```python
import pandas as pd

pdf = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
})

df = spark.createDataFrame(pdf)
```

### From Files

```python
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.json("data.json")
df = spark.read.parquet("data.parquet")
```

## DataFrame Operations

### Display

```python
df.show()
df.show(5)
df.printSchema()
df.columns
df.count()
df.describe().show()
```

### Selection

```python
from pyspark.sql.functions import col

df.select("name").show()
df.select("id", "name").show()
df.select(col("name").alias("employee_name")).show()
df.drop("age").show()
```

### Filtering

```python
df.filter(df.age > 25).show()
df.filter((df.age > 25) & (df.name == "Alice")).show()
df.filter(df.department.isin(["Sales", "Marketing"])).show()
df.filter(df.email.isNotNull()).show()
```

### Aggregation

```python
from pyspark.sql.functions import count, sum, avg, max, min

df.groupBy("department").count().show()
df.groupBy("department").agg(
    count("*").alias("count"),
    avg("salary").alias("avg_salary")
).show()
```

### Sorting

```python
from pyspark.sql.functions import desc, asc

df.sort("age").show()
df.sort(desc("salary")).show()
df.sort(asc("department"), desc("age")).show()
```

### Joins

```python
df1.join(df2, "id").show()
df1.join(df2, df1.emp_id == df2.id).show()
df1.join(df2, "id", "inner").show()
df1.join(df2, "id", "left").show()
```

## Transformations

```python
from pyspark.sql.functions import col, when, upper, lower, concat, lit

df = df.withColumn("age_doubled", col("age") * 2)
df = df.withColumnRenamed("age", "years_old")
df = df.withColumn("name", upper(col("name")))
df = df.withColumn("category",
    when(col("age") < 30, "Young")
    .when(col("age") < 50, "Middle")
    .otherwise("Senior")
)
```

## Writing DataFrames

```python
df.write.csv("output.csv", header=True, mode="overwrite")
df.write.json("output.json", mode="overwrite")
df.write.parquet("output.parquet", mode="overwrite")
df.write.saveAsTable("my_table", mode="overwrite")
```

## Best Practices

1. **Use explicit schema** - Faster than inference
2. **Cache intermediate results** - Only when reused
3. **Filter early** - Reduce data before transformations
4. **Select only needed columns** - Avoid reading unnecessary data
5. **Partition data** - For better performance on large datasets

## Next Steps

- Learn [Spark SQL](05-spark-sql-basics.md)
- Explore [Data I/O](06-reading-writing-data.md)
