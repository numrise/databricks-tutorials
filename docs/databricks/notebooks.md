# Working with Notebooks

## Notebook Basics

Databricks notebooks are interactive documents where you can:
- Write code (Python, SQL, Scala, R)
- Execute commands
- Visualize results
- Add documentation
- Collaborate with team members

## Cell Types

### Code Cells

```python
# Python code
df = spark.read.csv("data.csv", header=True)
display(df)
```

### SQL Cells

```sql
-- SQL cell
SELECT COUNT(*) as total_rows FROM iris
```

### Markdown Cells

```markdown
# My Project Title

This is documentation about my analysis.
```

### Shell Cells

```bash
%sh ls -la /mnt/
```

## Running Notebooks

### Execute Cells

- **Shift + Enter** - Run cell and move to next
- **Ctrl + Enter** - Run cell and stay
- **Ctrl + Shift + Enter** - Run all cells

### Run Entire Notebook

```
Click the "Run All" button in the toolbar
```

## Best Practices

### Organization

- Use markdown headers to organize sections
- One concept per cell
- Add comments explaining logic

### Documentation

```python
# This cell performs data cleaning
# - Remove duplicates
# - Handle missing values
# - Standardize formats

df_cleaned = df.dropDuplicates()
```

### Error Handling

```python
try:
    df = spark.read.csv("data.csv")
except Exception as e:
    print(f"Error reading file: {e}")
```

## Visualization

Use `display()` for automatic visualizations:

```python
display(df)  # Auto-shows table or chart
```

For custom plots, use libraries:

```python
import matplotlib.pyplot as plt
df_pandas = df.toPandas()
plt.plot(df_pandas['x'], df_pandas['y'])
display(plt.gcf())
```

## Sharing Notebooks

1. Click **Share** in top-right
2. Add collaborators
3. Set permission levels:
   - **Can Edit** - Full access
   - **Can Attach To** - Can run, no edit
   - **Can Read** - View only

## Notebook Workflows

Link notebooks together:

```python
# Run another notebook
%run ./my_other_notebook

# Pass variables between notebooks
notebook_params = {"param1": "value1"}
```

## Next Steps

- Explore built-in datasets in /databricks-datasets/
- Try running the example scripts
- Collaborate with team members
