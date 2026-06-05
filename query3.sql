-- SEVERELY UNOPTIMIZED: Sales Analysis by Employee and Department
-- Purpose: Find high-value sales with employee and department details
-- This query uses multiple performance anti-patterns

SELECT DISTINCT
    UPPER(e.emp_name) as employee_name,
    CAST(e.salary AS DECIMAL(10,2)) as employee_salary,
    UPPER(e.country) as employee_country,
    LOWER(d.dept_name) as department_name,
    d.location as dept_location,
    s.sale_id,
    CAST(s.amount AS DECIMAL(10,2)) as sale_amount,
    s.region,
    s.product
FROM workspace.sql_optimizer_tests.sales s
CROSS JOIN workspace.sql_optimizer_tests.employees e  
CROSS JOIN workspace.sql_optimizer_tests.departments d
WHERE CONCAT(s.emp_id, '') = CONCAT(e.emp_id, '')
  AND CONCAT(e.dept_id, '') = CONCAT(d.dept_id, '')
  AND YEAR(s.sale_date) = 2024
  AND MONTH(s.sale_date) BETWEEN 1 AND 6
  AND UPPER(e.country) = 'USA'
  AND LOWER(d.dept_name) LIKE '%engineering%'
  AND CAST(s.amount AS DECIMAL(10,2)) > (
      -- Correlated subquery: runs for EACH row!
      SELECT AVG(CAST(s2.amount AS DECIMAL(10,2)))
      FROM workspace.sql_optimizer_tests.sales s2
      INNER JOIN workspace.sql_optimizer_tests.employees e2 ON s2.emp_id = e2.emp_id
      WHERE CONCAT(e2.dept_id, '') = CONCAT(e.dept_id, '')
        AND YEAR(s2.sale_date) = 2024
  )
  AND s.sale_id IN (
      -- Additional subquery for filtering
      SELECT sale_id 
      FROM workspace.sql_optimizer_tests.sales
      WHERE YEAR(sale_date) = 2024
        AND MONTH(sale_date) <= 6
  )
ORDER BY 
    CAST(s.amount AS DECIMAL(10,2)) DESC,
    UPPER(e.emp_name);
