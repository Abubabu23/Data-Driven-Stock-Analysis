import pandas as pd
import os

# ==========================
# FILE PATHS (LOCAL CSV)
# ==========================
DATA_FOLDER = "csv"

PRICES_FILE = os.path.join(DATA_FOLDER, "cleaned_stock_data.csv")
SECTOR_FILE = os.path.join(DATA_FOLDER, "sector_data.csv")   # optional


# ==========================
# LOAD FUNCTIONS
# ==========================
def load_prices():
    df = pd.read_csv(PRICES_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Stock', 'Date'])
    return df


# ✅ AUTO-GENERATED SUMMARY (NO CSV NEEDED)
def load_summary():
    df = load_prices()

    summary = df.groupby('Stock').agg(
        First_Price=('Close', 'first'),
        Last_Price=('Close', 'last')
    ).reset_index()

    summary['One_Year_Return'] = (
        (summary['Last_Price'] - summary['First_Price'])
        / summary['First_Price']
    ) * 100

    return summary[['Stock', 'One_Year_Return']]


def load_sector():
    if os.path.exists(SECTOR_FILE):
        return pd.read_csv(SECTOR_FILE)
    else:
        print("⚠️ sector.csv not found, skipping sector analysis")
        return pd.DataFrame(columns=["Stock", "Sector"])


# ==========================
# 1️⃣ KEY METRICS
# ==========================
def key_metrics():
    summary = load_summary()
    prices = load_prices()

    top_10_green = summary.sort_values("One_Year_Return", ascending=False).head(10)
    top_10_loss = summary.sort_values("One_Year_Return", ascending=True).head(10)

    summary['Performance'] = summary['One_Year_Return'].apply(
        lambda x: "Green" if x > 0 else "Red"
    )

    total_green = (summary['Performance'] == "Green").sum()
    total_red = (summary['Performance'] == "Red").sum()

    avg_price = prices['Close'].mean()
    avg_volume = prices['Volume'].mean()

    market_summary = {
        "Total Green Stocks": int(total_green),
        "Total Red Stocks": int(total_red),
        "Average Price": round(avg_price, 2),
        "Average Volume": round(avg_volume, 2)
    }

    return top_10_green, top_10_loss, market_summary


# ==========================
# 2️⃣ VOLATILITY ANALYSIS
# ==========================
def volatility_analysis():
    df = load_prices()

    df['Daily_Return'] = df.groupby('Stock')['Close'].pct_change()
    vol = df.groupby('Stock')['Daily_Return'].std().dropna()

    top_vol = vol.sort_values(ascending=False).head(10)
    return top_vol.reset_index(name="Volatility")


# ==========================
# 3️⃣ CUMULATIVE RETURNS
# ==========================
def cumulative_returns():
    df = load_prices()

    df['Daily_Return'] = df.groupby('Stock')['Close'].pct_change()
    df['Cumulative_Return'] = df.groupby('Stock')['Daily_Return'].transform(
        lambda x: (1 + x).cumprod() - 1
    )

    final = df.groupby('Stock')['Cumulative_Return'].last().sort_values(ascending=False)
    top_5 = final.head(5).index

    return df[df['Stock'].isin(top_5)]


# ==========================
# 4️⃣ SECTOR PERFORMANCE
# ==========================
def sector_performance():
    summary = load_summary()
    sector = load_sector()

    if sector.empty:
        return pd.DataFrame()

    merged = summary.merge(sector, on="Stock", how="left")
    sector_avg = merged.groupby('Sector')['One_Year_Return'].mean().reset_index()

    return sector_avg


# ==========================
# 5️⃣ CORRELATION MATRIX
# ==========================
def correlation_matrix():
    df = load_prices()

    pivot = df.pivot(index='Date', columns='Stock', values='Close')
    corr = pivot.corr()

    return corr


# ==========================
# 6️⃣ MONTHLY GAINERS / LOSERS
# ==========================
def monthly_gainers_losers():
    df = load_prices()

    df['Month'] = df['Date'].dt.to_period('M')
    df['Month_Return'] = df.groupby('Stock')['Close'].pct_change()

    monthly = df.groupby(['Month', 'Stock'])['Month_Return'].last().reset_index()

    return monthly


# ==========================
# MAIN (TEST RUN)
# ==========================
if __name__ == "__main__":

    print("===== KEY METRICS =====")
    green, loss, summary = key_metrics()
    print(summary)

    print("\nTop 10 Gainers:")
    print(green)

    print("\nTop 10 Losers:")
    print(loss)

    print("\n===== TOP VOLATILITY =====")
    print(volatility_analysis().head())

    print("\n===== SECTOR PERFORMANCE =====")
    print(sector_performance().head())

    print("\n===== CORRELATION MATRIX =====")
    print(correlation_matrix().head())

    print("\n===== CUMULATIVE RETURNS (Top 5 Stocks) =====")
    print(cumulative_returns().head())

    print("\n===== MONTHLY RETURNS =====")
    print(monthly_gainers_losers().head())