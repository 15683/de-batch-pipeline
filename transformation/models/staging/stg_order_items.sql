{{
    config(
        materialized='view'
    )
}}

SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    CAST(price AS DECIMAL(10,2)) AS price,
    CAST(freight_value AS DECIMAL(10,2)) AS freight_value,
    CURRENT_TIMESTAMP AS loaded_at
FROM {{ source('raw', 'olist_order_items_dataset') }}
WHERE order_id IS NOT NULL
  AND price >= 0
  AND freight_value >= 0
