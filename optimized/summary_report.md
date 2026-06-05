# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 3 |
| **Failed Validation** | ❌ 0 |
| **Success Rate** | 100.0% |
| **Average Speedup** | 0.88x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ✅ PASSED | 124 | 0.96x | 4 |
| query3 | ✅ PASSED | 20 | 0.87x | 5 |
| sql_query_1 | ✅ PASSED | 7035000 | 0.83x | 1 |

## Common Issues Detected

- **CROSS JOIN used instead of INNER JOIN** (1 occurrence)
- **YEAR and MONTH functions used in WHERE clause, making it non-sargable** (1 occurrence)
- **CAST function used unnecessarily** (1 occurrence)
- **Non-sargable WHERE clause due to function-wrapped predicates** (1 occurrence)
- **Using YEAR() function in WHERE clause, which can prevent index usage** (1 occurrence)
- **Using CONCAT() in join conditions, which can prevent index usage** (1 occurrence)
- **Using CAST() in WHERE clause, which can prevent index usage** (1 occurrence)
- **Using CROSS JOIN is not present but INNER JOIN is used with CONCAT() which can be optimized** (1 occurrence)
- **Using SELECT DISTINCT, which can be slow for large datasets** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by pushing down the WHERE filter into a subquery or CTE to reduce the number of rows being joined** (1 occurrence)

---
*Generated: 2026-06-05 11:35:19*
