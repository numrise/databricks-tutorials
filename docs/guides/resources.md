# Resources

Official documentation and learning materials.

## Official Documentation

### Apache Spark
- **Official Site:** https://spark.apache.org
- **PySpark API:** https://spark.apache.org/docs/latest/api/python
- **Documentation:** https://spark.apache.org/documentation.html
- **GitHub:** https://github.com/apache/spark

### Databricks
- **Official Site:** https://www.databricks.com
- **Documentation:** https://docs.databricks.com
- **Best Practices:** https://docs.databricks.com/en/getting-started/index.html
- **Community:** https://community.databricks.com

### Azure Databricks
- **Azure Docs:** https://learn.microsoft.com/en-us/azure/databricks/
- **Training:** https://learn.microsoft.com/en-us/training/paths/perform-data-engineering-with-azure-databricks/
- **Quickstart:** https://learn.microsoft.com/en-us/azure/databricks/getting-started/index

## Learning Materials

### Beginner Tutorials
- Databricks Academy: https://academy.databricks.com
- Udemy Spark courses
- YouTube: DataTalks.Club, James Briggs

### Intermediate Topics
- Delta Lake: https://delta.io/
- MLflow: https://mlflow.org/
- Apache Spark configuration tuning

### Advanced Topics
- Catalyst Optimizer internals
- Tungsten memory management
- Custom data source APIs

## Key Concepts

### RDDs (Resilient Distributed Datasets)
- Low-level API
- Immutable distributed collections
- Use for unstructured data or fine-grained control

### DataFrames
- High-level API
- SQL-like operations
- Use for structured data

### Delta Lake
- ACID transactions
- Time travel
- Schema enforcement

### MLflow
- Model lifecycle management
- Experiment tracking
- Model registry

## Tools and Libraries

### Essential Libraries
```
pyspark          # Spark Python API
pandas           # Data manipulation
numpy            # Numerical computing
scikit-learn     # Machine learning
matplotlib       # Visualization
```

### Installation
```bash
pip install pyspark pandas numpy scikit-learn matplotlib
```

## Community Resources

### Forums
- Stack Overflow (tag: pyspark)
- Databricks Community Forum
- Reddit: r/apachespark, r/databricks

### Events
- Spark Summit (annual conference)
- Databricks events and webinars
- Local meetups and user groups

### Newsletters
- Databricks blog: https://www.databricks.com/blog
- Apache Spark mailing list
- Data Engineering Weekly

## Example Projects

### ETL Pipeline
1. Read from cloud storage
2. Transform and clean data
3. Write to data lake

### Machine Learning
1. Load and prepare data
2. Train model with MLflow
3. Register and deploy

### Real-time Streaming
1. Ingest Kafka/Events Hub data
2. Process with Spark Streaming
3. Write aggregations to Delta

## Best Practices Checklist

- [ ] Use DataFrames over RDDs
- [ ] Enable adaptive query execution
- [ ] Partition data appropriately
- [ ] Use predicate pushdown in joins
- [ ] Cache frequently accessed data
- [ ] Monitor cluster performance
- [ ] Use Delta for ACID guarantees
- [ ] Track experiments with MLflow

## Certification

### Databricks Certified
- Databricks Certified Associate Developer
- Databricks Certified Professional Data Engineer
- Exam practice: https://www.databricks.com/learn/certification

## Next Steps

- Take Databricks Academy course
- Complete a hands-on project
- Join community and ask questions
- Practice with real datasets
