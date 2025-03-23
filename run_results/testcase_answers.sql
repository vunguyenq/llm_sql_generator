-- 1. Which seller has delivered the most orders to customers in Rio de Janeiro? [string: seller_id]

SELECT 
    s.seller_id
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_city = 'rio de janeiro'
    AND o.order_status = 'delivered'
GROUP BY s.seller_id
ORDER BY COUNT(DISTINCT o.order_id) DESC
LIMIT 1;
-- seller_id: 4a3ca9315b744ce9f8e9374361493884 --

-- 2. What's the average review score for products in the 'beleza_saude' category? [float: score]

SELECT 
    ROUND(AVG(r.review_score), 2) as avg_score
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN order_reviews r ON oi.order_id = r.order_id
WHERE p.product_category_name = 'beleza_saude';

-- avg_score: 4.14 --

-- 3. How many sellers have completed orders worth more than 100,000 BRL in total? [integer: count]

SELECT COUNT(*) as seller_count
FROM (
    SELECT s.seller_id
    FROM sellers s
    JOIN order_items oi ON s.seller_id = oi.seller_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY s.seller_id
    HAVING SUM(oi.price) > 100000
) high_value_sellers;

-- seller_count: 17 --

-- 4. Which product category has the highest rate of 5-star reviews? [string: category_name]
SELECT 
    p.product_category_name
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN order_reviews r ON oi.order_id = r.order_id
GROUP BY p.product_category_name
HAVING COUNT(*) > 100
ORDER BY (COUNT(CASE WHEN r.review_score = 5 THEN 1 END) * 100.0 / COUNT(*)) DESC
LIMIT 1;

-- product_category_name: livros_interesse_geral --

-- 5. What's the most common payment installment count for orders over 1000 BRL? [integer: installments]
SELECT 
    payment_installments
FROM order_payments
WHERE payment_value > 1000
GROUP BY payment_installments
ORDER BY COUNT(*) DESC
LIMIT 1;

-- payment_installments: 10 --

-- 6. Which city has the highest average freight value per order? [string: city_name]
SELECT 
    c.customer_city
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_city
HAVING COUNT(DISTINCT o.order_id) > 50
ORDER BY AVG(oi.freight_value) DESC
LIMIT 1;

-- customer_city: 'campina grande'

-- 7. What's the most expensive product category based on average price? [string: category_name]

SELECT 
    p.product_category_name
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_category_name
HAVING COUNT(*) > 10
ORDER BY AVG(oi.price) DESC
LIMIT 1;

-- product_category_name: 'pcs' --

-- 8. Which product category has the shortest average delivery time? [string: category_name]

SELECT 
    p.product_category_name
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_purchase_timestamp IS NOT NULL
GROUP BY p.product_category_name
HAVING COUNT(*) > 100
ORDER BY AVG(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_purchase_timestamp)) ASC
LIMIT 1;

-- product_category_name: alimentos --

-- 9. How many orders have items from multiple sellers? [integer: count]
SELECT COUNT(*) as multi_seller_orders
FROM (
    SELECT order_id
    FROM order_items
    GROUP BY order_id
    HAVING COUNT(DISTINCT seller_id) > 1
) multi_seller;

-- multi_seller_orders: 1278 --

-- 10. What percentage of orders are delivered before the estimated delivery date? [float: percentage]
SELECT 
    ROUND(COUNT(CASE WHEN order_delivered_customer_date < order_estimated_delivery_date THEN 1 END) * 100.0 / COUNT(*), 2) as early_delivery_percentage
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;

-- early_delivery_percentage: 91.89 --