{{
    config(
        materialized='table'
    )
}}

SELECT
    order_purchase_date,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(total_items) AS total_items_sold,
    SUM(total_amount) AS total_revenue,
    SUM(total_freight) AS total_freight_cost,
    SUM(grand_total) AS grand_total_revenue,
    AVG(grand_total) AS avg_order_value,
    MIN(grand_total) AS min_order_value,
    MAX(grand_total) AS max_order_value
FROM {{ ref('fct_orders') }}
WHERE order_status = 'delivered'
GROUP BY order_purchase_date
ORDER BY order_purchase_date DESC
