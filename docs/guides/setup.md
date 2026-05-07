# Getting Started

Complete setup guide for your Databricks environment.

## System Requirements

### For Local Spark Development

- Python 3.8 or later
- Java Development Kit (JDK) 8 or 11
- 4GB RAM minimum (8GB recommended)
- 2GB disk space

### For Cloud Platforms

- Active subscription (AWS, Azure, or Google Cloud)
- Sufficient quota for cluster resources
- Network connectivity to cloud provider

## Installation Steps

### Step 1: Install Java

**Linux/macOS:**
```bash
# Using Homebrew (macOS)
brew install openjdk@11

# Or install from Oracle
# Download from: https://www.oracle.com/java/technologies/javase-jdk11-downloads.html
```

**Windows:**
- Download JDK from Oracle
- Run installer and follow prompts
- Set JAVA_HOME environment variable

Verify installation:
```bash
java -version
```

### Step 2: Install Python

**macOS/Linux:**
```bash
# Using system package manager
sudo apt-get install python3 python3-pip  # Debian/Ubuntu
brew install python3  # macOS
```

**Windows:**
- Download from python.org
- Run installer (check "Add Python to PATH")

Verify:
```bash
python3 --version
pip3 --version
```

### Step 3: Install Spark Locally

```bash
# Download Spark (choose a mirror)
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz

# Extract
tar -xzf spark-3.5.0-bin-hadoop3.tgz

# Move to standard location
mv spark-3.5.0-bin-hadoop3 ~/spark

# Add to PATH
export SPARK_HOME=~/spark
export PATH=$PATH:$SPARK_HOME/bin
```

### Step 4: Install PySpark

```bash
pip3 install pyspark
```

### Step 5: Verify Installation

```bash
pyspark
# Should start Spark shell

# Or test with Python
python3 -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.appName('test').getOrCreate(); print('Success!')"
```

## Environment Variables

Add to your shell profile (~/.bashrc, ~/.zshrc, or ~/.bash_profile):

```bash
export JAVA_HOME=/usr/libexec/java_home  # macOS
export SPARK_HOME=$HOME/spark
export PATH=$PATH:$SPARK_HOME/bin
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
```

Reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

## IDE Setup

### VS Code

1. Install Python extension
2. Install Apache Spark extension
3. Create test_spark.py:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("VSCode").getOrCreate()
df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
df.show()
```

4. Run with F5

### PyCharm

1. Install PyCharm Community or Professional
2. Add Python interpreter pointing to virtual environment
3. Configure PySpark in Run Configuration:
   - Set SPARK_HOME environment variable
   - Add $SPARK_HOME/python to Python path

### Jupyter

```bash
pip3 install jupyter

# Create notebook
jupyter notebook

# Import and use
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Jupyter").getOrCreate()
```

## Next Steps

- Explore [Troubleshooting](troubleshooting.md) if issues arise
- Check [Best Practices](best-practices.md)
- Review [Resources](resources.md) for learning materials
