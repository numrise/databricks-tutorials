# Installation & Setup

## Prerequisites

- **Python**: 3.8 or higher
- **Java**: 8 or 11 (OpenJDK recommended)
- **Memory**: Minimum 4GB RAM
- **Disk Space**: 2GB for Spark installation

## Installation Steps

### 1. Install Java

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install openjdk-11-jdk
java -version
```

**macOS**:
```bash
brew install openjdk@11
export PATH="/usr/local/opt/openjdk@11/bin:$PATH"
```

**Windows**:
- Download from [OpenJDK website](https://adoptopenjdk.net/)
- Follow installation wizard
- Add to PATH

### 2. Install Python

Recommended: Use Python 3.9 or 3.10

```bash
python --version
pip install --upgrade pip
```

### 3. Download Spark

```bash
# Navigate to download directory
cd ~/Downloads

# Download Spark 3.5.0 (latest stable)
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz

# Extract
tar -xzf spark-3.5.0-bin-hadoop3.tgz

# Move to home directory
mv spark-3.5.0-bin-hadoop3 ~/spark-3.5.0
```

### 4. Configure Environment Variables

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export SPARK_HOME=~/spark-3.5.0
export PATH=$PATH:$SPARK_HOME/bin
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64  # Adjust path as needed
```

Reload shell:
```bash
source ~/.bashrc
```

### 5. Install PySpark

```bash
pip install pyspark==3.5.0
```

### 6. Verify Installation

```bash
# Check Spark
spark-submit --version

# Check Java
java -version

# Check Python
python --version

# Start PySpark shell
pyspark
```

In the PySpark shell:
```python
spark.version
spark.range(5).show()
```

## Docker Alternative

For isolated environment without local installation:

```bash
# Pull Spark Docker image
docker pull bitnami/spark:latest

# Run container
docker run -it bitnami/spark:latest \
  pyspark
```

## Troubleshooting

### "spark-submit: command not found"
```bash
# Add to PATH
export PATH=$PATH:~/spark-3.5.0/bin
```

### "JAVA_HOME not found"
```bash
# Set JAVA_HOME explicitly
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

### Python version mismatch
```bash
# Use Python 3.9+
python3 --version
# Use python3 explicitly
python3 -m pyspark
```

### "Error: bind: Address already in use"
- Spark UI port (4040) is occupied
- Kill existing Spark process or use different port

```bash
lsof -i :4040  # Find process
kill -9 <PID>  # Kill it
```

## Installation Verification Script

```python
# test_installation.py
from pyspark.sql import SparkSession
import sys

print(f"Python version: {sys.version}")

spark = SparkSession.builder \
    .appName("InstallationTest") \
    .getOrCreate()

print(f"Spark version: {spark.version}")

# Create test data
data = range(100)
rdd = spark.sparkContext.parallelize(data)
print(f"RDD count: {rdd.count()}")

# Create DataFrame
df = spark.createDataFrame([(i, i*2) for i in range(10)], ["id", "value"])
print("DataFrame created successfully")
df.show()

print("\n✅ Installation verified successfully!")
```

Run it:
```bash
python test_installation.py
```

## Next Steps

- Move to [Spark Fundamentals](02-spark-fundamentals.md)
- Explore Spark documentation
- Try example scripts
