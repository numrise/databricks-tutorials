# Getting Started with Databricks

## Step 1: Create Account

Visit https://community.cloud.databricks.com/ and sign up for a free account.

## Step 2: Create a Cluster

1. In the sidebar, click **Clusters**
2. Click **Create Cluster**
3. Configure:
   - Cluster name: Give it a meaningful name
   - Databricks Runtime: Select 14.3 LTS or newer
   - Worker nodes: Start with 2-4 workers
   - Node type: Choose based on workload
4. Click **Create Cluster**

Wait for the cluster to start (5-10 minutes).

## Step 3: Create a Notebook

1. Click **Workspace** → **Create** → **Notebook**
2. Name your notebook
3. Choose **Python** as the language
4. Attach to your cluster

## Step 4: Write Your First Code

```python
# Read data
df = spark.read.csv("/databricks-datasets/iris/iris.csv", header=True, inferSchema=True)

# Display
display(df)

# Run SQL
df.createOrReplaceTempView("iris")
spark.sql("SELECT COUNT(*) FROM iris").show()
```

## Key Databricks Features

### Magic Commands

```python
%python     # Python cell
%sql        # SQL cell
%markdown   # Markdown cell
%sh         # Shell commands
%run        # Run another notebook
```

### Display Function

The `display()` function provides:
- Auto-visualization
- Interactive exploration
- Performance optimization

```python
display(df)
```

### Collaborative Notebooks

- Share notebooks with team members
- Real-time collaboration
- Version history
- Comments and discussions

## Workspace Organization

```
/Workspace/
  /Users/
    /user@example.com/
      /MyNotebooks/
  /Shared/
  /Repos/
```

## Next Steps

- Explore [Workspace & Clusters](workspace.md)
- Learn about [Notebooks](notebooks.md)
- Try running examples from /databricks-datasets/
