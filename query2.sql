SELECT DISTINCT *
FROM (
    SELECT
        s.*,
        c.*,
        p.*,
        d.*
    FROM sales s
    CROSS JOIN customers c
    CROSS JOIN products p
    CROSS JOIN departments d
    WHERE s.customer_id = c.customer_id
      AND s.product_id = p.product_id
      AND p.dept_id = d.dept_id
      AND YEAR(s.sale_date) = 2023
      AND UPPER(c.country) = 'USA'
      AND LOWER(p.category) = 'electronics'
      AND CAST(s.amount AS INTEGER) > 1000
      AND SUBSTRING(
            c.email,
            CHARINDEX('@', c.email) + 1,
            LEN(c.email)
          ) IN (
            SELECT DISTINCT domain
            FROM approved_domains
          )
) base_data
WHERE base_data.sale_id IN (
    SELECT sale_id
    FROM sales
    WHERE MONTH(sale_date) >= 6
      AND MONTH(sale_date) <= 12
)
ORDER BY base_data.sale_date DESC,
         base_data.amount DESC;
