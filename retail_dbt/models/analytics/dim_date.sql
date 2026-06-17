{{ config(materialized='table') }}

SELECT DISTINCT
    TO_CHAR(INVOICE_DATE, 'YYYYMMDD')::INT  AS DATE_ID,
    INVOICE_DATE::DATE                       AS FULL_DATE,
    DAY(INVOICE_DATE)                        AS DAY,
    MONTH(INVOICE_DATE)                      AS MONTH,
    YEAR(INVOICE_DATE)                       AS YEAR,
    MONTHNAME(INVOICE_DATE)                  AS MONTH_NAME,
    DAYNAME(INVOICE_DATE)                    AS DAY_NAME
FROM {{ source('staging', 'STG_ORDERS') }}