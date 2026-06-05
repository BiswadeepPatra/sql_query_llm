# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 2 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 66.7% |
| **Average Speedup** | 0.66x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ✅ PASSED | 2 | 0.86x | 4 |
| sql_query_1 | ✅ PASSED | 35000 | 1.13x | 1 |
| query3 | ❌ FAILED | 0 | 0.00x | 4 |

## Common Issues Detected

- **CROSS JOIN used instead of INNER JOIN** (2 occurrences)
- **YEAR and MONTH functions used in WHERE clause, which can prevent index usage** (1 occurrence)
- **CAST function used unnecessarily** (1 occurrence)
- **Non-sargable predicates due to function-wrapped columns** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by reordering the joins to reduce the number of rows being joined** (1 occurrence)
- **Function-wrapped predicates in WHERE clause (CONCAT, CAST, YEAR, MONTH)** (1 occurrence)
- **Non-sargable WHERE clauses (YEAR, MONTH, UPPER, LOWER, CAST, CONCAT)** (1 occurrence)
- **Unnecessary CAST operations** (1 occurrence)

---
*Generated: 2026-06-05 07:29:38*
