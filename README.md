# Stock Performance Dashboard – Nifty 50

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

### Market Overview
 Average stock price
 Average trading volume
 Percentage of green vs red stocks
 <img width="1915" height="922" alt="Image" src="https://github.com/user-attachments/assets/40f11c6d-a9eb-44b3-aa73-a3bde940c9b2" />
 
### Stock Performance Ranking
 Top 10 **best-performing (green)** stocks
 Top 10 **worst-performing (red)** stocks
 
<img width="1911" height="859" alt="Image" src="https://github.com/user-attachments/assets/9b277ebb-122c-4d9a-b894-15ca930c4fad" />

<img width="1914" height="921" alt="Image" src="https://github.com/user-attachments/assets/bee68cac-e696-4e66-ab8a-f7cc1e48e884" />

### Volatility Analysis
 Daily return calculation
 Standard deviation used to measure volatility
 Top 10 most volatile stocks visualization

<img width="1910" height="925" alt="Image" src="https://github.com/user-attachments/assets/e9c84a0a-3af4-4c23-9d8d-9416e14b20db" />

### Cumulative Return
 Yearly cumulative return calculation
 Line chart for top 5 performing stocks

 <img width="1913" height="921" alt="Image" src="https://github.com/user-attachments/assets/f37bdb98-0b08-4032-a924-68ab8da46e88" />

### Sector-wise Performance
 Average yearly return by sector

 <img width="1905" height="913" alt="Image" src="https://github.com/user-attachments/assets/775ff0ee-2650-41df-b363-91f645477bbc" />
 <img width="1904" height="915" alt="Image" src="https://github.com/user-attachments/assets/99f6530c-157b-4dc0-a28c-93b67cbb3d01" />

### Stock Correlation
 Correlation matrix of stock closing prices
 Heatmap to visualize relationships between stocks

 <img width="1911" height="922" alt="Image" src="https://github.com/user-attachments/assets/09d656d9-f7e9-467f-85c8-4c6a7708783c" />

### Monthly Gainers & Losers
 Top 5 gainers and losers for each month
<img width="1910" height="908" alt="Image" src="https://github.com/user-attachments/assets/f75a03c9-c8bc-4ff4-a642-c648d021eb4b" />

### PowerBi Dashboard

<img width="1353" height="748" alt="Image" src="https://github.com/user-attachments/assets/3c5b1ee4-bce3-4091-ac51-8b415022d3bd" />

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

