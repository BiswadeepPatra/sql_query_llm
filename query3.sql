-- UNOPTIMIZED: Sales Analysis by Employee and Department
-- Purpose: High-value sales with employee/department details
-- Multiple performance anti-patterns for demonstration

SELECT DISTINCT
    UPPER(e.emp_name) as employee_name,
    CAST(e.salary AS DECIMAL(10,2)) as employee_salary,
    UPPER(e.country) as employee_country,
    LOWER(d.dept_name) as department_name,
    s.sale_id,
    CAST(s.amount AS DECIMAL(10,2)) as sale_amount,
    s.region
FROM workspace.sql_optimizer_tests.sales s
CROSS JOIN workspace.sql_optimizer_tests.employees e  
CROSS JOIN workspace.sql_optimizer_tests.departments d
WHERE CONCAT(CAST(s.emp_id AS STRING), '') = CONCAT(CAST(e.emp_id AS STRING), '')
  AND CONCAT(CAST(e.dept_id AS STRING), '') = CONCAT(CAST(d.dept_id AS STRING), '')
  AND YEAR(s.sale_date) = 2024
  AND MONTH(s.sale_date) BETWEEN 1 AND 6
  AND UPPER(e.country) = 'USA'
  AND LOWER(d.dept_name) LIKE '%engineering%'
  AND CAST(s.amount AS DECIMAL(10,2)) > 5000
ORDER BY 
    CAST(s.amount AS DECIMAL(10,2)) DESC;
