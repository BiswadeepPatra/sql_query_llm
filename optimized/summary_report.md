# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 3 |
| **Failed Validation** | ❌ 0 |
| **Success Rate** | 100.0% |
| **Average Speedup** | 0.89x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ✅ PASSED | 2 | 1.01x | 4 |
| sql_query_1 | ✅ PASSED | 35000 | 0.63x | 1 |
| query3 | ✅ PASSED | 2 | 1.01x | 5 |

## Common Issues Detected

- **CROSS JOIN used instead of INNER JOIN** (2 occurrences)
- **YEAR and MONTH functions used in WHERE clause, which can prevent index usage** (1 occurrence)
- **CAST function used unnecessarily** (1 occurrence)
- **Non-sargable LIKE pattern used in WHERE clause** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by reordering the joins to reduce the number of rows being joined** (1 occurrence)
- **CONCAT() used in join conditions** (1 occurrence)
- **YEAR() and MONTH() functions used in WHERE clause** (1 occurrence)
- **CAST() used unnecessarily in WHERE clause** (1 occurrence)
- **Non-sargable WHERE clause due to function-wrapped predicates** (1 occurrence)

---
*Generated: 2026-06-05 07:31:34*
