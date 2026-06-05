# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 12 |
| **Passed Validation** | ✅ 3 |
| **Failed Validation** | ❌ 9 |
| **Success Rate** | 25.0% |
| **Average Speedup** | 0.26x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| sql_query_1 | ❌ FAILED | N/A | 0.00x | 0 |
| query2 | ❌ FAILED | 0 | 0.00x | 5 |
| sql_query_1_original_optimized | ✅ PASSED | 35000 | 0.89x | 2 |
| sql_query_1_original_original | ❌ FAILED | N/A | 0.00x | 0 |
| sql_query_1_optimized_original | ✅ PASSED | 35000 | 0.81x | 3 |
| sql_query_1_optimized_optimized | ✅ PASSED | 35000 | 0.78x | 2 |
| query2_original | ❌ FAILED | 0 | 0.67x | 5 |
| query2_optimized | ❌ FAILED | N/A | 0.00x | 0 |
| query2_original_optimized | ❌ FAILED | N/A | 0.00x | 0 |
| query2_original_original | ❌ FAILED | 0 | 0.00x | 5 |
| sql_query_1_optimized | ❌ FAILED | 0 | 0.00x | 2 |
| sql_query_1_original | ❌ FAILED | N/A | 0.00x | 0 |

## Common Issues Detected

- **Using CROSS JOIN instead of INNER JOIN** (3 occurrences)
- **Using SELECT * instead of selecting specific columns** (2 occurrences)
- **Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST)** (2 occurrences)
- **Using non-sargable WHERE clauses (LIKE with wildcard at the beginning)** (2 occurrences)
- **SELECT statement is selecting all columns from the joined tables, but only a subset of columns are used** (2 occurrences)
- **No indexing is specified, which could improve join and filter performance** (2 occurrences)
- **Using subquery in the WHERE clause with IN operator** (1 occurrence)
- **SELECT statement is selecting specific columns but could be improved by only selecting necessary columns from the sales table** (1 occurrence)
- **No indexes are specified on the join columns (e.dept_id, d.dept_id, e.emp_id, s.emp_id) which could improve join performance** (1 occurrence)
- **No indexes are specified on the column used in the WHERE clause (e.salary) which could improve filter performance** (1 occurrence)
- **Using non-sargable WHERE clauses (LIKE with a wildcard at the beginning)** (1 occurrence)
- **Using a subquery in the WHERE clause instead of a JOIN** (1 occurrence)
- **Using SELECT * instead of selecting only required columns** (1 occurrence)
- **Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) which can prevent index usage** (1 occurrence)
- **Using subquery in the WHERE clause which can be slow for large datasets** (1 occurrence)
- **No indexes on join columns and where clause column** (1 occurrence)
- **Potential full table scan due to lack of indexes** (1 occurrence)

---
*Generated: 2026-06-05 05:55:34*
