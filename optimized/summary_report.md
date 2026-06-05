# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 2 |
| **Passed Validation** | ✅ 1 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 50.0% |
| **Average Speedup** | 0.89x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ❌ FAILED | 2 | 0.92x | 3 |
| sql_query_1 | ✅ PASSED | 35000 | 0.85x | 1 |

## Common Issues Detected

- **CROSS JOIN used instead of INNER JOIN** (1 occurrence)
- **Function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) in WHERE clause** (1 occurrence)
- **Non-sargable WHERE clauses (YEAR, MONTH, UPPER, LOWER, CAST, LIKE with wildcard at the beginning)** (1 occurrence)
- **No significant performance issues found, but the query can be slightly optimized by reordering the joins to reduce the number of rows being joined** (1 occurrence)

---
*Generated: 2026-06-05 07:11:03*
