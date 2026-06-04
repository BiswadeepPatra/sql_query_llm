# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 7 |
| **Passed Validation** | ✅ 6 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 85.7% |
| **Average Speedup** | 0.79x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| sql_query_1 | ❌ FAILED | N/A | 0.00x | 0 |
| sql_query_1_optimized_original | ✅ PASSED | 350 | 0.96x | 2 |
| sql_query_1_optimized_optimized | ✅ PASSED | 350 | 0.92x | 2 |
| sql_query_1_original_optimized | ✅ PASSED | 350 | 0.90x | 2 |
| sql_query_1_original_original | ✅ PASSED | 350 | 0.82x | 3 |
| sql_query_1_original | ✅ PASSED | 350 | 1.10x | 3 |
| sql_query_1_optimized | ✅ PASSED | 350 | 0.85x | 2 |

## Common Issues Detected

- **No explicit column selection in the SELECT clause for the 'sales' table, potentially retrieving unnecessary data** (2 occurrences)
- **No explicit column selection in the SELECT clause for the 'sales' table, which could potentially lead to unnecessary data transfer if 'sales' has many columns** (2 occurrences)
- **No CROSS JOIN or function-wrapped predicates** (2 occurrences)
- **No non-sargable WHERE clauses** (2 occurrences)
- **No indexing information available, potentially leading to slower join and filter operations** (1 occurrence)
- **No indexing information available, which could impact join and filter performance** (1 occurrence)
- **No indexes are explicitly mentioned, which could lead to slower join and filter operations** (1 occurrence)
- **No explicit column selection in the original query, but the query only selects specific columns, so this is not an issue in this case** (1 occurrence)
- **No explicit column selection in the original query, but it's already selecting specific columns, so no issue here** (1 occurrence)
- **No indexes on join columns (e.dept_id, d.dept_id, e.emp_id, s.emp_id) or filter column (e.salary), potentially leading to slower join and filter operations** (1 occurrence)

---
*Generated: 2026-06-04 07:44:33*
