from bs4 import BeautifulSoup
import pandas as pd

# HTML file read 
with open('competitor_site.html', 'r', encoding='utf-8') as f:
    html = f.read()

# parse from BeautifulSoup 
soup = BeautifulSoup(html, 'html.parser')

# Table find and extract data 
table = soup.find('table', {'id': 'products'})
rows = table.find('tbody').find_all('tr')

records = []
for row in rows:
    cols = row.find_all('td')
    records.append({
        'STOCK_CODE':        cols[0].text.strip(),
        'PRODUCT_NAME':      cols[1].text.strip(),
        'COMPETITOR_PRICE':  float(cols[2].text.strip()),
        'CATEGORY':          cols[3].text.strip(),
    })

# DataFrame 
df_comp = pd.DataFrame(records)
print(df_comp)

# CSV save 
df_comp.to_csv('stg_competitor_prices.csv', index=False)
print("\nScraping complete! File saved: stg_competitor_prices.csv")