{{
    config(
        materialized='table'
    )
}}

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

orders AS (
    SELECT * FROM {{ ref('fct_orders') }}
),

customer_metrics AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        SUM(grand_total) AS total_spent,
        AVG(grand_total) AS avg_order_value,
        MIN(order_purchase_date) AS first_order_date,
        MAX(order_purchase_date) AS last_order_date
    FROM orders
    GROUP BY customer_id
)

SELECT
    c.*,
    cm.total_orders,
    cm.total_spent,
    cm.avg_order_value,
    cm.first_order_date,
    cm.last_order_date
FROM customers c
LEFT JOIN customer_metrics cm ON c.customer_id = cm.customer_id
