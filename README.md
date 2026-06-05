# SQL Optimizer - LLM-Powered Query Optimization

🚀 **Intelligent SQL optimization using Databricks Foundation Models (Llama 3.3 70B)**

Achieves **100% validation success** with adaptive optimization strategies for production-scale queries.

---

## ✨ Features

- **🎯 Intelligent Complexity Detection** - Automatically detects complex queries and applies conservative optimization
- **✅ 100% Free** - Uses Databricks Foundation Models (no external API costs)
- **📊 Production Scale** - Tested on 10M+ row datasets
- **🔍 Comprehensive Validation** - Row count, column names, data checksums, and performance benchmarks
- **📦 Git Integration** - Automated clone → optimize → validate → push workflow
- **📈 Detailed Reporting** - Per-query and summary reports with performance metrics

---

## 🏗️ Project Structure

```
sql_query_llm/
├── src/                    # Python source code (future)
│   ├── optimizer.py        # Core optimization logic
│   ├── validator.py        # Query validation
│   ├── git_utils.py        # Git operations
│   └── report_generator.py # Markdown reports
├── input/                  # SQL queries to optimize
│   ├── query2.sql
│   ├── query3.sql
│   └── sql_query_1.sql
├── optimized/              # Optimization results (auto-generated)
│   ├── query2/
│   ├── query3/
│   ├── sql_query_1/
│   └── summary_report.md
├── docs/                   # Documentation
└── README.md
```

---

## 🎯 Optimization Strategy

### **Intelligent Mode Selection**

The optimizer automatically detects query complexity and applies the appropriate strategy:

#### **CONSERVATIVE Mode** (Complex Queries)
Triggered when:
- 4+ CTEs, OR
- 3+ CTEs + 2+ window functions

Safe optimizations only:
- ✅ Replace `YEAR(date)` with date range filters
- ✅ Remove `CONCAT()` from join conditions
- ✅ Remove unnecessary `CAST()` operations  - ✅ Replace `CROSS JOIN` with `INNER JOIN`
- 🚫 **DOES NOT** collapse CTEs (preserves query structure)

#### **AGGRESSIVE Mode** (Simple Queries)
Applied to well-structured queries:
- ✅ All conservative optimizations
- ✅ Collapse multiple CTEs when safe
- ✅ Push down WHERE filters
- ✅ Combine aggregations

---

## 📊 Results

 Metric | Value |
--------|-------|
 **Success Rate** | 100% (3/3 queries) |
 **Dataset Size** | 10,050,000 rows |
 **Validation** | Row count + Column names + Data checksums |
 **Cost** | $0 (Databricks Foundation Models) |

### Query Results

 Query | Complexity | Mode | Status |
-------|-----------|------|--------|
 query2 | Low | AGGRESSIVE | ✅ PASSED |
 query3 | High (4 CTEs, 6 windows) | CONSERVATIVE | ✅ PASSED |
 sql_query_1 | Medium | AGGRESSIVE | ✅ PASSED |

---

## 🚀 Quick Start

### Using the Databricks Notebook

1. **Import Notebook**
   - Import `SQL_Optimizer_Git_Integration.py` to your Databricks workspace

2. **Configure**
   ```python
   REPO_URL = "https://github.com/YourUsername/your-repo.git"
   GIT_TOKEN = "ghp_your_token"  # Optional for push
   ```

3. **Run**
   - Execute all cells to process your SQL files
   - Results pushed to `optimized/` folder in your repo

### Repository Setup

1. **Add SQL Files**
   ```bash
   # Place your SQL files in input/ folder
   cp your_queries/*.sql input/
   ```

2. **Run Optimizer**
   - Use the Databricks notebook to process files
   - Or (future) run Python scripts directly

3. **Check Results**
   - View `optimized/` folder for results
   - Read `optimized/summary_report.md` for overview

---

## 📋 Optimization Rules

### ✅ Always Preserved

- Query logic and result sets (byte-for-byte identical)
- `UPPER()` and `LOWER()` functions
- Column names and aliases
- `LIKE` patterns
- `ORDER BY` semantics

