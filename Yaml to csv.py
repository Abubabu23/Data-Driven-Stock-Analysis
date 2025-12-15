import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
df = pd.read_csv(r"C:\Users\Abuthahir\project\Stock_Analysis\Stockfinaldata.csv")

# Preprocessing
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['Ticker', 'date'])
df.columns = df.columns.str.strip()
df['Ticker'] = df['Ticker'].str.strip().str.upper()

# Calculate performance
first_close = df.groupby("Ticker")['close'].first()
last_close = df.groupby("Ticker")['close'].last()

performance = pd.DataFrame({
    'Ticker': first_close.index,
    'first_close': first_close.values,
    'last_close': last_close.values
})

performance['yearly_return'] = ((performance['last_close'] - performance['first_close']) / performance['first_close']) * 100

# Merge sector info
performance_sector = performance.merge(
    df[['Ticker','sector']].drop_duplicates(),
    on='Ticker',
    how='left'
)

sector_perf = performance_sector.groupby('sector')['yearly_return'].mean().reset_index()
sector_perf = sector_perf.sort_values('yearly_return', ascending=False)

# Market summary stats
green_stocks = (performance['yearly_return'] > 0).sum()
red_stocks = (performance['yearly_return'] < 0).sum()
avg_price = df['close'].mean().round(2)
avg_volume = df['volume'].mean().round(2)

# Top gainers/losers
top_10_gainers = performance.sort_values('yearly_return', ascending=False).head(10)
top_10_loser = performance.sort_values('yearly_return').head(10)

# Volatility
df["daily_return"] = df.groupby('Ticker')["close"].pct_change()
volatility = df.groupby('Ticker')["daily_return"].std().reset_index().rename(columns={'daily_return':'volatility'})
top_10_volatile = volatility.sort_values('volatility', ascending=False).head(10)

# Cumulative returns
df['cum_return'] = (1 + df['daily_return']).groupby(df['Ticker']).cumprod() - 1
top_5_cum = performance.sort_values('yearly_return', ascending=False).head(5)['Ticker'].tolist()

# Price correlation
price_df = df.pivot(index='date', columns='Ticker', values='close')
corr = price_df.pct_change().corr()

# Monthly returns
df['month'] = df['date'].dt.month
monthly_returns = {}
for m in sorted(df['month'].unique()):
    monthly = df[df['month'] == m].copy()
    monthly_return = monthly.groupby('Ticker').apply(
        lambda x: (x['close'].iloc[-1] - x['close'].iloc[0]) / x['close'].iloc[0] * 100
    ).reset_index(name='monthly_return')
    top5_gain = monthly_return.sort_values('monthly_return', ascending=False).head(5)
    top5_loss = monthly_return.sort_values('monthly_return').head(5).tail(5)
    monthly_returns[m] = {'gainers': top5_gain, 'losers': top5_loss}

# Streamlit Sidebar
st.sidebar.title("Navigation")
pages = [
    "Market Summary",
    "Top Gainers/Losers",
    "Volatility Analysis",
    "Cumulative Returns",
    "Sector-Wise Performance",
    "Stock Correlation",
    "Monthly Gainers/Losers"
]
selected_page = st.sidebar.radio("Select Page", pages)

st.write(f"### {selected_page}")

# Page Rendering
if selected_page == "Market Summary":
    st.write(f"Green Stocks: {green_stocks}")
    st.write(f"Red Stocks: {red_stocks}")
    st.write(f"Average Close Price: {avg_price}")
    st.write(f"Average Volume: {avg_volume}")

elif selected_page == "Top Gainers/Losers":
    st.subheader("Top 10 Gainers 📈")
    st.table(top_10_gainers[['Ticker','yearly_return']])
    st.subheader("Top 10 Losers 📉")
    st.table(top_10_loser[['Ticker','yearly_return']])

elif selected_page == "Volatility Analysis":
    st.subheader("Top 10 Most Volatile Stocks")
    st.table(top_10_volatile)

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x='Ticker', y='volatility', data=top_10_volatile, palette='Reds_r', ax=ax)
    ax.set_xlabel("Stock")
    ax.set_ylabel("Volatility")
    ax.set_title("Top 10 Most Volatile Stocks")
    st.pyplot(fig)

elif selected_page == "Cumulative Returns":
    st.subheader("Top 5 Performing Stocks by Cumulative Return")
    fig, ax = plt.subplots(figsize=(12,6))
    for sym in top_5_cum:
        data = df[df['Ticker'] == sym]
        ax.plot(data['date'], data['cum_return'], label=sym)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.set_title("Cumulative Return for Top 5 Performing Stocks")
    ax.legend()
    st.pyplot(fig)

elif selected_page == "Sector-Wise Performance":
    st.subheader("Average Yearly Return per Sector")
    st.table(sector_perf)

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x='sector', y='yearly_return', data=sector_perf, palette='Blues_r', ax=ax)
    ax.set_xlabel("Sector")
    ax.set_ylabel("Average Yearly Return (%)")
    ax.set_title("Average Yearly Return by Sector")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif selected_page == "Stock Correlation":
    st.subheader("Stock Price Correlation Heatmap")
    
    top_symbols = performance.sort_values('yearly_return', ascending=False).head(20)['Ticker']
    fig, ax = plt.subplots(figsize=(12,10))
    sns.heatmap(corr.loc[top_symbols, top_symbols], annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, ax=ax)
    st.pyplot(fig)

elif selected_page == "Monthly Gainers/Losers":
    st.title("Monthly Top 5 Gainers & Losers")
    for m in monthly_returns.keys():
        st.subheader(f"Month {m}")
        fig, ax = plt.subplots(1, 2, figsize=(12,4))
        sns.barplot(x='Ticker', y='monthly_return', data=monthly_returns[m]['gainers'], palette='Greens_r', ax=ax[0])
        ax[0].set_title("Top 5 Gainers")
        ax[0].set_ylabel("Monthly Return (%)")
        
        sns.barplot(x='Ticker', y='monthly_return', data=monthly_returns[m]['losers'], palette='Reds_r', ax=ax[1])
        ax[1].set_title("Top 5 Losers")
        ax[1].set_ylabel("Monthly Return (%)")
        
        plt.tight_layout()
        st.pyplot(fig)
