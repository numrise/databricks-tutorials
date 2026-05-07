# Databricks Tutorials

Comprehensive tutorials and practical examples for Apache Spark, Databricks, and Azure Databricks.

## Quick Links

- **📚 Full Documentation:** See [docs/](docs/) for complete tutorials
- **🚀 Getting Started:** [Setup Guide](docs/guides/setup.md)
- **⚡ Apache Spark:** [Spark Tutorials](docs/spark/)
- **🔷 Databricks:** [Databricks Guides](docs/databricks/)
- **☁️ Azure:** [Azure Databricks](docs/azure-databricks/)
- **📖 Guides:** [Setup, Troubleshooting, Resources](docs/guides/)

## What's Included

- **Spark Tutorials** - From installation to optimization
- **Databricks Guides** - Workspace setup and notebooks
- **Azure Integration** - Setup and cost optimization
- **Production Scripts** - Ready-to-use Python examples
- **Best Practices** - Patterns for production environments

## Learning Paths

1. **Beginner:** Start with [Spark Installation](docs/spark/01-installation-setup.md)
2. **Intermediate:** Learn [Spark SQL](docs/spark/05-spark-sql-basics.md) and [DataFrames](docs/spark/04-working-with-dataframes.md)
3. **Advanced:** Explore [Performance Tuning](docs/spark/performance-tuning.md)
4. **Cloud:** Set up [Databricks](docs/databricks/setup.md) or [Azure Databricks](docs/azure-databricks/setup.md)

## Usage

View documentation locally:

```bash
pip install mkdocs mkdocs-readthedocs-theme
mkdocs serve
# Open http://localhost:8000
```

## Repository Structure

```
databricks-tutorials/
├── docs/                    # MkDocs source
│   ├── index.md
│   ├── spark/              # Spark tutorials
│   ├── databricks/         # Databricks guides
│   ├── azure-databricks/   # Azure Databricks
│   └── guides/             # Cross-platform guides
├── scripts/                # Python examples
├── mkdocs.yml             # Site configuration
└── requirements.txt       # Python dependencies
```

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Try the word count example:

```bash
python scripts/word_count.py
```

3. Run the full ETL pipeline:

```bash
python scripts/etl_pipeline.py
```

## Resources

- [Apache Spark Documentation](https://spark.apache.org/documentation.html)
- [Databricks Documentation](https://docs.databricks.com)
- [Azure Databricks Training](https://learn.microsoft.com/en-us/azure/databricks/)
- [Delta Lake](https://delta.io/)

## Contributing

Feel free to submit issues or pull requests to improve these tutorials.

## License

This repository is provided as-is for educational purposes.
