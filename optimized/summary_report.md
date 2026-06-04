# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 6 |
| **Passed Validation** | ✅ 3 |
| **Failed Validation** | ❌ 3 |
| **Success Rate** | 50.0% |
| **Average Speedup** | 0.77x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ❌ FAILED | 0 | 1.54x | 5 |
| sql_query_1 | ✅ PASSED | 35000 | 0.94x | 3 |
| query2_optimized | ❌ FAILED | N/A | 0.00x | 0 |
| query2_original | ❌ FAILED | 0 | 0.44x | 5 |
| sql_query_1_original | ✅ PASSED | 35000 | 0.88x | 3 |
| sql_query_1_optimized | ✅ PASSED | 35000 | 0.79x | 2 |

## Common Issues Detected

- **Using SELECT * which can retrieve unnecessary columns** (1 occurrence)
- **Using CROSS JOIN which can lead to a large result set** (1 occurrence)
- **Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) which can prevent index usage** (1 occurrence)
- **Using non-sargable WHERE clauses (LIKE with a wildcard at the beginning)** (1 occurrence)
- **Using a subquery in the WHERE clause which can be slow for large tables** (1 occurrence)
- **No explicit column selection in the subquery is not present but the query can still be optimized** (1 occurrence)
- **No indexes are present on join columns** (1 occurrence)
- **No indexes are present on the where clause column** (1 occurrence)
- **Using SELECT * instead of selecting only required columns** (1 occurrence)
- **Using CROSS JOIN instead of INNER JOIN** (1 occurrence)
- **Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST)** (1 occurrence)
- **Using non-sargable WHERE clauses (LIKE with wildcard at the beginning)** (1 occurrence)
- **Using subquery in the WHERE clause** (1 occurrence)
- **No explicit column selection in the original query, but the query only selects specific columns, so this is not an issue in this case** (1 occurrence)
- **No CROSS JOIN or function-wrapped predicates** (1 occurrence)
- **No non-sargable WHERE clauses** (1 occurrence)
- **No explicit column selection in the SELECT clause for the 'sales' table, which could potentially lead to unnecessary data transfer if 'sales' has many columns** (1 occurrence)
- **No indexing or partitioning information available, which could impact query performance** (1 occurrence)

---
*Generated: 2026-06-04 08:45:40*
