# Setup Instructions

## Prerequisites

- Databricks Workspace (AWS, Azure, or GCP)
- Databricks Serverless Compute (recommended) or Cluster
- GitHub Account (for Git integration)

## Installation

### Option 1: Use the Databricks Notebook (Recommended)

1. **Import Notebook**
   - Download `SQL_Optimizer_Git_Integration.py` from your workspace
   - Import to your Databricks workspace

2. **Configure**
   ```python
   REPO_URL = "https://github.com/YourUsername/your-repo.git"
   GIT_TOKEN = "ghp_your_token"  # Optional
   ```

3. **Run**
   - Execute cells 1-7
   - Results saved to `optimized/` folder

### Option 2: Use Python Modules Directly

1. **Clone Repository**
   ```bash
   git clone https://github.com/BiswadeepPatra/sql_query_llm.git
   cd sql_query_llm
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Use in Your Code**
   ```python
   from src.optimizer import optimize_sql, detect_complex_query
   from src.git_utils import find_sql_files
   
   # Detect complexity
   complexity = detect_complex_query(your_sql_query)
   print(f"Complexity: {complexity['recommendation']}")
   
   # Optimize
   result = optimize_sql(your_sql_query, llm_client)
   print(f"Optimized: {result['optimized_sql']}")
   ```

## GitHub Token Setup

To enable automatic push to GitHub:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scope: `repo` (full control)
4. Copy the token (starts with `ghp_`)
5. Set in notebook: `GIT_TOKEN = "ghp_..."`

## Project Structure

```
sql_query_llm/
├── src/                    # Python source code
│   ├── __init__.py        # Package initialization
│   ├── optimizer.py       # Core optimization logic
│   ├── git_utils.py       # Git operations
│   └── report_generator.py # Report creation
├── input/                  # SQL queries to optimize
├── optimized/              # Results (auto-generated)
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## Usage Examples

### Basic Optimization

```python
import mlflow.deployments

# Initialize LLM client
client = mlflow.deployments.get_deploy_client("databricks")

# Optimize a query
from src.optimizer import optimize_sql

query = """
SELECT * FROM sales 
WHERE YEAR(sale_date) = 2024
"""

result = optimize_sql(query, client)
print(result['optimized_sql'])
```

### Batch Processing

```python
from src.git_utils import find_sql_files
from src.optimizer import optimize_sql
from src.report_generator import save_optimization_results

# Find SQL files
sql_files = find_sql_files("/path/to/repo")

# Process each
for sql_file in sql_files:
    result = optimize_sql(sql_file['content'], client)
    save_optimization_results(sql_file, result, validation, "output/")
```

## Troubleshooting

### Issue: "LLM client not available"
**Solution**: Ensure you're running on Databricks compute with MLflow installed

### Issue: "Git push failed"
**Solution**: Check your GitHub token has `repo` scope permissions

### Issue: "Module not found"
**Solution**: Ensure you're in the repository root and ran `pip install -r requirements.txt`

## Next Steps

- Read the [README](../README.md) for full documentation
- Check [optimization examples](../input/) for sample queries
- View [results](../optimized/) to see optimization reports

---

For questions: GitHub Issues or Databricks Community
