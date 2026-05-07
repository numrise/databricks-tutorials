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
┌─────────────────────────────────┐
│     Spark Application (Driver)  │
├─────────────────────────────────┤
│     SparkContext / SparkSession │
├─────────────────────────────────┤
│   Cluster Manager (YARN/Mesos)  │
├─────────────────────────────────┤
│ Executor | Executor | Executor  │
│ (tasks)  | (tasks)  | (tasks)   │
└─────────────────────────────────┘
```

## Execution Modes

- **Local Mode**: Run on single machine
- **Cluster Mode**: Run on Spark cluster
- **YARN Mode**: Run on Hadoop YARN
- **Kubernetes Mode**: Run on K8s

## RDD (Resilient Distributed Dataset)

### What is an RDD?

- Fundamental data structure of Spark
- Immutable distributed collection
- Can be processed in parallel
- Fault-tolerant

### Creating RDDs

```python
from pyspark import SparkContext

sc = SparkContext("local", "RDD Example")

# From Python collection
rdd1 = sc.parallelize([1, 2, 3, 4, 5])

# From external storage
rdd2 = sc.textFile("path/to/file.txt")

# From another RDD
rdd3 = rdd1.map(lambda x: x * 2)
```

### RDD Operations

**Transformations** (lazy):
```python
rdd2 = rdd1.map(lambda x: x * 2)
rdd3 = rdd1.filter(lambda x: x > 2)
rdd4 = rdd1.flatMap(lambda x: [x, x*2])
```

**Actions** (trigger execution):
```python
result = rdd1.collect()
count = rdd1.count()
first = rdd1.first()
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

spark = SparkSession.builder.appName("Example").getOrCreate()

# From list of tuples
data = [("Alice", 25), ("Bob", 30)]
df = spark.createDataFrame(data, ["name", "age"])

# From pandas
import pandas as pd
pdf = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
df = spark.createDataFrame(pdf)

# From CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)
```

## SparkSession

SparkSession is the entry point for Spark functionality:

```python
spark = SparkSession.builder \
    .appName("MyApp") \
    .master("local") \
    .getOrCreate()
```

## Practice Exercise

Create a program that:
1. Creates a DataFrame with sample data
2. Filters rows based on a condition
3. Calculates aggregations
4. Displays results

See `scripts/utils/spark_utils.py` for example utilities.

## Next Steps

- Proceed to [RDDs vs DataFrames](03-rdds-vs-dataframes.md)
- Explore [Working with DataFrames](04-working-with-dataframes.md)
