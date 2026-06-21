# 🛒Enterprise Retail Analytics Engine (Capstone Project)

An end-to-end modern data engineering and analytics platform that transforms raw retail data into actionable business insights. The system features an interactive Flask dashboard backed by a Snowflake cloud data warehouse, automated dbt data modeling, and a cutting-edge generative AI assistant powered by Groq to query data using plain English.

---

## 🚀 Key Features

*   **Live Executive Dashboard:** Interactive user interface tracking high-level KPIs, operational metrics, and revenue trends.
*   **Modern Data Stack (MDS) Pipeline:** Automated extraction, transformation, and dimensional modeling utilizing **dbt** inside **Snowflake**.
*   **AI-Powered "Ask Your Data":** Integration with **Groq AI** that translates natural language questions into complex, executable Snowflake SQL queries on-the-fly.
*   **Dynamic Visualizations:** Rich, color-coded charts showcasing dynamic daily revenue spikes, product category performance, and top customer segments.

---

## 🛠️ Tech Stack & Architecture

*   **Frontend/Backend:** Flask (Python)
*   **Data Warehouse:** Snowflake Cloud Data Platform
*   **Data Transformation & Modeling:** dbt (Data Build Tool)
*   **LLM/Generative AI:** Groq AI (Natural Language to SQL Engine)
*   **Visualizations:** Chart.js / HTML5 / Bootstrap CSS

---

## 📊 Core Business Metrics Tracked

| Metric | Overview |
| :--- | :--- |
| **Total Revenue** | £337K+ accumulated across global operations |
| **Order Volume** | 937 enterprise orders processed |
| **Customer Base** | 560 unique global customers |
| **Catalog Breadth** | 2,408 active product SKUs |
| **Global Reach** | Transactional operations spanning 38 countries |

---

## 🖥️ Project Structure & Flow

1. **Data Ingestion & dbt Modeling:** Raw transactional retail data is moved to Snowflake. dbt models raw data into clean staging tables and optimized business marts (handling bulk orders, daily trends, and top customer rankings like *Customer 18102*).
2. **Flask Application Layer:** Connects securely to Snowflake via Python connectors to fetch live analytical views.
3. **Groq AI Integration:** Intercepts plain-English user prompts, parses metadata context, converts it to valid Snowflake-compliant SQL, and streams structured results directly to the interface.

---

## 🛠️ Local Setup & Installation

Follow these steps to run the analytics engine locally:

### Prerequisite Checklist
* Python 3.9+ installed
* Active Snowflake Account with warehouse credentials
* Groq API Key

### 1. Clone the Repository
```bash
git clone [https://github.com/hadija1016/Retail-analytics-system.git](https://github.com/hadija1016/Retail-analytics-system.git)
cd Retail-analytics-system
