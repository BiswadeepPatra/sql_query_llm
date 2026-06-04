
    SELECT DISTINCT 
      s.sale_id,
      s.emp_id,
      s.sale_date,
      s.amount,
      e.emp_id,
      e.dept_id,
      e.country,
      d.dept_id,
      d.dept_name
    FROM workspace.sql_optimizer_tests.sales s
    INNER JOIN workspace.sql_optimizer_tests.employees e
      ON s.emp_id = e.emp_id
    INNER JOIN workspace.sql_optimizer_tests.departments d
      ON e.dept_id = d.dept_id
    WHERE s.sale_date >= '2020-01-01'
      AND s.sale_date < '2020-07-01'
      AND e.country = 'USA'
      AND s.amount > 5000.00
      AND d.dept_name LIKE '%engineering%'
      AND s.sale_id IN (
        SELECT sale_id
        FROM workspace.sql_optimizer_tests.sales
        WHERE sale_date >= '2024-01-01'
          AND sale_date < '2025-01-01'
      )
    ORDER BY s.sale_date DESC,
             s.amount DESC;
  