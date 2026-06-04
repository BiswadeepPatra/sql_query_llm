# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 2 |
| **Passed Validation** | ✅ 1 |
| **Failed Validation** | ❌ 1 |
| **Success Rate** | 50.0% |
| **Average Speedup** | 1.37x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ❌ FAILED | 0 | 1.84x | 5 |
| sql_query_1 | ✅ PASSED | 35000 | 0.90x | 3 |

## Common Issues Detected

- **Using SELECT * which can retrieve unnecessary columns** (1 occurrence)
- **Using CROSS JOIN which can lead to a Cartesian product and slow performance** (1 occurrence)
- **Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) which can prevent index usage** (1 occurrence)
- **Using non-sargable WHERE clauses (LIKE with a wildcard at the beginning)** (1 occurrence)
- **Using a subquery in the WHERE clause which can be slow** (1 occurrence)
- **No explicit column selection in the original query, but the query only selects specific columns, so this is not an issue in this case** (1 occurrence)
- **No CROSS JOIN or function-wrapped predicates** (1 occurrence)
- **No non-sargable WHERE clauses** (1 occurrence)

---
*Generated: 2026-06-04 08:40:03*
