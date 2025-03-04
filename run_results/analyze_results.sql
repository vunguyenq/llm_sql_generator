-- 1. Which seller has delivered the most orders to customers in Rio de Janeiro? [string: seller_id]
-- OpenAI query:
SELECT oi.seller_id
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_city = 'Rio de Janeiro'
GROUP BY oi.seller_id
ORDER BY COUNT(DISTINCT oi.order_id) DESC
LIMIT 1;

-- Issue: customer_city is not exactly typed 'Rio de Janeiro'. In customers table it is 'rio de janeiro'
-- => OpenAI understands db schema but not data points
SELECT * FROM customers c WHERE customer_city LIKE '%rio de%%'

------------------------------------------------------------------------------------------------------
-- 2. What's the average review score for products in the 'beleza_saude' category? [float: score]
-- OpenAI query:
SELECT AVG(orvw.review_score) AS average_review_score
FROM order_reviews AS orvw
JOIN orders AS ord ON orvw.order_id = ord.order_id
JOIN order_items AS oitm ON ord.order_id = oitm.order_id
JOIN products AS prod ON oitm.product_id = prod.product_id
WHERE prod.product_category_name = 'beleza_saude';

-- Result looks ok

------------------------------------------------------------------------------------------------------
-- 3. How many sellers have completed orders worth more than 100,000 BRL in total? [integer: count]
-- OpenAI query:
SELECT COUNT(DISTINCT oi.seller_id) AS sellers_count
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY oi.seller_id
HAVING SUM(oi.price) > 100000;

-- Issue: OpenAI query returns a list of all 17 sellers matching the criteria. Lacking the step of counting how many sellers there are (17)
-- => OpenAI doesnt return nested queries or Common Table Expression (WITH clause)?
-- Corrected answer:
SELECT COUNT(*) FROM
(SELECT DISTINCT oi.seller_id
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY oi.seller_id
HAVING SUM(oi.price) > 100000)

------------------------------------------------------------------------------------------------------
-- 4. Which product category has the highest rate of 5-star reviews? [string: category_name]
-- OpenAI query:
SELECT p.product_category_name
FROM order_reviews r
JOIN order_items oi ON r.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE r.review_score = 5
GROUP BY p.product_category_name
ORDER BY COUNT(*) DESC
LIMIT 1;

-- Issue: Ambigous query. Review is on order level, not on order item/ product level?

------------------------------------------------------------------------------------------------------
-- 5. What's the most common payment installment count for orders over 1000 BRL? [integer: installments]
-- OpenAI query:

SELECT payment_installments
FROM order_payments
WHERE order_id IN (
    SELECT order_id
    FROM order_items
    GROUP BY order_id
    HAVING SUM(price) > 1000
)
GROUP BY payment_installments
ORDER BY COUNT(*) DESC
LIMIT 1;

-- Result looks OK

------------------------------------------------------------------------------------------------------
-- 6. Which city has the highest average freight value per order? [string: city_name]
-- OpenAI query:

SELECT s.seller_city
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY s.seller_city
ORDER BY AVG(oi.freight_value) DESC
LIMIT 1;

-- Result looks ok but still ambigous query. By "city", does this mean the city where seller or customer is located?

------------------------------------------------------------------------------------------------------
-- 7. What's the most expensive product category based on average price? [string: category_name]
-- OpenAI query:
SELECT p.product_category_name 
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY AVG(oi.price) DESC
LIMIT 1;

-- Result is correct

------------------------------------------------------------------------------------------------------
-- 8. Which product category has the shortest average delivery time? [string: category_name]
-- OpenAI query:
SELECT p.product_category_name
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY p.product_category_name
ORDER BY AVG(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_purchase_timestamp)) ASC
LIMIT 1;

-- Result looks correct

------------------------------------------------------------------------------------------------------
-- 9. How many orders have items from multiple sellers? [integer: count]
-- OpenAI query:
SELECT COUNT(DISTINCT order_id) AS order_count
FROM order_items
GROUP BY order_id
HAVING COUNT(DISTINCT seller_id) > 1;

-- Issue: Similar to question 3, generated query returns the right list of orders having multiple selæers, but did not do the last step of counting number of orders
-- Corrected query:
SELECT count(*) FROM
(SELECT DISTINCT order_id
FROM order_items
GROUP BY order_id
HAVING COUNT(DISTINCT seller_id) > 1)

------------------------------------------------------------------------------------------------------
-- 10. What percentage of orders are delivered before the estimated delivery date? [float: percentage]
-- OpenAI query:
SELECT (100.0 * SUM(CASE WHEN order_delivered_customer_date < order_estimated_delivery_date THEN 1 ELSE 0 END) / COUNT(*)) AS percentage_delivered_early
FROM orders
WHERE order_delivered_customer_date IS NOT NULL AND order_estimated_delivery_date IS NOT NULL;

-- Result looks OK