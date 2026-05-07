# Spark SQL

## What is Spark SQL?

Spark SQL is a Spark module for structured data processing, providing:
- SQL query interface for DataFrames
- Optimized performance via Catalyst optimizer
- Support for multiple data formats
- Integration with external databases

## Creating Temporary Views

```python
# Session-scoped temporary view
df.createOrReplaceTempView("employees")

# Global temporary view
df.createGlobalTempView("employees_global")

# Permanent table
df.write.mode("overwrite").saveAsTable("employees_table")
```

## SQL Queries

```python
# Basic SELECT
spark.sql("SELECT * FROM employees").show()

# SELECT specific columns
spark.sql("""
    SELECT name, salary FROM employees 
    WHERE salary > 80000
""").show()

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

## Common SQL Functions

### Aggregation

```python
spark.sql("""
    SELECT 
        COUNT(*) as total_rows,
        SUM(salary) as total_salary,
        AVG(salary) as avg_salary,
        MIN(salary) as min_salary,
        MAX(salary) as max_salary
    FROM employees
""").show()
```

### String Functions

```python
spark.sql("""
    SELECT 
        UPPER(name) as name_upper,
        SUBSTR(name, 1, 3) as first_3_chars,
        LENGTH(name) as name_length
    FROM employees
""").show()
```

### Date Functions

```python
spark.sql("""
    SELECT 
        CURRENT_DATE as today,
        DATE_ADD(CURRENT_DATE, 30) as in_30_days,
        YEAR(hire_date) as hire_year
    FROM employees
""").show()
```

### Conditional Functions

```python
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

## DataFrame API vs SQL

Both approaches achieve the same results:

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

## Best Practices

1. **Use SQL for analytics** - It's intuitive and well-optimized
2. **Use DataFrame API for complex logic** - Better for programmatic access
3. **Mix both** - Use whichever is clearest
4. **Use predicate pushdown** - Filters are pushed down automatically
5. **Partition data** - For better query performance

## Next Steps

- Learn [Data I/O](06-reading-writing-data.md)
- Explore [Performance Tuning](performance-tuning.md)
