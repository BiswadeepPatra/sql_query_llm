
    SELECT DISTINCT 
      s.sale_id,
      s.customer_id,
      s.product_id,
      s.sale_date,
      s.amount,
      c.customer_name,
      c.country,
      c.email,
      p.product_name,
      p.category,
      p.dept_id,
      d.dept_name
    FROM sales s
    INNER JOIN customers c ON s.customer_id = c.customer_id
    INNER JOIN products p ON s.product_id = p.product_id
    INNER JOIN departments d ON p.dept_id = d.dept_id
    WHERE s.sale_date >= '2023-01-01' AND s.sale_date < '2024-01-01'
      AND c.country = 'USA'
      AND p.category = 'electronics'
      AND s.amount > 1000
      AND c.email LIKE '%@%.%' 
      AND SUBSTRING_INDEX(c.email, '@', -1) IN (
        SELECT DISTINCT domain
        FROM approved_domains
      )
    AND s.sale_id IN (
      SELECT sale_id
      FROM sales
      WHERE sale_date >= '2023-06-01' AND sale_date < '2024-01-01'
    )
    ORDER BY s.sale_date DESC,
             s.amount DESC;
  