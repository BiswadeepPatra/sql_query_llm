# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 2 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 66.7% |
| **Average Speedup** | 0.99x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ✅ PASSED | 2 | 1.13x | 5 |
| sql_query_1 | ✅ PASSED | 35000 | 0.86x | 1 |
| query3 | ❌ FAILED | 20 | 0.99x | 7 |

## Common Issues Detected

- **CROSS JOIN used instead of INNER JOIN** (1 occurrence)
- **YEAR and MONTH functions used in WHERE clause, which can prevent index usage** (1 occurrence)
- **CAST function used unnecessarily** (1 occurrence)
- **LIKE pattern with leading wildcard, which can prevent index usage** (1 occurrence)
- **Non-sargable predicates due to function-wrapped columns** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by reordering the joins to reduce the number of rows being joined** (1 occurrence)
- **Redundant CTEs (employee_totals, dept_averages, employee_ranks, dept_info) can be combined** (1 occurrence)
- **Unnecessary CONCAT() and CAST() in join conditions** (1 occurrence)
- **YEAR() function in WHERE clause can be replaced with date range filter** (1 occurrence)
- **Redundant joins (joining to same table multiple times)** (1 occurrence)
- **WHERE filters can be pushed down into CTEs** (1 occurrence)
- **Unnecessary CAST() in aggregate functions** (1 occurrence)
- **Unnecessary DISTINCT keyword** (1 occurrence)

---
*Generated: 2026-06-05 07:53:01*
