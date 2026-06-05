
    WITH employee_data AS (
        SELECT 
            e.emp_id,
            UPPER(e.emp_name) as emp_name,
            e.dept_id,
            UPPER(e.country) as country,
            SUM(s.amount) as total_sales,
            COUNT(*) as num_sales
        FROM workspace.sql_optimizer_tests.sales s
        INNER JOIN workspace.sql_optimizer_tests.employees e ON s.emp_id = e.emp_id
        WHERE s.sale_date >= '2024-01-01' AND s.sale_date < '2025-01-01'
        GROUP BY e.emp_id, e.emp_name, e.dept_id, e.country
    ),
    department_data AS (
        SELECT 
            e.dept_id,
            AVG(s.amount) as avg_dept_sale,
            COUNT(*) as dept_sale_count
        FROM workspace.sql_optimizer_tests.sales s
        INNER JOIN workspace.sql_optimizer_tests.employees e ON s.emp_id = e.emp_id
        WHERE s.sale_date >= '2024-01-01' AND s.sale_date < '2025-01-01'
        GROUP BY e.dept_id
    ),
    ranked_employees AS (
        SELECT 
            emp_id,
            emp_name,
            dept_id,
            country,
            total_sales,
            num_sales,
            RANK() OVER (PARTITION BY dept_id ORDER BY total_sales DESC) as dept_rank
        FROM employee_data
    )
    SELECT 
        re.emp_name,
        re.total_sales,
        re.num_sales,
        re.dept_rank,
        di.dept_name,
        di.location,
        dd.avg_dept_sale,
        dd.dept_sale_count,
        CASE 
            WHEN re.total_sales > dd.avg_dept_sale * 1.5 THEN 'Top Performer'
            WHEN re.total_sales > dd.avg_dept_sale THEN 'Above Average'
            ELSE 'Below Average'
        END as performance_tier
    FROM ranked_employees re
    INNER JOIN department_data dd ON re.dept_id = dd.dept_id
    INNER JOIN workspace.sql_optimizer_tests.departments di ON re.dept_id = di.dept_id
    WHERE re.country = 'USA'
      AND di.dept_name LIKE '%engineering%'
      AND re.total_sales > 1000
    ORDER BY re.dept_rank, re.total_sales DESC;
  