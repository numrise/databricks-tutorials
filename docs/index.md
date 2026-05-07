# Databricks Tutorials

A comprehensive learning resource for Apache Spark, Databricks, and Azure Databricks - from beginner to advanced.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Local Spark
```bash
bash scripts/setup-spark.sh
source ~/.bashrc
```

### 3. Verify Installation
```bash
python scripts/test_installation.py
```

## 📚 Learning Paths

### Path 1: Spark Fundamentals
Start here if you're new to Apache Spark:
- [Installation & Setup](spark/01-installation-setup.md)
- [Spark Fundamentals](spark/02-spark-fundamentals.md)
- [DataFrames](spark/04-working-with-dataframes.md)
- [Spark SQL](spark/05-spark-sql-basics.md)

### Path 2: Data Engineering
Build practical data pipelines:
- [RDDs vs DataFrames](spark/03-rdds-vs-dataframes.md)
- [Reading & Writing Data](spark/06-reading-writing-data.md)
- [Performance Tuning](spark/performance-tuning.md)

### Path 3: Databricks Platform
Deploy on managed infrastructure:
- [Databricks Getting Started](databricks/index.md)
- [Workspace & Clusters](databricks/workspace.md)
- [Notebooks](databricks/notebooks.md)

### Path 4: Azure Integration
Use on Microsoft Azure:
- [Azure Databricks Setup](azure-databricks/setup.md)
- [Azure Integration](azure-databricks/integration.md)
- [Cost Optimization](azure-databricks/cost.md)

## 🛠️ Available Resources

### Scripts
- `scripts/word_count.py` - Classic MapReduce pattern
- `scripts/etl_pipeline.py` - ETL pipeline example
- `scripts/data_generator.py` - Generate sample datasets
- `scripts/spark_utils.py` - Common utilities
- `scripts/setup-spark.sh` - Automated Spark installation
- `scripts/test_installation.py` - Verify Spark setup

### Documentation
- [Setup Guide](guides/setup.md) - Installation and configuration
- [Troubleshooting](guides/troubleshooting.md) - Common issues and solutions
- [Learning Resources](guides/resources.md) - Official docs and courses
- [Best Practices](guides/best-practices.md) - Production patterns

## 📖 Full Documentation

Browse the complete documentation using the navigation menu to the left (or top on mobile).

## 🤝 Contributing

We welcome contributions! Feel free to submit issues or pull requests.

## 📝 License

This repository is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

---

**Version**: 1.0 | **Updated**: May 2024 | **Status**: Production Ready
