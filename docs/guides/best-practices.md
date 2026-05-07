# Best Practices

Production-ready patterns and optimization techniques.

## Code Organization

### Structure Your Projects

```
my_project/
  ├── notebooks/          # Interactive development
  ├── src/
  │   ├── etl/           # Extract, transform, load
  │   ├── transformations/
  │   └── utils/
  ├── tests/             # Unit tests
  ├── config/            # Configuration files
  ├── requirements.txt   # Dependencies
  └── README.md          # Documentation
```

### Modular Code

```python
# Create reusable modules
# utils/transformations.py

def clean_data(df):
    """Remove nulls and duplicates"""
    return df.dropna().dropDuplicates()

def normalize_columns(df):
    """Standardize column names"""
    return df.toDF(*[col.lower().replace(' ', '_') for col in df.columns])

# notebooks/pipeline.py
from utils.transformations import clean_data, normalize_columns

df = spark.read.csv("data.csv")
df = clean_data(df)
df = normalize_columns(df)
```

## Performance Optimization

### 1. Query Optimization

```python
# GOOD: Let Spark optimize
df1.join(df2, "id", "inner") \
   .filter(df.amount > 1000) \
   .groupBy("category").count()

# BAD: Inefficient operations
df1.collect()  # Brings entire DF to driver
df1.show(10000)  # Unnecessary materialization
```

### 2. Partitioning

```python
# Partition data by frequently filtered column
df.write \
    .partitionBy("date") \
    .format("delta") \
    .mode("overwrite") \
    .save("path")

# Read only relevant partitions
df = spark.read.delta("path").filter("date >= '2024-01-01'")
```

### 3. Caching Strategy

```python
# Cache if reused multiple times
df = spark.read.parquet("large_file.parquet")
df.cache()

# Use cached data for multiple operations
result1 = df.filter("amount > 1000").count()
result2 = df.filter("category == 'A'").count()

# Unpersist when done
df.unpersist()
```

### 4. Broadcast Small DataFrames

```python
# Broadcast dimension table for efficient joins
from pyspark.sql.functions import broadcast

large_df = spark.read.parquet("large_data.parquet")
small_df = spark.read.parquet("lookup.parquet")

result = large_df.join(broadcast(small_df), "id", "inner")
```

## Data Quality

### Schema Validation

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("amount", IntegerType(), True)
])

df = spark.read.schema(schema).csv("data.csv")
```

### Data Validation

```python
# Check for nulls
null_counts = df.select([count(when(col(c).isNull(), 1)).alias(c) for c in df.columns])

# Validate ranges
df.filter("amount < 0").count()  # Should be 0

# Check uniqueness
df.select("id").distinct().count() == df.count()  # Should be True
```

## Error Handling

### Try-Except Patterns

```python
from datetime import datetime

def safe_read_data(path):
    """Read data with error handling"""
    try:
        df = spark.read.parquet(path)
        print(f"Successfully read {df.count()} rows")
        return df
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Usage
df = safe_read_data("path/to/data")
if df is not None:
    df.show()
```

### Data Pipeline Resilience

```python
def run_with_retry(func, max_retries=3, backoff_factor=2):
    """Run function with exponential backoff"""
    from time import sleep
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                print(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
                sleep(wait_time)
            else:
                raise

# Usage
def process_data():
    df = spark.read.parquet("data.parquet")
    return df.filter("amount > 0")

result = run_with_retry(process_data)
```

## Testing

### Unit Tests

```python
# test_transformations.py
import pytest
from pyspark.sql import SparkSession
from src.transformations import clean_data

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.appName("test").getOrCreate()

def test_clean_data(spark):
    # Arrange
    data = [(1, "Alice"), (None, "Bob"), (1, "Alice")]
    df = spark.createDataFrame(data, ["id", "name"])
    
    # Act
    result = clean_data(df)
    
    # Assert
    assert result.count() == 1
    assert result.collect()[0]["name"] == "Alice"
```

## Security

### Credential Management

```python
# NEVER hardcode credentials
# WRONG:
spark.conf.set("fs.azure.account.key.account.dfs.core.windows.net", "key123")

# RIGHT: Use secrets
token = dbutils.secrets.get(scope="keyvault-scope", key="storage-key")
spark.conf.set("fs.azure.account.key.account.dfs.core.windows.net", token)

# Or use service principals/managed identities
```

### Access Control

```python
# Use row-level security in Delta
spark.sql("""
    CREATE TABLE sensitive_data (id INT, value STRING)
    USING DELTA
    WITH ROW ACCESS CONTROL
""")

# Grant permissions
spark.sql("GRANT SELECT ON TABLE sensitive_data TO user@example.com")
```

## Monitoring & Logging

### Custom Logging

```python
import logging

logger = logging.getLogger(__name__)

def process_batch(batch_id):
    logger.info(f"Processing batch {batch_id}")
    try:
        # Processing logic
        logger.info(f"Batch {batch_id} completed successfully")
    except Exception as e:
        logger.error(f"Batch {batch_id} failed: {e}", exc_info=True)
```

### Performance Monitoring

```python
import time

start_time = time.time()

# Your code
df = spark.read.parquet("large_file.parquet")
result = df.filter("amount > 1000").count()

elapsed = time.time() - start_time
print(f"Query took {elapsed:.2f} seconds")
```

## Deployment Checklist

- [ ] Code passes unit tests
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Credentials use secret management
- [ ] Performance validated
- [ ] Data validation checks included
- [ ] Documentation complete
- [ ] Monitoring/alerting setup
- [ ] Rollback plan documented

## Next Steps

- Implement one best practice per sprint
- Review and refactor old code
- Share practices with team
- Stay updated with Spark releases
