SELECT DISTINCT *
FROM (
    SELECT
        e.*,
        d.*,
        s.*
    FROM workspace.sql_optimizer_tests.sales s
    CROSS JOIN workspace.sql_optimizer_tests.employees e
    CROSS JOIN workspace.sql_optimizer_tests.departments d
    WHERE s.emp_id = e.emp_id
      AND e.dept_id = d.dept_id
      AND YEAR(s.sale_date) = 2020
      AND MONTH(s.sale_date) BETWEEN 1 AND 6
      AND UPPER(e.country) = 'USA'
      AND CAST(s.amount AS DECIMAL(10,2)) > 5000
      AND LOWER(d.dept_name) LIKE '%engineering%'
) base_query
WHERE base_query.sale_id IN (
    SELECT sale_id
    FROM workspace.sql_optimizer_tests.sales
    WHERE YEAR(sale_date) = 2020
)
ORDER BY base_query.sale_date DESC,
         base_query.amount DESC;
