from flask import Flask, render_template, request, jsonify
import snowflake.connector
import pandas as pd
import requests
import os
app = Flask(__name__)

def get_snowflake_conn():
    return snowflake.connector.connect(
        user     = "Nooruet06",
        password = "Nooruet06@23-cs-06",
        account  = "qec17511.us-east-1",
        warehouse= "COMPUTE_WH",
        database = "RETAIL_DB",
        schema   = "DBT_ANALYTICS"
    )

def run_query(sql):
    conn = get_snowflake_conn()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

@app.route('/')
def index():
    revenue_df = run_query("""
        SELECT d.FULL_DATE, SUM(f.REVENUE) AS DAILY_REVENUE
        FROM FCT_SALES f
        JOIN DIM_DATE d ON f.DATE_ID = d.DATE_ID
        GROUP BY d.FULL_DATE ORDER BY d.FULL_DATE
    """)
    category_df = run_query("""
        SELECT p.CATEGORY, SUM(f.REVENUE) AS TOTAL_REVENUE
        FROM FCT_SALES f
        JOIN DIM_PRODUCT p ON f.STOCK_CODE = p.STOCK_CODE
        WHERE p.CATEGORY != 'General'
        GROUP BY p.CATEGORY ORDER BY TOTAL_REVENUE DESC
    """)
    customer_df = run_query("""
        SELECT f.CUSTOMER_ID, SUM(f.REVENUE) AS TOTAL_REVENUE
        FROM FCT_SALES f
        WHERE f.CUSTOMER_ID != 0
        GROUP BY f.CUSTOMER_ID ORDER BY TOTAL_REVENUE DESC LIMIT 10
    """)
    return render_template('index.html',
        revenue_dates  = revenue_df['FULL_DATE'].astype(str).tolist(),
        revenue_values = revenue_df['DAILY_REVENUE'].tolist(),
        cat_names      = category_df['CATEGORY'].tolist(),
        cat_values     = category_df['TOTAL_REVENUE'].tolist(),
        cust_ids       = customer_df['CUSTOMER_ID'].tolist(),
        cust_values    = customer_df['TOTAL_REVENUE'].tolist()
    )

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{
                    "role": "user",
                    "content": f"""You are a SQL expert. Generate a Snowflake SQL query for this question:
"{question}"

Tables available:
- FCT_SALES (SALE_ID, CUSTOMER_ID, STOCK_CODE, DATE_ID, QUANTITY, REVENUE, MARGIN, COMPETITOR_PRICE_DELTA)
- DIM_CUSTOMER (CUSTOMER_ID, COUNTRY, REGION)
- DIM_PRODUCT (STOCK_CODE, DESCRIPTION, UNIT_PRICE, COMPETITOR_PRICE, CATEGORY)
- DIM_DATE (DATE_ID, FULL_DATE, DAY, MONTH, YEAR, MONTH_NAME, DAY_NAME)

IMPORTANT RULES:
- Always exclude CUSTOMER_ID = 0 from any query involving customers
- Always exclude CATEGORY = 'General' from any query involving categories

Return ONLY the SQL query, no explanation, no markdown."""
                }],
                "max_tokens": 500
            }
        )

        print("Groq status:", response.status_code)
        print("Groq response:", response.text[:300])

        resp_json = response.json()
        sql = resp_json['choices'][0]['message']['content'].strip()
        sql = sql.replace('```sql', '').replace('```', '').strip()

        result_df = run_query(sql)
        return jsonify({
            'sql': sql,
            'data': result_df.head(10).to_dict(orient='records')
        })
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({'sql': '', 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)