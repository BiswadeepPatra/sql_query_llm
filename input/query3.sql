-- SEVERELY UNOPTIMIZED: Employee Sales Analysis with Multiple CTEs
-- Purpose: Analyze employee performance with department rankings
-- Uses multiple redundant CTEs and aggregations

-- CTE 1: Calculate employee total sales
WITH employee_totals AS (
    SELECT 
        e.emp_id,
        UPPER(e.emp_name) as emp_name,
        e.dept_id,
        UPPER(e.country) as country,
        SUM(CAST(s.amount AS DECIMAL(10,2))) as total_sales,
        COUNT(*) as num_sales
    FROM workspace.sql_optimizer_tests.sales s
    INNER JOIN workspace.sql_optimizer_tests.employees e ON CONCAT(CAST(s.emp_id AS STRING), '') = CONCAT(CAST(e.emp_id AS STRING), '')
    WHERE YEAR(s.sale_date) = 2024
    GROUP BY e.emp_id, e.emp_name, e.dept_id, e.country
),
-- CTE 2: Calculate department averages
dept_averages AS (
    SELECT 
        e.dept_id,
        AVG(CAST(s.amount AS DECIMAL(10,2))) as avg_dept_sale,
        COUNT(*) as dept_sale_count
    FROM workspace.sql_optimizer_tests.sales s
    INNER JOIN workspace.sql_optimizer_tests.employees e ON CONCAT(CAST(s.emp_id AS STRING), '') = CONCAT(CAST(e.emp_id AS STRING), '')
    WHERE YEAR(s.sale_date) = 2024
    GROUP BY e.dept_id
),
-- CTE 3: Rank employees within departments
employee_ranks AS (
    SELECT 
        emp_id,
        emp_name,
        dept_id,
        country,
        total_sales,
        num_sales,
        RANK() OVER (PARTITION BY dept_id ORDER BY total_sales DESC) as dept_rank
    FROM employee_totals
),
-- CTE 4: Get department info
dept_info AS (
    SELECT 
        dept_id,
        LOWER(dept_name) as dept_name,
        location
    FROM workspace.sql_optimizer_tests.departments
)

-- Main query: Join all CTEs together
SELECT DISTINCT
    er.emp_name,
    er.total_sales,
    er.num_sales,
    er.dept_rank,
    di.dept_name,
    di.location,
    da.avg_dept_sale,
    da.dept_sale_count,
    CASE 
        WHEN er.total_sales > da.avg_dept_sale * 1.5 THEN 'Top Performer'
        WHEN er.total_sales > da.avg_dept_sale THEN 'Above Average'
        ELSE 'Below Average'
    END as performance_tier
FROM employee_ranks er
INNER JOIN dept_info di ON CONCAT(CAST(er.dept_id AS STRING), '') = CONCAT(CAST(di.dept_id AS STRING), '')
INNER JOIN dept_averages da ON CONCAT(CAST(er.dept_id AS STRING), '') = CONCAT(CAST(da.dept_id AS STRING), '')
WHERE UPPER(er.country) = 'USA'
  AND LOWER(di.dept_name) LIKE '%engineering%'
  AND CAST(er.total_sales AS DECIMAL(10,2)) > 1000
ORDER BY er.dept_rank, er.total_sales DESC;
