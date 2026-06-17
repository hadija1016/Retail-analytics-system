{{ config(materialized='table') }}

SELECT
    CUSTOMER_ID,
    COUNTRY,
    REGION
FROM {{ source('staging', 'STG_CUSTOMERS') }}