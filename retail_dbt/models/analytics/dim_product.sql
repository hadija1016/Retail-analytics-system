{{ config(materialized='table') }}

SELECT
    p.STOCK_CODE,
    p.DESCRIPTION,
    p.UNIT_PRICE,
    c.COMPETITOR_PRICE,
    c.CATEGORY
FROM {{ source('staging', 'STG_PRODUCTS') }} p
LEFT JOIN {{ source('staging', 'STG_COMPETITOR_PRICES') }} c
    ON p.STOCK_CODE = c.STOCK_CODE