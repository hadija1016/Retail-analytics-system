import pandas as pd

# Load dataset
df = pd.read_csv('Dataset online retail.csv')
print("Raw rows:", len(df))

# Sirf zaroori columns rakhna
cols = ['InvoiceNo', 'StockCode', 'Item(Description)', 
        'Quantity', 'InvoiceDate', 'UnitPrice', 
        'CustomerID', 'Region', 'Country', 
        'Total Price', 'Order Type']

df = df[cols].copy()

# Null rows remove karo (important columns se)
df.dropna(subset=['InvoiceNo', 'StockCode', 'Quantity', 
                  'InvoiceDate', 'UnitPrice'], inplace=True)

# CustomerID ka null zero se fill karo
df['CustomerID'] = df['CustomerID'].fillna(0).astype(int)

# Data types fix karo
df['Quantity']    = df['Quantity'].astype(int)
df['UnitPrice']   = df['UnitPrice'].astype(float)
df['Total Price'] = df['Total Price'].astype(float)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

print("Clean rows:", len(df))
print("Data cleaning complete!")

# ── TABLE 1: CUSTOMERS ──
stg_customers = df[df['CustomerID'] != 0][['CustomerID', 'Country', 'Region']]
stg_customers = stg_customers.drop_duplicates(subset=['CustomerID']).reset_index(drop=True)
stg_customers.columns = ['CUSTOMER_ID', 'COUNTRY', 'REGION']
print("Customers:", len(stg_customers))

# ── TABLE 2: PRODUCTS ──
stg_products = df[['StockCode', 'Item(Description)', 'UnitPrice']]
stg_products = stg_products.drop_duplicates(subset=['StockCode']).reset_index(drop=True)
stg_products.columns = ['STOCK_CODE', 'DESCRIPTION', 'UNIT_PRICE']
print("Products:", len(stg_products))

# ── TABLE 3: ORDERS ──
stg_orders = df[['InvoiceNo', 'CustomerID', 'InvoiceDate', 'Order Type']]
stg_orders = stg_orders.drop_duplicates(subset=['InvoiceNo']).reset_index(drop=True)
stg_orders.columns = ['INVOICE_NO', 'CUSTOMER_ID', 'INVOICE_DATE', 'ORDER_TYPE']
print("Orders:", len(stg_orders))

# ── TABLE 4: ORDER ITEMS ──
stg_order_items = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'Total Price']].copy()
stg_order_items.columns = ['INVOICE_NO', 'STOCK_CODE', 'QUANTITY', 'UNIT_PRICE', 'LINE_TOTAL']
stg_order_items.insert(0, 'ORDER_ITEM_ID', range(1, len(stg_order_items) + 1))
print("Order Items:", len(stg_order_items))

print("\nAll 4 tables created successfully!")


# Save tables as CSV files
stg_customers.to_csv('stg_customers.csv', index=False)
stg_products.to_csv('stg_products.csv', index=False)
stg_orders.to_csv('stg_orders.csv', index=False)
stg_order_items.to_csv('stg_order_items.csv', index=False)

print("4 CSV files saved successfully!")