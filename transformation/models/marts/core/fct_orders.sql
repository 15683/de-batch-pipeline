{{
    config(
        materialized='table'
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

order_aggregates AS (
    SELECT
        order_id,
        COUNT(*) AS total_items,
        SUM(price) AS total_amount,
        SUM(freight_value) AS total_freight
    FROM order_items
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    DATE(o.order_purchase_timestamp) AS order_purchase_date,
    oa.total_items,
    oa.total_amount,
    oa.total_freight,
    oa.total_amount + oa.total_freight AS grand_total
FROM orders o
LEFT JOIN order_aggregates oa ON o.order_id = oa.order_id
