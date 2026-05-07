# Spark Fundamentals

## Core Concepts

### What is Apache Spark?

Apache Spark is a fast, distributed computing framework for processing large-scale data. It provides APIs in Python, Java, Scala, and SQL.

**Key Features**:
- **Fast**: In-memory computation, 100x faster than Hadoop MapReduce
- **Distributed**: Process data across multiple machines
- **General-purpose**: Batch processing, streaming, ML, SQL
- **Easy to use**: High-level APIs

### Spark Architecture

```
┌─────────────────────────────────────────┐
│     Spark Application (Driver)          │
├─────────────────────────────────────────┤
│     SparkContext / SparkSession         │
├─────────────────────────────────────────┤
│        Cluster Manager (YARN/Mesos)     │
├─────────────────────────────────────────┤
│  Executor  │  Executor  │  Executor     │
│  (tasks)   │  (tasks)   │  (tasks)      │
└─────────────────────────────────────────┘
```

### Execution Modes

1. **Local Mode**: Run locally on single machine
   ```bash
   pyspark --master local
   ```

2. **Cluster Mode**: Run on Spark cluster
   ```bash
   spark-submit --master spark://hostname:7077 app.py
   ```

3. **YARN Mode**: Run on Hadoop YARN
   ```bash
   spark-submit --master yarn app.py
   ```

4. **Kubernetes Mode**: Run on K8s
   ```bash
   spark-submit --master k8s://apiserver:port app.py
   ```

## RDD (Resilient Distributed Dataset)

### What is an RDD?

- Fundamental data structure of Spark
- Immutable distributed collection of objects
- Can be processed in parallel
- Fault-tolerant

### Creating RDDs

```python
from pyspark import SparkContext

sc = SparkContext("local", "RDD Example")

# From Python collection
rdd1 = sc.parallelize([1, 2, 3, 4, 5])

# From external storage
rdd2 = sc.textFile("hdfs://path/to/file.txt")

# From another RDD
rdd3 = rdd1.map(lambda x: x * 2)
```

### RDD Operations

**Transformations** (lazy - not executed immediately):
```python
# map: apply function to each element
rdd2 = rdd1.map(lambda x: x * 2)

# filter: keep elements matching condition
rdd3 = rdd1.filter(lambda x: x > 2)

# flatMap: map then flatten
rdd4 = rdd1.flatMap(lambda x: [x, x*2])

# union: combine two RDDs
rdd5 = rdd1.union(rdd2)
```

**Actions** (trigger execution):
```python
# collect: return all elements to driver
result = rdd1.collect()

# count: return number of elements
count = rdd1.count()

# first: return first element
first = rdd1.first()

# take: return first n elements
first_3 = rdd1.take(3)

# saveAsTextFile: write to file
rdd1.saveAsTextFile("hdfs://path/output")
```

### Example: Word Count with RDD

```python
text_rdd = sc.textFile("data.txt")

# Split into words, count occurrences
word_counts = (text_rdd
    .flatMap(lambda line: line.split())  # Split lines into words
    .map(lambda word: (word, 1))          # Create (word, 1) pairs
    .reduceByKey(lambda a, b: a + b)      # Sum counts by key
)

# Show results
word_counts.collect()
```

## DataFrame

### What is a DataFrame?

- Distributed collection of data organized in named columns
- Similar to SQL table or pandas DataFrame
- Optimized for SQL operations
- **Preferred over RDDs for most use cases**

### Creating DataFrames

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrame").getOrCreate()

# From list of tuples
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])

# From dictionary
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30}
]
df = spark.createDataFrame(data)

# From pandas DataFrame
import pandas as pd
pdf = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
df = spark.createDataFrame(pdf)

# From CSV file
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# From JSON file
df = spark.read.json("data.json")
```

### DataFrame Operations

```python
# Show
df.show()

# Schema
df.printSchema()

# Select columns
df.select("name", "age").show()

# Filter
df.filter(df.age > 25).show()

# GroupBy
df.groupBy("age").count().show()

# Sort
df.sort("age").show()
```

## Transformations vs Actions

| Type | Nature | Example |
|------|--------|---------|
| **Transformation** | Lazy (not executed) | map, filter, select, groupBy |
| **Action** | Eager (executed immediately) | collect, count, show, write |

### Lazy Evaluation

```python
# These are NOT executed yet
df2 = df.filter(df.age > 25)
df3 = df2.select("name")

# This triggers execution
df3.show()
```

This optimization allows Spark to optimize the entire pipeline before execution.

## SparkContext vs SparkSession

| SparkContext | SparkSession |
|--------------|--------------|
| Entry point for RDD API | Entry point for DataFrames/SQL |
| Lower-level operations | High-level operations |
| Created first | Created automatically with SparkSession |

**Modern approach**: Use `SparkSession`

```python
spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()

# Access SparkContext if needed
sc = spark.sparkContext
```

## Practice Exercise

Create a program that:
1. Generates sample data (10 people with names and ages)
2. Filters people older than 28
3. Groups by age ranges (20-25, 26-30, 30+)
4. Counts per group
5. Displays results

**Solution**: See `../../scripts/data_processing/spark_fundamentals_exercise.py`

## Next Steps

- Continue with [RDDs vs DataFrames](03-rdds-vs-dataframes.md)
- Explore [Working with DataFrames](04-working-with-dataframes.md)
- Try the example scripts
