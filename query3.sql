-- SEVERELY UNOPTIMIZED: Employee Performance Analysis with Sales Aggregates
-- Purpose: Calculate employee sales metrics by department and region
-- This query intentionally uses WORST performance anti-patterns for demonstration

SELECT DISTINCT *
FROM (
    -- Subquery 1: Get all employee-sale-dept combinations using CROSS JOIN
    SELECT 
        UPPER(e.emp_name) as employee_name,
        YEAR(e.hire_date) as hire_year,
        MONTH(e.hire_date) as hire_month,
        UPPER(e.country) as country,
        LOWER(d.dept_name) as department,
        CAST(e.salary AS DECIMAL(10,2)) as salary,
        s.sale_id,
        YEAR(s.sale_date) as sale_year,
        MONTH(s.sale_date) as sale_month,
        CAST(s.amount AS DECIMAL(10,2)) as sale_amount,
        s.region
    FROM workspace.sql_optimizer_tests.employees e
    CROSS JOIN workspace.sql_optimizer_tests.sales s
    CROSS JOIN workspace.sql_optimizer_tests.departments d
    WHERE CONCAT(e.emp_id, '') = CONCAT(s.emp_id, '')
      AND CONCAT(e.dept_id, '') = CONCAT(d.dept_id, '')
      AND YEAR(s.sale_date) = 2024
      AND MONTH(s.sale_date) >= 1
) base
WHERE base.sale_id IN (
    -- Subquery 2: Find sales above department average (inefficient)
    SELECT s2.sale_id
    FROM workspace.sql_optimizer_tests.sales s2
    CROSS JOIN workspace.sql_optimizer_tests.employees e2
    WHERE CONCAT(s2.emp_id, '') = CONCAT(e2.emp_id, '')
      AND CAST(s2.amount AS DECIMAL(10,2)) > (
          -- Subquery 3: Calculate dept average (runs for each row!)
          SELECT AVG(CAST(s3.amount AS DECIMAL(10,2)))
          FROM workspace.sql_optimizer_tests.sales s3
          INNER JOIN workspace.sql_optimizer_tests.employees e3 ON s3.emp_id = e3.emp_id
          WHERE LOWER(CONCAT(e3.dept_id, '')) = LOWER(CONCAT(e2.dept_id, ''))
            AND YEAR(s3.sale_date) = YEAR(s2.sale_date)
      )
)
  AND UPPER(base.country) LIKE '%USA%'
  AND LOWER(base.department) LIKE '%engineering%'
  AND CAST(base.salary AS DECIMAL(10,2)) > 50000
ORDER BY 
    YEAR(base.hire_year) DESC,
    MONTH(base.hire_month) DESC,
    base.sale_amount DESC;
