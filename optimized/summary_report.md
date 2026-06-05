# SQL Optimization Summary Report

## Overview

| Metric | Value |
|--------|-------|
| **Total SQL Files** | 2 |
| **Passed Validation** | ✅ 0 |
| **Failed Validation** | ❌ 2 |
| **Success Rate** | 0.0% |
| **Average Speedup** | 0.00x |

## Detailed Results

| SQL File | Status | Rows | Speedup | Issues Fixed |
|----------|--------|------|---------|---------------|
| query2 | ❌ FAILED | 0 | 0.00x | 5 |
| sql_query_1 | ❌ FAILED | N/A | 0.00x | 0 |

## Common Issues Detected

- **Using SELECT * instead of selecting specific columns** (1 occurrence)
- **Using CROSS JOIN instead of INNER JOIN** (1 occurrence)
- **Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST)** (1 occurrence)
- **Using non-sargable WHERE clauses (LIKE with wildcard at the beginning)** (1 occurrence)
- **Using subquery in the WHERE clause with IN operator** (1 occurrence)

---
*Generated: 2026-06-05 07:02:43*
