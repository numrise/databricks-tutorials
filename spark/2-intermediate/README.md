# Apache Spark - Intermediate Level

Advanced data processing techniques and optimization strategies.

## Topics

1. [Spark SQL Performance Tuning](01-spark-sql-performance.md)
2. [Window Functions & Advanced Aggregations](02-window-functions.md)
3. [Complex Transformations](03-complex-transformations.md)
4. [Partitioning & Bucketing](04-partitioning-bucketing.md)
5. [Caching & Memory Management](05-caching-memory.md)

## Prerequisites

- Complete all Beginner level tutorials
- Comfortable with Spark SQL and DataFrames
- Basic understanding of distributed computing

## Learning Objectives

- Optimize Spark queries for performance
- Master advanced SQL operations
- Understand partitioning strategies
- Manage memory efficiently
- Process large-scale data effectively

## Quick Reference

### Common Performance Issues

| Problem | Solution |
|---------|----------|
| Slow joins | Broadcast small tables, partition data |
| Out of memory | Increase executor memory, partition data |
| Skewed data | Repartition, salting technique |
| Slow reads | Use Parquet, partition by common filters |

## When to Use Intermediate Techniques

- Working with datasets > 100MB
- Complex multi-step transformations
- Production pipelines requiring optimization
- Performance optimization required
- Need for advanced analytics

## Next Steps

- Continue with specific topics in order
- Apply techniques to real datasets
- Move to Advanced when comfortable
