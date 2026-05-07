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

### 2. Install Python

Recommended: Use Python 3.9 or 3.10

```bash
python --version
pip install --upgrade pip
```

### 3. Download Spark

```bash
cd ~/Downloads
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xzf spark-3.5.0-bin-hadoop3.tgz
mv spark-3.5.0-bin-hadoop3 ~/spark-3.5.0
```

### 4. Configure Environment Variables

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export SPARK_HOME=~/spark-3.5.0
export PATH=$PATH:$SPARK_HOME/bin
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

Then reload:
```bash
source ~/.bashrc
```

### 5. Install PySpark

```bash
pip install pyspark==3.5.0
```

### 6. Verify Installation

```bash
spark-submit --version
java -version
python --version
pyspark
```

In the PySpark shell:
```python
spark.version
spark.range(5).show()
```

## Using the Setup Script

We provide an automated setup script:

```bash
bash scripts/setup-spark.sh
```

Then verify:
```bash
python scripts/test_installation.py
```

## Troubleshooting

### "spark-submit: command not found"
```bash
export PATH=$PATH:~/spark-3.5.0/bin
```

### "JAVA_HOME not found"
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

### Port Already in Use
The Spark UI uses port 4040. If occupied:
```bash
lsof -i :4040
kill -9 <PID>
```

## Docker Alternative

```bash
docker pull bitnami/spark:latest
docker run -it bitnami/spark:latest pyspark
```

## Next Steps

- Proceed to [Spark Fundamentals](02-spark-fundamentals.md)
- Check out [example scripts](../../scripts/)
