{{
    config(
        materialized='view'
    )
}}

SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    LOWER(TRIM(customer_city)) AS customer_city,
    UPPER(TRIM(customer_state)) AS customer_state,
    CURRENT_TIMESTAMP AS loaded_at
FROM {{ source('raw', 'olist_customers_dataset') }}
WHERE customer_id IS NOT NULL