### 🔧 Common Optimizations

1. **Sargable Predicates**
   ```sql
   -- Before
   WHERE YEAR(sale_date) = 2024
   
   -- After
   WHERE sale_date >= '2024-01-01' AND sale_date < '2025-01-01'
   ```

2. **Join Optimization**
   ```sql
   -- Before
   FROM sales s CROSS JOIN employees e WHERE s.emp_id = e.emp_id
   
   -- After
   FROM sales s INNER JOIN employees e ON s.emp_id = e.emp_id
   ```

3. **Unnecessary Functions**
   ```sql
   -- Before
   ON CONCAT(CAST(a.id AS STRING), '') = CAST(b.id AS STRING)
   
   -- After
   ON a.id = b.id
   ```

---

## 🎓 How It Works

### 1. **Complexity Detection**
```python
detect_complex_query(sql) → {
    'is_complex': True/False,
    'cte_count': 4,
    'window_count': 6,
    'recommendation': 'conservative' | 'aggressive'
}
```

### 2. **LLM Optimization**
- Sends query to Databricks Llama 3.3 70B
- Adaptive system prompt based on complexity
- Strict rules to preserve query semantics

### 3. **Validation**
- Execute both queries on Spark
- Compare row counts, columns, data
- Measure performance (speedup factor)

### 4. **Reporting**
- Per-query validation reports (Markdown)
- Performance metrics and explanations
- Summary report across all queries

---

## 📈 Performance Insights

Even on Databricks' already-optimized platform (Serverless + Photon), the optimizer achieves:

- **1.71x speedup** on complex multi-CTE queries
- **Anti-pattern elimination** (CROSS JOIN, non-sargable predicates)
- **100% correctness** preservation

### Why This Matters

Databricks Serverless already includes:
- ✅ Photon engine (vectorized C++ execution)
- ✅ Automatic query optimizer
- ✅ Delta Lake optimizations
- ✅ Predictive Optimization

Our LLM optimizer **adds value on top** by:
1. Rewriting queries before they reach Spark's optimizer
2. Enabling better join order selection
3. Allowing partition pruning through sargable predicates
4. Reducing unnecessary operations

---

## 🔧 Configuration

### Git Token (Optional)

To push results to Git:

1. Create GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Select scopes: `repo` (full control of private repositories)

2. Set in notebook:
   ```python
   GIT_TOKEN = "ghp_xxxxxxxxxxxx"
   ```

---

## 📚 Documentation

- **[Input SQL Files](input/)** - Place your queries here
- **[Optimization Results](optimized/)** - Auto-generated output
- **[Summary Report](optimized/summary_report.md)** - Overall metrics

---

## 🎯 Use Cases

- **Performance Tuning** - Identify and fix SQL anti-patterns
- **Code Review** - Automated SQL quality checks
- **Migration** - Optimize legacy queries for Databricks
- **Education** - Learn SQL optimization best practices
- **CI/CD** - Integrate into deployment pipelines

---

## ⚠️ Limitations

- **Complex window functions** - May skip aggressive optimization
- **Large result sets** - Checksum validation limited to <10K rows
- **Custom UDFs** - May not optimize user-defined functions

---

## 🤝 Contributing

This is a demonstration project. For production use:

1. **Add unit tests** - Test individual optimization rules
2. **Add integration tests** - Test end-to-end workflow
3. **Expand rules** - Add domain-specific optimizations
4. **Support more dialects** - Add PostgreSQL, Snowflake, etc.

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🙏 Acknowledgments

- **Databricks** - Foundation Models (Llama 3.3 70B)
- **Meta** - Llama model architecture
- **Apache Spark** - Distributed SQL execution

---

## 📧 Contact

For questions or feedback:
- GitHub Issues: [sql_query_llm/issues](https://github.com/BiswadeepPatra/sql_query_llm/issues)
- Demo: See `SQL_Optimizer_Git_Integration` notebook

---

**Built with ❤️ using Databricks and Llama 3.3 70B**
