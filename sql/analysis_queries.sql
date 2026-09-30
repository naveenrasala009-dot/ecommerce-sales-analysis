-- E-Commerce Sales & Customer Analytics
-- Compatible with PostgreSQL-style SQL. Adjust DATE functions for other databases.

-- 1. Total revenue
SELECT ROUND(SUM(sales), 2) AS total_revenue
FROM ecommerce_sales
WHERE order_status = 'Completed';

-- 2. Monthly revenue
SELECT DATE_TRUNC('month', order_date) AS month,
       ROUND(SUM(sales), 2) AS revenue,
       COUNT(DISTINCT order_id) AS orders
FROM ecommerce_sales
GROUP BY 1
ORDER BY 1;

-- 3. Revenue by category
SELECT category,
       ROUND(SUM(sales), 2) AS revenue,
       SUM(quantity) AS units,
       COUNT(DISTINCT order_id) AS orders
FROM ecommerce_sales
GROUP BY category
ORDER BY revenue DESC;

-- 4. Top 10 products
SELECT product,
       category,
       ROUND(SUM(sales), 2) AS revenue,
       SUM(quantity) AS units
FROM ecommerce_sales
GROUP BY product, category
ORDER BY revenue DESC
LIMIT 10;

-- 5. State performance
SELECT state,
       ROUND(SUM(sales), 2) AS revenue,
       COUNT(DISTINCT customer_id) AS customers
FROM ecommerce_sales
GROUP BY state
ORDER BY revenue DESC;

-- 6. Customer lifetime revenue
SELECT customer_id,
       customer_name,
       ROUND(SUM(sales), 2) AS revenue,
       COUNT(DISTINCT order_id) AS orders
FROM ecommerce_sales
GROUP BY customer_id, customer_name
ORDER BY revenue DESC
LIMIT 25;

-- 7. Return rate by category
SELECT category,
       ROUND(100.0 * AVG(CASE WHEN order_status='Returned' THEN 1.0 ELSE 0.0 END), 2) AS return_rate_pct
FROM ecommerce_sales
GROUP BY category
ORDER BY return_rate_pct DESC;

-- 8. Average order value by channel
SELECT channel,
       ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM ecommerce_sales
GROUP BY channel
ORDER BY avg_order_value DESC;
