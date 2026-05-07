# Troubleshooting

Common issues and solutions.

## PySpark Installation Issues

### Issue: "java.lang.ClassNotFoundException"

**Cause:** Java not installed or JAVA_HOME not set.

**Solution:**
```bash
# Verify Java
java -version

# Set JAVA_HOME
export JAVA_HOME=$(which java)

# Or on macOS
export JAVA_HOME=$(/usr/libexec/java_home)
```

### Issue: "SPARK_HOME environment variable is not set"

**Solution:**
```bash
# Set temporarily
export SPARK_HOME=~/spark

# Or permanently in ~/.bashrc or ~/.zshrc
echo 'export SPARK_HOME=~/spark' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "ModuleNotFoundError: No module named 'pyspark'"

**Solution:**
```bash
# Install PySpark
pip install pyspark

# Or upgrade
pip install --upgrade pyspark
```

## Cluster Connection Issues

### Issue: Cannot connect to Databricks cluster

**Cause:** Missing or invalid personal access token.

**Solution:**
1. Generate token in Databricks workspace
   - Settings → User Settings → Access Tokens
2. Copy full token
3. Configure in notebook or IDE

### Issue: Cluster won't start

**Cause:** Insufficient quota or resource limits.

**Solution:**
1. Check Azure/AWS quota
2. Reduce cluster size
3. Choose different region/availability zone
4. Contact cloud provider support

## Performance Issues

### Issue: Spark job runs slowly

**Common causes:**
- Small cluster size
- Inefficient queries
- Skewed data distribution
- Network bottlenecks

**Solutions:**
```python
# 1. Check execution plan
df.explain()

# 2. Increase parallelism
df = df.repartition(100)

# 3. Use cache for reused data
df.cache()

# 4. Use SQL for optimization
spark.sql("SELECT * FROM data WHERE id > 100").explain()
```

### Issue: Out of memory errors

**Solution:**
```python
# 1. Reduce data size
df = df.limit(10000)

# 2. Increase executor memory in cluster config
# spark.executor.memory = 4g

# 3. Use Spark built-in optimization
spark.conf.set("spark.sql.adaptive.enabled", "true")

# 4. Stream large datasets instead of loading all
df = spark.read.parquet("data/").limit(1000)
```

## Data Access Issues

### Issue: Cannot read from cloud storage

**Cause:** Missing credentials or permissions.

**Azure Storage:**
```python
# Verify credentials
spark.conf.set(
    f"fs.azure.account.key.{account}.dfs.core.windows.net",
    key
)
```

**AWS S3:**
```python
spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
```

### Issue: Delta Lake transaction conflicts

**Solution:**
```python
# Use isolation level
df.write.format("delta").mode("overwrite") \
    .option("txnVersion", "0") \
    .save("path")

# Or retry with backoff
from time import sleep
for i in range(3):
    try:
        df.write.format("delta").mode("overwrite").save("path")
        break
    except Exception as e:
        if i < 2:
            sleep(2 ** i)  # Exponential backoff
```

## Notebook Issues

### Issue: Notebook won't attach to cluster

**Solution:**
1. Check cluster is running
2. Verify you have attach permissions
3. Restart cluster
4. Try different cluster

### Issue: %run command fails

**Cause:** Notebook path incorrect or notebook doesn't exist.

**Solution:**
```python
# Correct path format
%run ./path/to/notebook

# Test path exists
%sh ls -la /Workspace/Users/user@example.com/path/to/
```

## SQL-Related Issues

### Issue: Table not found in SQL

**Solution:**
```python
# Create temporary view
df.createOrReplaceTempView("mytable")

# Or register in catalog
df.write.format("delta").mode("overwrite").saveAsTable("mytable")
```

### Issue: Slow SQL queries

**Solution:**
```python
# Enable adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Use proper joins
df1.join(df2, "id", "inner")

# Add explain to debug
spark.sql("SELECT * FROM table WHERE col > 100").explain()
```

## Debugging Tips

1. **Enable verbose logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Check Spark UI:**
   - Go to cluster's Spark UI
   - Monitor tasks and stages
   - Check driver/executor logs

3. **Use dbutils for logging:**
```python
dbutils.notebook.run("debug_notebook", 300, {"param": "value"})
```

4. **Test in isolation:**
```python
# Create minimal reproducible example
df = spark.createDataFrame([(1, "test")], ["id", "name"])
df.show()
```

## Getting Help

- Check [Resources](resources.md) for official documentation
- Review [Best Practices](best-practices.md)
- Search Databricks community forum
- Contact your cloud provider support
