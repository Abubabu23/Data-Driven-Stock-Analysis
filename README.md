<img width="1912" height="916" alt="image" src="https://github.com/user-attachments/assets/2645ee61-3a72-44bf-afc6-39de3f4deb6c" /># Stock Performance Dashboard – Nifty 50

An end-to-end data analytics project that analyzes the performance of **Nifty 50 stocks** over the past year.  
The project converts stock data from **YAML format to CSV** and presents key insights through an **interactive Streamlit dashboard**.



## Project Objective

The objective of this project is to help investors, analysts, and market enthusiasts understand stock performance trends by providing:

- Top-performing and worst-performing stocks
- Market overview and summary metrics
- Volatility and risk analysis
- Cumulative return trends
- Sector-wise performance insights
- Stock price correlation analysis
- Monthly top gainers and losers



## Repository Structure
yaml_to_csv.py # Converts monthly YAML stock data into CSV format
streamlit_app.py # Interactive Streamlit dashboard

## Data Workflow

1. **Input Data**
    Stock data is available in YAML format, organized month-wise and date-wise.

2. **Data Transformation**
    `yaml_to_csv.py` extracts, cleans, and converts YAML data into structured CSV files for each stock symbol.

3. **Analysis & Visualization**
   `streamlit_app.py` loads CSV data and performs analysis.
    Results are displayed using interactive charts and metrics in Streamlit.



## Key Features

### Market Overview & Stock Performance Ranking
 Average stock price
 Average trading volume
 Percentage of green vs red stocks
 Top 10 **best-performing (green)** stocks
 Top 10 **worst-performing (red)**
 
 <img width="1915" height="922" alt="Image" src="https://github.com/user-attachments/assets/40f11c6d-a9eb-44b3-aa73-a3bde940c9b2" />
 
### Volatility Analysis
 Daily return calculation
 Standard deviation used to measure volatility
 Top 10 most volatile stocks visualization

<img width="1912" height="916" alt="Image" src="https://github.com/user-attachments/assets/0f5e6055-ac57-4b38-b5bb-24e158810803" />

### Cumulative Return
 Yearly cumulative return calculation
 Line chart for top 5 performing stocks

 <img width="1910" height="918" alt="Image" src="https://github.com/user-attachments/assets/3c42fa8e-ff6a-41a8-8972-07f5b6607496" />

### Sector-wise Performance
 Average yearly return by sector
<img width="1914" height="918" alt="Image" src="https://github.com/user-attachments/assets/3e27eb52-d922-4145-97a7-a85d586dd312" />

### Stock Correlation
 Correlation matrix of stock closing prices
 Heatmap to visualize relationships between stocks
<img width="1915" height="912" alt="Image" src="https://github.com/user-attachments/assets/ca2aab53-eca3-44e6-8a63-e2e6b4494b44" />

### Monthly Gainers & Losers
 Top 5 gainers and losers for each month
<img width="1910" height="908" alt="Image" src="https://github.com/user-attachments/assets/f75a03c9-c8bc-4ff4-a642-c648d021eb4b" />
<img width="1912" height="915" alt="Image" src="https://github.com/user-attachments/assets/12121270-4c86-47d2-b20d-729c066ea50b" />

## Technologies Used

**Language:** Python
**Libraries:** Pandas, PyYAML, Matplotlib
**Visualization:** Streamlit
**Database (Optional):** MySQL / PostgreSQL
**BI Tool (Optional):** Power BI


## How to Run the Project

- Step 1 --> Install Required Libraries
- Step2 -->  Convert YAML to CSV (python yaml_to_csv.py)
- Step3 -->  Run the Streamlit Dashboard (streamlit run streamlit_app.py)


##Why This Project Is Useful**

 - 1.Helps analyze stock performance easily
 - 2.Useful for learning data analytics and visualization
 - 3.Good project for portfolio and interviews
 - 4.Demonstrates real-world financial data analysis

