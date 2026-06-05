
    WITH employee_analysis AS (
        SELECT 
            e.emp_id,
            UPPER(e.emp_name) as emp_name,
            e.dept_id,
            UPPER(e.country) as country,
            SUM(s.amount) as total_sales,
            COUNT(*) as num_sales,
            AVG(s.amount) OVER (PARTITION BY e.dept_id) as avg_dept_sale,
            COUNT(*) OVER (PARTITION BY e.dept_id) as dept_sale_count,
            RANK() OVER (PARTITION BY e.dept_id ORDER BY SUM(s.amount) DESC) as dept_rank
        FROM workspace.sql_optimizer_tests.sales s
        INNER JOIN workspace.sql_optimizer_tests.employees e ON s.emp_id = e.emp_id
        WHERE s.sale_date >= '2024-01-01' AND s.sale_date < '2025-01-01'
        GROUP BY e.emp_id, e.emp_name, e.dept_id, e.country
    )
    SELECT DISTINCT
        ea.emp_name,
        ea.total_sales,
        ea.num_sales,
        ea.dept_rank,
        di.dept_name,
        di.location,
        ea.avg_dept_sale,
        ea.dept_sale_count,
        CASE 
            WHEN ea.total_sales > ea.avg_dept_sale * 1.5 THEN 'Top Performer'
            WHEN ea.total_sales > ea.avg_dept_sale THEN 'Above Average'
            ELSE 'Below Average'
        END as performance_tier
    FROM employee_analysis ea
    INNER JOIN (
        SELECT 
            dept_id,
            LOWER(dept_name) as dept_name,
            location
        FROM workspace.sql_optimizer_tests.departments
    ) di ON ea.dept_id = di.dept_id
    WHERE UPPER(ea.country) = 'USA'
      AND LOWER(di.dept_name) LIKE '%engineering%'
      AND ea.total_sales > 1000
    ORDER BY ea.dept_rank, ea.total_sales DESC;
  