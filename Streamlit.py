import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

#Load Data
df = pd.read_csv(r"C:\Users\Abuthahir\project\Stock_Analysis\Stockfinaldata.csv")

df['date'] = pd.to_datetime(df['date'])
df.columns = df.columns.str.strip()
df['Ticker'] = df['Ticker'].str.strip().str.upper()
df = df.sort_values(['Ticker', 'date'])

#Yearly Performance (%)
first_close = df.groupby("Ticker")['close'].first()
last_close = df.groupby("Ticker")['close'].last()

performance = pd.DataFrame({
    'Ticker': first_close.index,
    'first_close': first_close.values,
    'last_close': last_close.values
})

performance['yearly_return_pct'] = (
    (performance['last_close'] - performance['first_close'])
    / performance['first_close']
) * 100

#Sector-wise Performance (%)
performance_sector = performance.merge(
    df[['Ticker', 'sector']].drop_duplicates(),
    on='Ticker',
    how='left'
)

sector_perf = (
    performance_sector
    .groupby('sector')['yearly_return_pct']
    .mean()
    .reset_index()
    .sort_values('yearly_return_pct', ascending=False)
)

#Market Summary
green_count = (performance['yearly_return_pct'] > 0).sum()
red_count = (performance['yearly_return_pct'] < 0).sum()
total_stocks = green_count + red_count

green_pct = round((green_count / total_stocks) * 100, 2)
red_pct = round((red_count / total_stocks) * 100, 2)

avg_price = round(df['close'].mean(), 2)
avg_volume = round(df['volume'].mean(), 2)

#Top Gainers / Losers (%)
top_10_gainers = performance.sort_values(
    'yearly_return_pct', ascending=False
).head(10)

top_10_losers = performance.sort_values(
    'yearly_return_pct'
).head(10)

#Daily Return (%) & Volatility
df['daily_return_pct'] = df.groupby('Ticker')['close'].pct_change() * 100

volatility = (
    df.groupby('Ticker')['daily_return_pct']
    .std()
    .reset_index(name='volatility')
)

top_10_volatile = volatility.sort_values(
    'volatility', ascending=False
).head(10)

#Cumulative Return (%)
df['cum_return_pct'] = (
    (1 + df['daily_return_pct'] / 100)
    .groupby(df['Ticker'])
    .cumprod() - 1
) * 100

top_5_cum = top_10_gainers.head(5)['Ticker'].tolist()

# Correlation 
price_df = df.pivot(index='date', columns='Ticker', values='close')
corr = price_df.pct_change().corr()

# Monthly Returns
df['month'] = df['date'].dt.month
monthly_returns = {}

for m in sorted(df['month'].unique()):
    monthly = df[df['month'] == m]
    monthly_return = monthly.groupby('Ticker').apply(
        lambda x: ((x['close'].iloc[-1] - x['close'].iloc[0]) / x['close'].iloc[0]) * 100
    ).reset_index(name='monthly_return_pct')

    monthly_returns[m] = {
        'gainers': monthly_return.sort_values('monthly_return_pct', ascending=False).head(5),
        'losers': monthly_return.sort_values('monthly_return_pct').head(5)
    }


st.title("📊 Stock Analysis Dashboard")

st.sidebar.title("Navigation")
pages = [
    "Market Summary",
    "Top Gainers & Losers",
    "Volatility Analysis",
    "Cumulative Returns",
    "Sector-Wise Performance",
    "Stock Correlation",
    "Monthly Gainers & Losers"
]

selected_page = st.sidebar.radio("Select Page", pages)


if selected_page == "Market Summary":
    st.subheader("Market Overview")
    st.metric("Green Stocks (%)", f"{green_pct}%")
    st.metric("Red Stocks (%)", f"{red_pct}%")
    st.metric("Average Close Price (₹)", avg_price)
    st.metric("Average Volume", avg_volume)

elif selected_page == "Top Gainers & Losers":
    st.subheader("Top 10 Gainers (%)")
    st.table(top_10_gainers[['Ticker', 'yearly_return_pct']].round(2))

    st.subheader("Top 10 Losers (%)")
    st.table(top_10_losers[['Ticker', 'yearly_return_pct']].round(2))

elif selected_page == "Volatility Analysis":
    st.subheader("Top 10 Most Volatile Stocks")
    st.table(top_10_volatile.round(2))

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x='Ticker',
        y='volatility',
        data=top_10_volatile,
        ax=ax
    )
    ax.set_ylabel("Volatility (%)")
    ax.set_title("Top 10 Volatile Stocks")
    st.pyplot(fig)

elif selected_page == "Cumulative Returns":
    st.subheader("Top 5 Stocks – Cumulative Return (%)")
    fig, ax = plt.subplots(figsize=(12, 6))

    for sym in top_5_cum:
        data = df[df['Ticker'] == sym]
        ax.plot(data['date'], data['cum_return_pct'], label=sym)

    ax.set_ylabel("Cumulative Return (%)")
    ax.legend()
    st.pyplot(fig)

elif selected_page == "Sector-Wise Performance":
    st.subheader("Average Yearly Return by Sector (%)")
    st.table(sector_perf.round(2))

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x='sector',
        y='yearly_return_pct',
        data=sector_perf,
        ax=ax
    )
    ax.set_ylabel("Average Return (%)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif selected_page == "Stock Correlation":
    st.subheader("Stock Price Correlation Heatmap")
    top_symbols = top_10_gainers.head(20)['Ticker']

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr.loc[top_symbols, top_symbols],
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        ax=ax
    )
    st.pyplot(fig)

elif selected_page == "Monthly Gainers & Losers":
    st.subheader("Monthly Top 5 Gainers & Losers (%)")

    for m, data in monthly_returns.items():
        st.write(f"### Month {m}")

        fig, ax = plt.subplots(1, 2, figsize=(12, 4))

        sns.barplot(
            x='Ticker',
            y='monthly_return_pct',
            data=data['gainers'],
            ax=ax[0]
        )
        ax[0].set_title("Top 5 Gainers (%)")

        sns.barplot(
            x='Ticker',
            y='monthly_return_pct',
            data=data['losers'],
            ax=ax[1]
        )
        ax[1].set_title("Top 5 Losers (%)")

        st.pyplot(fig)
