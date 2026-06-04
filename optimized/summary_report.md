# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 3 |
| **Passed Validation** | ✅ 3 |
| **Failed Validation** | ❌ 0 |
| **Success Rate** | 100.0% |
| **Average Speedup** | 1.39x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| sql_query_1 | ✅ PASSED | 350 | 1.96x | 3 |
| sql_query_1_original | ✅ PASSED | 350 | 1.44x | 3 |
| sql_query_1_optimized | ✅ PASSED | 350 | 0.76x | 2 |

## Common Issues Detected

- **No explicit column selection in the original query, but the query only selects specific columns, so this is not an issue** (2 occurrences)
- **No CROSS JOIN or function-wrapped predicates** (2 occurrences)
- **No non-sargable WHERE clauses** (2 occurrences)
- **No explicit column selection in the SELECT clause for the 'sales' table, which could potentially lead to slower performance if the 'sales' table has many columns** (1 occurrence)
- **No indexing information provided, which could impact query performance** (1 occurrence)

---
*Generated: 2026-06-04 07:41:05*
