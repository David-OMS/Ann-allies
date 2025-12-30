-- SQL Analysis Queries
-- Purpose: Sales and production reporting from manually maintained records

-- ==================================================
-- 1. DAILY REVENUE BY PRODUCT
-- ==================================================

SELECT
    date,
    product_name,
    SUM(quantity_sold) AS units_sold,
    SUM(total_sales) AS daily_revenue
FROM daily_sales_cleaned
GROUP BY date, product_name
ORDER BY date, product_name;

-- ==================================================
-- 2. MONTHLY REVENUE BY PRODUCT
-- ==================================================

SELECT
    year_month,
    product_name,
    SUM(quantity_sold) AS total_units_sold,
    SUM(total_sales) AS monthly_revenue
FROM daily_sales_cleaned
GROUP BY year_month, product_name
ORDER BY year_month, monthly_revenue DESC;

-- ==================================================
-- 3. TOTAL UNITS SOLD PER PRODUCT
-- ==================================================

SELECT
    product_name,
    product_size,
    product_flavor,
    SUM(quantity_sold) AS total_units_sold,
    SUM(total_sales) AS total_revenue,
    COUNT(DISTINCT date) AS days_with_sales
FROM daily_sales_cleaned
GROUP BY product_name, product_size, product_flavor
ORDER BY total_units_sold DESC;

-- ==================================================
-- 4. PRODUCT SIZE COMPARISON (250ml vs 500ml)
-- ==================================================

SELECT
    product_size,
    SUM(quantity_sold) AS total_units_sold,
    SUM(total_sales) AS total_revenue
FROM daily_sales_cleaned
GROUP BY product_size
ORDER BY product_size;

-- ==================================================
-- 5. FLAVOR PERFORMANCE
-- ==================================================

SELECT
    product_flavor,
    SUM(quantity_sold) AS total_units_sold,
    SUM(total_sales) AS total_revenue
FROM daily_sales_cleaned
GROUP BY product_flavor
ORDER BY total_revenue DESC;

-- ==================================================
-- 6. TOTAL PRODUCTION BY PRODUCT
-- ==================================================

SELECT
    product_name,
    product_size,
    product_flavor,
    SUM(quantity_produced) AS total_produced,
    COUNT(DISTINCT date) AS production_days
FROM production_stock_cleaned
GROUP BY product_name, product_size, product_flavor
ORDER BY total_produced DESC;

-- ==================================================
-- 7. PRODUCTION VS RECORDED SALES
-- ==================================================

SELECT
    p.product_name,
    p.product_size,
    p.product_flavor,
    SUM(p.quantity_produced) AS total_produced,
    COALESCE(SUM(s.quantity_sold), 0) AS total_sold,
    SUM(p.quantity_produced) - COALESCE(SUM(s.quantity_sold), 0) AS unit_difference
FROM production_stock_cleaned p
LEFT JOIN daily_sales_cleaned s
    ON p.product_name = s.product_name
GROUP BY p.product_name, p.product_size, p.product_flavor
ORDER BY total_produced DESC;
