
    WITH employee_analysis AS (
        SELECT 
            e.emp_id,
            UPPER(e.emp_name) as emp_name,
            e.dept_id,
            UPPER(e.country) as country,
            SUM(s.amount) as total_sales,
            COUNT(*) as num_sales,
            d.dept_name,
            d.location
        FROM workspace.sql_optimizer_tests.sales s
        INNER JOIN workspace.sql_optimizer_tests.employees e ON s.emp_id = e.emp_id
        INNER JOIN workspace.sql_optimizer_tests.departments d ON e.dept_id = d.dept_id
        WHERE s.sale_date >= '2024-01-01' AND s.sale_date < '2025-01-01'
        GROUP BY e.emp_id, e.emp_name, e.dept_id, e.country, d.dept_name, d.location
    )
    SELECT 
        emp_name,
        total_sales,
        num_sales,
        RANK() OVER (PARTITION BY dept_id ORDER BY total_sales DESC) as dept_rank,
        dept_name,
        location,
        AVG(total_sales) OVER (PARTITION BY dept_id) as avg_dept_sale,
        COUNT(*) OVER (PARTITION BY dept_id) as dept_sale_count,
        CASE 
            WHEN total_sales > AVG(total_sales) OVER (PARTITION BY dept_id) * 1.5 THEN 'Top Performer'
            WHEN total_sales > AVG(total_sales) OVER (PARTITION BY dept_id) THEN 'Above Average'
            ELSE 'Below Average'
        END as performance_tier
    FROM employee_analysis
    WHERE UPPER(country) = 'USA'
      AND LOWER(dept_name) LIKE '%engineering%'
      AND total_sales > 1000
    ORDER BY dept_rank, total_sales DESC;
  