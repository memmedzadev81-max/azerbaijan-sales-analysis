-- ============================================================
-- SATIŞ DATASI ANALİZİ - SQL SORĞULARI (SQLite uyğun)
-- Dataset: sales_data.csv (500 sifariş, 2024-2025)
-- ============================================================

-- 1. ÜMUMİ GÖSTERİCİLƏR
SELECT 
    COUNT(*)                        AS total_orders,
    COUNT(DISTINCT customer_id)     AS unique_customers,
    SUM(quantity)                   AS total_items_sold,
    ROUND(SUM(total_amount), 2)     AS total_revenue,
    ROUND(AVG(total_amount), 2)     AS avg_order_value,
    ROUND(MIN(total_amount), 2)     AS min_order,
    ROUND(MAX(total_amount), 2)     AS max_order
FROM sales;


-- 2. REGION ÜZRƏ SATIŞ
SELECT 
    region,
    COUNT(*)                        AS order_count,
    ROUND(SUM(total_amount), 2)     AS total_sales,
    ROUND(AVG(total_amount), 2)     AS avg_order,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 1) AS sales_share_pct
FROM sales
GROUP BY region
ORDER BY total_sales DESC;


-- 3. KATEQORİYA ÜZRƏ SATIŞ
SELECT 
    category,
    COUNT(*)                        AS order_count,
    ROUND(SUM(total_amount), 2)     AS total_sales,
    ROUND(AVG(total_amount), 2)     AS avg_order,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 1) AS pct_of_total
FROM sales
GROUP BY category
ORDER BY total_sales DESC;


-- 4. SATIŞ NÜMAYƏNDƏSİ PERFORMANSI
SELECT 
    salesperson,
    COUNT(*)                        AS orders,
    ROUND(SUM(total_amount), 2)     AS total_sales,
    ROUND(AVG(total_amount), 2)     AS avg_order_value,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 1) AS contribution_pct
FROM sales
GROUP BY salesperson
ORDER BY total_sales DESC;


-- 5. AYLIQ TREND
SELECT 
    year_month,
    COUNT(*)                        AS order_count,
    ROUND(SUM(total_amount), 2)     AS monthly_sales,
    ROUND(AVG(total_amount), 2)     AS avg_order
FROM sales
GROUP BY year_month
ORDER BY year_month;


-- 6. TOP 10 MƏHSUL
SELECT 
    category,
    product,
    COUNT(*)                        AS times_ordered,
    SUM(quantity)                   AS total_qty_sold,
    ROUND(SUM(total_amount), 2)     AS revenue
FROM sales
GROUP BY category, product
ORDER BY revenue DESC
LIMIT 10;


-- 7. TOP 10 MÜŞTƏRİ
SELECT 
    customer_id,
    COUNT(*)                        AS order_count,
    ROUND(SUM(total_amount), 2)     AS total_spent,
    ROUND(AVG(total_amount), 2)     AS avg_order_value,
    MIN(order_date)                 AS first_order,
    MAX(order_date)                 AS last_order
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;


-- 8. ENDİRİM ANALİZİ
SELECT 
    CASE WHEN discount > 0 THEN 'Endirimli' ELSE 'Endirimsiz' END AS discount_status,
    COUNT(*)                        AS order_count,
    ROUND(SUM(total_amount), 2)     AS total_sales,
    ROUND(AVG(total_amount), 2)     AS avg_order,
    ROUND(AVG(discount) * 100, 1)   AS avg_discount_pct
FROM sales
GROUP BY CASE WHEN discount > 0 THEN 'Endirimli' ELSE 'Endirimsiz' END;


-- 9. Hər regionda ən çox satan məhsul
WITH product_sales AS (
    SELECT 
        region,
        product,
        SUM(total_amount) AS product_revenue,
        RANK() OVER (PARTITION BY region ORDER BY SUM(total_amount) DESC) AS rnk
    FROM sales
    GROUP BY region, product
)
SELECT region, product, ROUND(product_revenue, 2) AS revenue
FROM product_sales
WHERE rnk = 1
ORDER BY revenue DESC;


-- 10. Kumulativ satış (Running Total)
WITH monthly AS (
    SELECT 
        year_month,
        SUM(total_amount) AS monthly_sales
    FROM sales
    GROUP BY year_month
)
SELECT 
    year_month,
    ROUND(monthly_sales, 2) AS monthly_sales,
    ROUND(SUM(monthly_sales) OVER (ORDER BY year_month), 2) AS running_total
FROM monthly
ORDER BY year_month;


-- 11. YoY müqayisə (2024 vs 2025)
WITH yearly AS (
    SELECT 
        year,
        month,
        SUM(total_amount) AS sales
    FROM sales
    GROUP BY year, month
)
SELECT 
    a.month,
    ROUND(a.sales, 2) AS sales_2024,
    ROUND(b.sales, 2) AS sales_2025,
    ROUND(b.sales - a.sales, 2) AS difference,
    ROUND((b.sales - a.sales) * 100.0 / NULLIF(a.sales, 0), 1) AS growth_pct
FROM yearly a
JOIN yearly b ON a.month = b.month
WHERE a.year = 2024 AND b.year = 2025
ORDER BY a.month;


-- 12. Müştəri seqmenti
WITH customer_stats AS (
    SELECT 
        customer_id,
        COUNT(*) AS orders,
        SUM(total_amount) AS total_spent
    FROM sales
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN total_spent >= 15000 THEN 'VIP'
        WHEN total_spent >= 8000  THEN 'Yüksək'
        WHEN total_spent >= 3000  THEN 'Orta'
        ELSE 'Aşağı'
    END AS segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(total_spent), 2) AS avg_spent,
    ROUND(SUM(total_spent), 2) AS segment_revenue
FROM customer_stats
GROUP BY 1
ORDER BY avg_spent DESC;
