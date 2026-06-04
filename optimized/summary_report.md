# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 2 |
| **Passed Validation** | ✅ 1 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 50.0% |
| **Average Speedup** | 0.55x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ❌ FAILED | 0 | 0.00x | 5 |
| sql_query_1 | ✅ PASSED | 350 | 1.11x | 3 |

## Common Issues Detected

- **Using SELECT * instead of selecting only necessary columns** (1 occurrence)
- **Using CROSS JOIN instead of INNER JOIN** (1 occurrence)
- **Using function-wrapped predicates (YEAR, UPPER, LOWER, CAST, SUBSTRING, CHARINDEX, LEN)** (1 occurrence)
- **Using non-sargable WHERE clauses (SUBSTRING, CHARINDEX, LEN)** (1 occurrence)
- **Using subquery in the WHERE clause without optimization** (1 occurrence)
- **No explicit column selection in the original query, but the query only selects specific columns, so this is not an issue** (1 occurrence)
- **No CROSS JOIN or function-wrapped predicates** (1 occurrence)
- **No non-sargable WHERE clauses** (1 occurrence)

---
*Generated: 2026-06-04 08:29:39*
