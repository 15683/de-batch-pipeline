{{
    config(
        materialized='view'
    )
}}

SELECT
    order_id,
    customer_id,
    LOWER(TRIM(order_status)) AS order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    CURRENT_TIMESTAMP AS loaded_at
FROM {{ source('raw', 'olist_orders_dataset') }}
WHERE order_id IS NOT NULL
  AND customer_id IS NOT NULL
