# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 2 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 66.7% |
| **Average Speedup** | 5.00x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| sql_query_1 | ✅ PASSED | 7035000 | 14.33x | 1 |
| query3 | ❌ FAILED | 0 | 0.00x | 5 |
| query2 | ✅ PASSED | 124 | 0.67x | 4 |

## Common Issues Detected

- **No major performance issues found, but the query can be slightly optimized by pushing down the filter on salary into a subquery or CTE to reduce the number of rows being joined** (1 occurrence)
- **Redundant CTEs (employee_totals, dept_averages, employee_ranks, dept_info) can be combined** (1 occurrence)
- **Unnecessary CAST() operations** (1 occurrence)
- **Unnecessary CONCAT() operations in join conditions** (1 occurrence)
- **YEAR() function in WHERE clause can be replaced with date range filter** (1 occurrence)
- **Multiple aggregations scanning the same table can be combined** (1 occurrence)
- **CROSS JOIN used instead of INNER JOIN** (1 occurrence)
- **YEAR and MONTH functions used in WHERE clause, which can prevent index usage** (1 occurrence)
- **CAST function used unnecessarily** (1 occurrence)
- **Non-sargable WHERE clause due to function-wrapped predicates** (1 occurrence)

---
*Generated: 2026-06-05 10:34:02*
