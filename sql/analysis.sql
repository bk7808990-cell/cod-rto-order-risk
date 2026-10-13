-- COD/RTO analysis
-- database: cod_rto, table: orders_clean

USE cod_rto;

-- 1. COD vs Prepaid RTO
-- This is the main one - shows the core difference

SELECT 
    payment_mode,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) AS rto_orders,
    ROUND(SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rto_pct
FROM orders_clean
WHERE delivery_status != 'Cancelled Before Dispatch'
GROUP BY payment_mode;

-- Result: COD 22.63%, Prepaid 5.26%


-- 2. RTO by value band
-- Wanted to check if high-value orders are riskier

SELECT 
    CASE 
        WHEN order_value BETWEEN 300 AND 749 THEN 'A: 300-749'
        WHEN order_value BETWEEN 750 AND 1499 THEN 'B: 750-1499'
        WHEN order_value BETWEEN 1500 AND 2999 THEN 'C: 1500-2999'
        WHEN order_value BETWEEN 3000 AND 5000 THEN 'D: 3000-5000'
        WHEN order_value > 5000 THEN 'E: Bulk'
        ELSE 'Other'
    END AS value_band,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) AS rto_orders,
    ROUND(SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rto_pct
FROM orders_clean
WHERE delivery_status != 'Cancelled Before Dispatch'
GROUP BY value_band
ORDER BY value_band;

-- Result: low value ~14.5%, high value ~18%


-- 3. New vs repeat customers
-- The rule says new customers are riskier, but only for COD

SELECT 
    customer_type,
    payment_mode,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) AS rto_orders,
    ROUND(SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rto_pct
FROM orders_clean
WHERE delivery_status != 'Cancelled Before Dispatch'
GROUP BY customer_type, payment_mode
ORDER BY payment_mode, customer_type;

-- Result: new COD 23.90% vs repeat COD 20.13%. Prepaid shows no difference, as expected.


-- 4. Pincode tier loss
-- Which tiers are costing the most money?

SELECT 
    pincode_tier,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) AS rto_orders,
    ROUND(SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rto_pct,
    ROUND(SUM(CASE WHEN delivery_status = 'RTO' THEN shipping_cost + return_shipping_cost + packaging_cost ELSE 0 END), 0) AS total_loss_rs
FROM orders_clean
WHERE delivery_status != 'Cancelled Before Dispatch'
GROUP BY pincode_tier
ORDER BY total_loss_rs DESC;

-- Result: Tier-3 (Rs 69,660) and Remote (Rs 66,550) are the top two. Together they are 58% of the loss.


-- 5. Monthly trend
-- Wanted to see if RTO is seasonal. The date column was imported as text in DD-MM-YYYY, 
-- so had to use substring instead of DATE_FORMAT.

SELECT 
    CONCAT(SUBSTRING(order_date, 4, 2), '-', RIGHT(order_date, 4)) AS month,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) AS rto_orders,
    ROUND(SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rto_pct
FROM orders_clean
WHERE delivery_status != 'Cancelled Before Dispatch'
GROUP BY month
ORDER BY month;

-- Result: 14.82% to 16.60%. Stable. Not seasonal, it is structural.


-- 6. A/B test result
-- This is the main finding. Control = no call, Treatment = call made.

SELECT 
    `group`,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) AS rto_orders,
    ROUND(SUM(CASE WHEN delivery_status = 'RTO' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rto_pct
FROM orders_clean
WHERE `group` IN ('Control', 'Treatment')
GROUP BY `group`;

-- Result: Control 33.77%, Treatment 25.44%. Reduction of 8.33 points.


-- 7. Loss per RTO

SELECT 
    ROUND(AVG(shipping_cost + return_shipping_cost + packaging_cost), 2) AS avg_loss_per_rto,
    SUM(shipping_cost + return_shipping_cost + packaging_cost) AS total_rto_loss,
    COUNT(*) AS total_rto_orders
FROM orders_clean
WHERE delivery_status = 'RTO';

-- Result: Rs 196.02 average. Total Rs 2,35,415 across 1201 RTOs.


-- 8. Margin per delivered order

SELECT 
    ROUND(AVG(order_value - product_cost - shipping_cost - packaging_cost), 2) AS avg_margin,
    COUNT(*) AS total_delivered
FROM orders_clean
WHERE delivery_status = 'Delivered';

-- Result: Rs 670.70 average, 6399 delivered orders
