import streamlit as st
import plotly.express as px
from analysis import (
    key_metrics, volatility_analysis, cumulative_returns,
    sector_performance, correlation_matrix, monthly_gainers_losers
)

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Nifty 50 Stock Performance Dashboard")

# ==========================
# TABS (CATEGORIES)
# ==========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "⚡ Volatility",
    "📈 Returns",
    "🏭 Sector",
    "🔗 Correlation",
    "📅 Monthly"
])

# ==========================
# 📊 TAB 1 - OVERVIEW
# ==========================
with tab1:
    st.subheader("📊 Market Overview")

    top_10_green, top_10_loss, market_summary = key_metrics()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Green Stocks ↑", market_summary["Total Green Stocks"])
    col2.metric("Red Stocks ↓", market_summary["Total Red Stocks"])
    col3.metric("Avg Price (₹)", market_summary["Average Price"])
    col4.metric("Avg Volume", market_summary["Average Volume"])

    st.write("🟢 Top 10 Best Performing Stocks")
    st.dataframe(top_10_green)

    st.write("🔴 Top 10 Worst Performing Stocks")
    st.dataframe(top_10_loss)


# ==========================
# ⚡ TAB 2 - VOLATILITY
# ==========================
with tab2:
    st.subheader("⚡ Top 10 Most Volatile Stocks")

    vol = volatility_analysis()
    fig_vol = px.bar(vol, x="Stock", y="Volatility")

    st.plotly_chart(fig_vol, use_container_width=True)


# ==========================
# 📈 TAB 3 - RETURNS
# ==========================
with tab3:
    st.subheader("📈 Cumulative Return of Top 5 Stocks")

    cr = cumulative_returns()
    fig_cr = px.line(cr, x="Date", y="Cumulative_Return", color="Stock")

    st.plotly_chart(fig_cr, use_container_width=True)


# ==========================
# 🏭 TAB 4 - SECTOR
# ==========================
with tab4:
    st.subheader("🏭 Sector-wise Performance")

    sec = sector_performance()

    if sec.empty:
        st.warning("No sector data available")
    else:
        fig_sec = px.bar(sec, x="Sector", y="One_Year_Return")
        st.plotly_chart(fig_sec, use_container_width=True)


# ==========================
# 🔗 TAB 5 - CORRELATION
# ==========================
with tab5:
    st.subheader("🔗 Stock Price Correlation Heatmap")

    corr = correlation_matrix()
    fig_corr = px.imshow(corr, color_continuous_scale="RdBu", aspect="auto")

    st.plotly_chart(fig_corr, use_container_width=True)


# ==========================
# 📅 TAB 6 - MONTHLY
# ==========================
with tab6:
    st.subheader("📅 Monthly Gainers & Losers")

    monthly = monthly_gainers_losers()

    month = st.selectbox("Select Month", sorted(monthly["Month"].unique()))
    selected = monthly[monthly["Month"] == month]

    gainers = selected.sort_values("Month_Return", ascending=False).head(5)
    losers = selected.sort_values("Month_Return", ascending=True).head(5)

    col1, col2 = st.columns(2)

    col1.write("🟢 Top 5 Gainers")
    col1.dataframe(gainers)

    col2.write("🔴 Top 5 Losers")
    col2.dataframe(losers)
