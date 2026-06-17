import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# ── Snowflake Details ──
conn = snowflake.connector.connect(
    user     = "Nooruet06",    #  Snowflake username 
    password = "Nooruet06@23-cs-06",    #  password 
    account  = "qec17511.us-east-1",
    warehouse= "COMPUTE_WH",
    database = "RETAIL_DB",
    schema   = "STAGING"
)

print("Snowflake connected!")

# ── CSVs Load  ──
stg_customers    = pd.read_csv('stg_customers.csv')
stg_products     = pd.read_csv('stg_products.csv')
stg_orders       = pd.read_csv('stg_orders.csv')
stg_order_items  = pd.read_csv('stg_order_items.csv')
stg_competitor   = pd.read_csv('stg_competitor_prices.csv')

# ── load into Snowflake  ──
tables = {
    "STG_CUSTOMERS":        stg_customers,
    "STG_PRODUCTS":         stg_products,
    "STG_ORDERS":           stg_orders,
    "STG_ORDER_ITEMS":      stg_order_items,
    "STG_COMPETITOR_PRICES": stg_competitor,
}

for table_name, df in tables.items():
    success, _, nrows, _ = write_pandas(
        conn, df, table_name,
        database="RETAIL_DB",
        schema="STAGING",
        overwrite=True
    )
    print(f"{table_name}: {nrows} rows loaded — {'OK' if success else 'FAILED'}")

conn.close()
print("\nAll data loaded successfully!")