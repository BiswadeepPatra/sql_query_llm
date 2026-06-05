# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 2 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 66.7% |
| **Average Speedup** | 1.87x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ✅ PASSED | 124 | 3.83x | 4 |
| query3 | ❌ FAILED | 20 | 1.17x | 5 |
| sql_query_1 | ✅ PASSED | 7035000 | 0.62x | 1 |

## Common Issues Detected

- **CROSS JOIN is used instead of INNER JOIN** (1 occurrence)
- **YEAR and MONTH functions are used in the WHERE clause, which can prevent index usage** (1 occurrence)
- **CAST is used unnecessarily** (1 occurrence)
- **LIKE pattern is used with a function-wrapped column, which can prevent index usage** (1 occurrence)
- **Redundant CTEs (employee_totals, dept_averages, employee_ranks, dept_info) can be combined** (1 occurrence)
- **Unnecessary CONCAT() and CAST() in join conditions** (1 occurrence)
- **Unnecessary CAST() in aggregate functions** (1 occurrence)
- **Non-sargable WHERE clause (YEAR(s.sale_date) = 2024) can be replaced with date range filter** (1 occurrence)
- **Unnecessary DISTINCT keyword in SELECT statement** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by pushing down the filter on salary into a subquery or CTE to reduce the number of rows being joined** (1 occurrence)

---
*Generated: 2026-06-05 11:17:19*
