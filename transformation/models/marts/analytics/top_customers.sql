{{
    config(
        materialized='table'
    )
}}

SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state,
    total_orders,
    total_spent,
    avg_order_value,
    first_order_date,
    last_order_date,
    DATEDIFF('day', first_order_date, last_order_date) AS customer_lifetime_days
FROM {{ ref('dim_customers') }}
WHERE total_orders > 0
ORDER BY total_spent DESC
LIMIT 100
