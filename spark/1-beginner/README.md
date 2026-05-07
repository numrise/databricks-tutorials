# Apache Spark - Beginner Level

Welcome to Apache Spark! This guide covers essential concepts to get you started.

## Table of Contents

1. [Installation & Setup](01-installation-setup.md)
2. [Spark Fundamentals](02-spark-fundamentals.md)
3. [RDDs vs DataFrames](03-rdds-vs-dataframes.md)
4. [Working with DataFrames](04-working-with-dataframes.md)
5. [Spark SQL Basics](05-spark-sql-basics.md)
6. [Reading & Writing Data](06-reading-writing-data.md)

## Prerequisites

- Python 3.8 or higher
- Java 8 or 11
- Basic Python knowledge
- Terminal/Command line familiarity

## Learning Objectives

By the end of this section, you will understand:

- ✅ How to install and configure Spark
- ✅ Core Spark concepts (RDDs, DataFrames, Datasets)
- ✅ Transformations and Actions
- ✅ How to read and write data
- ✅ Basic Spark SQL operations
- ✅ How to run Spark applications locally

## Quick Start

### 1. Install Spark

```bash
# Run the setup script
bash ../../scripts/setup-spark.sh

# Verify installation
spark-submit --version
```

### 2. Start PySpark Shell

```bash
pyspark
```

### 3. First Program

```python
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder.appName("HelloWorld").getOrCreate()

# Create a simple DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])

# Display
df.show()

# Output:
# +-------+---+
# |   name|age|
# +-------+---+
# |  Alice| 25|
# |    Bob| 30|
# |Charlie| 35|
# +-------+---+
```

## Common Tasks

### Count Records
```python
df.count()
```

### Filter Data
```python
df.filter(df.age > 25).show()
```

### Select Columns
```python
df.select("name").show()
```

### Group & Aggregate
```python
df.groupBy("age").count().show()
```

## Troubleshooting

**Issue**: Java not found
```bash
# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

**Issue**: Spark command not found
```bash
# Add Spark to PATH
export SPARK_HOME=~/spark-3.5.0-bin-hadoop3
export PATH=$PATH:$SPARK_HOME/bin
```

## Next Steps

- Complete the tutorials in order
- Run the example scripts
- Experiment with sample data
- Move to Intermediate level

## Resources

- [Official Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-getting-started.html)
