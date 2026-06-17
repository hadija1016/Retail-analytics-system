{{ config(materialized='table') }}

SELECT
    ROW_NUMBER() OVER (ORDER BY oi.INVOICE_NO, oi.STOCK_CODE) AS SALE_ID,
    o.CUSTOMER_ID,
    oi.STOCK_CODE,
    TO_CHAR(o.INVOICE_DATE, 'YYYYMMDD')::INT                  AS DATE_ID,
    oi.QUANTITY,
    oi.LINE_TOTAL                                              AS REVENUE,
    oi.LINE_TOTAL - (oi.QUANTITY * oi.UNIT_PRICE)              AS MARGIN,
    c.COMPETITOR_PRICE - oi.UNIT_PRICE                         AS COMPETITOR_PRICE_DELTA
FROM {{ source('staging', 'STG_ORDER_ITEMS') }} oi
JOIN {{ source('staging', 'STG_ORDERS') }} o
    ON oi.INVOICE_NO = o.INVOICE_NO
LEFT JOIN {{ source('staging', 'STG_COMPETITOR_PRICES') }} c
    ON oi.STOCK_CODE = c.STOCK_CODE