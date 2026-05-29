# Data Storytelling Dashboard

An interactive e-commerce analytics dashboard built to turn transactional data into clear executive-level business insights.

This project is designed for business analytics, strategy, and operations use cases. It helps users track revenue performance, profit trends, customer segments, cohort retention, product contribution, geography-wise sales, and channel performance from a single Streamlit dashboard.

## Live Preview

Run locally using Streamlit:

```bash
streamlit run app/app.py
Key Features



Feature	Description
KPI Overview	Tracks Revenue, Profit, Orders, Customers, AOV, and Margin %.
Business Insight Bar	Highlights top category, best channel, leading market, and margin performance.
Monthly Trend Analysis	Shows revenue, profit, and order volume over time.
Category Analysis	Compares revenue contribution by product category.
Product Analysis	Displays top-performing products by revenue.
Geography Analysis	Breaks down revenue by country and city using an interactive treemap.
Channel Analysis	Shows acquisition channel contribution using a donut chart.
Cohort Retention	Tracks customer retention across monthly cohorts.
RFM Segmentation	Segments customers into Champion, Active, New, Cold, and At-Risk groups.
CSV Export	Allows users to download filtered order data and RFM tables.
Project Structure
text


data-storytelling-dashboard/
├── app/
│   ├── app.py
│   └── utils/
│       └── data_utils.py
├── data/
│   └── orders.csv
├── requirements.txt
├── LICENSE
└── README.md
Tech Stack



Layer	Tools
Language	Python
Dashboard	Streamlit
Visualization	Plotly Express, Plotly Graph Objects
Data Processing	Pandas, NumPy
Styling	Custom CSS
Version Control	Git, GitHub
Dataset
The dashboard uses a synthetic e-commerce dataset with transactional order-level data.

Expected columns:

text


order_id, order_date, customer_id, country, city, channel,
product_id, category, subcategory, unit_price, quantity,
discount, revenue, cost
Getting Started
1. Clone the repository
bash


git clone https://github.com/dhanushkumarb01/data-storytelling-dashboard.git
cd data-storytelling-dashboard
2. Install dependencies
bash


pip install -r requirements.txt
3. Run the dashboard
bash


streamlit run app/app.py
Open the local Streamlit URL shown in the terminal.

Optional: Use Your Own Dataset
You can point the app to your own CSV file using an environment variable.

Windows PowerShell
powershell


$env:ORDERS_CSV="C:\path\to\orders.csv"
streamlit run app/app.py
Linux / macOS
bash


export ORDERS_CSV=/path/to/orders.csv
streamlit run app/app.py
Business Relevance
This project demonstrates skills relevant to analytics and strategy roles:

Business KPI tracking
Data cleaning and transformation
Executive dashboard design
Revenue and profit analysis
Customer segmentation
Retention analysis
Insight-driven storytelling
Python-based data analytics
Author
Dhanush Kumar
B.Tech Computer Science Engineering, 2027
BML Munjal University, Haryana
Email: dhanush.23cse@bmu.edu.in