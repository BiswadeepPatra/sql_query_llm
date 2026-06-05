# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 2 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 66.7% |
| **Average Speedup** | 4.73x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query3 | ❌ FAILED | 20 | 12.28x | 5 |
| query2 | ✅ PASSED | 2 | 0.91x | 4 |
| sql_query_1 | ✅ PASSED | 35000 | 0.98x | 1 |

## Common Issues Detected

- **Redundant CTEs (employee_totals, dept_averages, employee_ranks, dept_info) can be combined** (1 occurrence)
- **Unnecessary CONCAT() and CAST() in join conditions** (1 occurrence)
- **YEAR() function in WHERE clause can be replaced with date range filter** (1 occurrence)
- **CAST() in SELECT and WHERE clauses can be removed when not needed** (1 occurrence)
- **Multiple aggregations scanning the same table can be combined** (1 occurrence)
- **CROSS JOIN used instead of INNER JOIN** (1 occurrence)
- **YEAR and MONTH functions used in WHERE clause, which can prevent index usage** (1 occurrence)
- **CAST function used unnecessarily** (1 occurrence)
- **Non-sargable WHERE clause due to function-wrapped predicates** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by reordering the joins to reduce the number of rows being joined** (1 occurrence)

---
*Generated: 2026-06-05 09:23:45*
