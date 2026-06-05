
    -- Create indexes on join columns and where clause column
    CREATE INDEX idx_employees_dept_id ON workspace.sql_optimizer_tests.employees(dept_id);
    CREATE INDEX idx_employees_emp_id ON workspace.sql_optimizer_tests.employees(emp_id);
    CREATE INDEX idx_departments_dept_id ON workspace.sql_optimizer_tests.departments(dept_id);
    CREATE INDEX idx_sales_emp_id ON workspace.sql_optimizer_tests.sales(emp_id);
    CREATE INDEX idx_employees_salary ON workspace.sql_optimizer_tests.employees(salary);

    SELECT e.emp_name, d.dept_name, s.product
    FROM workspace.sql_optimizer_tests.employees e
    INNER JOIN workspace.sql_optimizer_tests.departments d
        ON e.dept_id = d.dept_id
    INNER JOIN workspace.sql_optimizer_tests.sales s
        ON e.emp_id = s.emp_id
    WHERE e.salary > 80000;
  