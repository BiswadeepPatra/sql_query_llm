# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 2 |
| **Passed Validation** | ✅ 1 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 50.0% |
| **Average Speedup** | 0.34x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ❌ FAILED | 0 | 0.00x | 5 |
| sql_query_1 | ✅ PASSED | 35000 | 0.68x | 2 |

## Common Issues Detected

- **Using SELECT * instead of selecting only necessary columns** (1 occurrence)
- **Using CROSS JOIN instead of INNER JOIN** (1 occurrence)
- **Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) which can prevent index usage** (1 occurrence)
- **Using non-sargable WHERE clauses (LIKE with a wildcard at the beginning)** (1 occurrence)
- **Using a subquery in the WHERE clause which can be slow for large datasets** (1 occurrence)
- **No explicit column selection in the subquery is not an issue here, but selecting only required columns is a good practice** (1 occurrence)
- **No performance issues like CROSS JOIN, function-wrapped predicates, or non-sargable WHERE clauses are found** (1 occurrence)

---
*Generated: 2026-06-04 08:44:06*
