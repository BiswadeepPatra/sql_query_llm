# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 2 |
| **Passed Validation** | ✅ 2 |
| **Failed Validation** | ❌ 0 |
| **Success Rate** | 100.0% |
| **Average Speedup** | 0.87x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ✅ PASSED | 2 | 0.79x | 4 |
| sql_query_1 | ✅ PASSED | 35000 | 0.95x | 1 |

## Common Issues Detected

- **CROSS JOIN used instead of INNER JOIN** (1 occurrence)
- **YEAR and MONTH functions used in WHERE clause, which can prevent index usage** (1 occurrence)
- **CAST function used unnecessarily** (1 occurrence)
- **Non-sargable predicates used in WHERE clause, such as UPPER and LOWER functions, and LIKE pattern** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by reordering the joins to reduce the number of rows being joined** (1 occurrence)

---
*Generated: 2026-06-05 07:13:51*
