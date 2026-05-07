# Apache Spark Quickstart

## Prerequisites

- Java 8/11
- Python 3.6+ (for PySpark)
- Scala 2.12+ (optional)

## Installation

Download Spark:

TODO: Create script

```bash
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xvzf spark-3.5.0-bin-hadoop3.tgz
```

Set environment variables

```bash
export SPARK_HOME=\$PWD/spark-3.5.0-bin-hadoop3
export PATH=\$PATH:\$SPARK_HOME/bin
```

## Running Spark

Start the Spark shell:

```bash
pyspark         # For PySpark
spark-shell     # For Scala
```

Submit a job:

```bash
spark-submit your_script.py
```
