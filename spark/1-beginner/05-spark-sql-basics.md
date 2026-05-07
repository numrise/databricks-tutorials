# Spark SQL Basics

## What is Spark SQL?

Spark SQL is a Spark module for structured data processing. It provides:
- SQL query interface for DataFrames
- Optimized performance via Catalyst optimizer
- Support for multiple data formats (CSV, JSON, Parquet, etc.)
- Integration with external databases

## Creating SQL Context

```python
from pyspark.sql import SparkSession

# SparkSession automatically includes SQL context
spark = SparkSession.builder.appName("SQL").getOrCreate()

# Access SQL context
spark.sql("SELECT * FROM table_name")
```

## Creating Temporary Views

```python
# Create temporary view (session-scoped)
df.createOrReplaceTempView("employees")

# Create global temporary view
df.createGlobalTempView("employees_global")

# Create permanent table (requires SQL warehouse)
df.write.mode("overwrite").saveAsTable("employees_table")
```

## SQL Queries

```python
# Basic SELECT
spark.sql("SELECT * FROM employees").show()

# SELECT specific columns
spark.sql("SELECT name, salary FROM employees WHERE salary > 80000").show()

# Aggregation
spark.sql("""
    SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""").show()

# JOIN
spark.sql("""
    SELECT e.name, d.department_name
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
""").show()

# Window functions
spark.sql("""
    SELECT 
        name, 
        salary,
        ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
    FROM employees
""").show()
```

## DataFrame API vs SQL

Both achieve same results:

```python
# DataFrame API
employees.filter(col("salary") > 80000) \
    .select("name", "salary") \
    .show()

# SQL
spark.sql("""
    SELECT name, salary 
    FROM employees 
    WHERE salary > 80000
""").show()
```

## Common SQL Functions

```python
# Aggregation functions
spark.sql("""
    SELECT 
        COUNT(*) as total_rows,
        SUM(salary) as total_salary,
        AVG(salary) as avg_salary,
        MIN(salary) as min_salary,
        MAX(salary) as max_salary
    FROM employees
""").show()

# String functions
spark.sql("""
    SELECT 
        UPPER(name) as name_upper,
        LOWER(name) as name_lower,
        SUBSTR(name, 1, 3) as first_3_chars,
        LENGTH(name) as name_length
    FROM employees
""").show()

# Date functions
spark.sql("""
    SELECT 
        CURRENT_DATE as today,
        DATE_ADD(CURRENT_DATE, 30) as in_30_days,
        YEAR(hire_date) as hire_year
    FROM employees
""").show()

# Conditional functions
spark.sql("""
    SELECT 
        CASE 
            WHEN salary > 100000 THEN 'High'
            WHEN salary > 75000 THEN 'Medium'
            ELSE 'Low'
        END as salary_level
    FROM employees
""").show()
```

## Query Optimization Tips

1. **Use Parquet format** - Columnar, compressed, efficient
2. **Partition data** - Split into logical chunks
3. **Use predicate pushdown** - Filter early
4. **Cache intermediate results** - Reuse expensive computations
5. **Broadcast small tables** - For JOIN operations

## Practice Exercise

```python
# Create sample data
employees = spark.createDataFrame([
    (1, "Alice", "Engineering", 85000, "2020-01-15"),
    (2, "Bob", "Sales", 72000, "2019-03-20"),
    (3, "Charlie", "Engineering", 78000, "2021-06-01"),
    (4, "David", "Management", 95000, "2018-09-10"),
    (5, "Eve", "Sales", 68000, "2022-02-14")
], ["emp_id", "name", "department", "salary", "hire_date"])

employees.createOrReplaceTempView("employees")

# TODO: Write queries to answer:
# 1. Average salary by department
# 2. Employees hired in 2020 or later
# 3. Total salary per department
# 4. Employee with highest salary in each department
```

## Next Steps

- Continue with [Reading & Writing Data](06-reading-writing-data.md)
- Explore [Intermediate Spark](../../2-intermediate/README.md)
