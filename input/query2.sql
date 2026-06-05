-- Sales Performance Analysis with Anti-Patterns
-- Purpose: Analyze high-value sales by employee and department

SELECT 
    s.sale_id,
    s.emp_id,
    s.sale_date,
    s.amount,
    e.emp_name,
    e.country,
    d.dept_name
FROM workspace.sql_optimizer_tests.sales s
CROSS JOIN workspace.sql_optimizer_tests.employees e
CROSS JOIN workspace.sql_optimizer_tests.departments d
WHERE s.emp_id = e.emp_id
  AND e.dept_id = d.dept_id
  AND YEAR(s.sale_date) = 2024
  AND MONTH(s.sale_date) <= 6
  AND UPPER(e.country) = 'USA'
  AND CAST(s.amount AS DECIMAL(10,2)) > 5000
  AND LOWER(d.dept_name) LIKE '%engineering%'
ORDER BY s.sale_date DESC, s.amount DESC;
