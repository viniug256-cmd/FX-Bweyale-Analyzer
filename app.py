import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="FX Bweyale", layout="wide")
st.title("📈 FX Bweyale Analyzer")
st.markdown("**Ogwang's Supply & Demand Zones**")

pair = st.sidebar.selectbox("Pair", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X", "AUDUSD=X", "EURJPY=X", "GBPJPY=X", "XAUUSD=X"])
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"])
interval = st.sidebar.selectbox("Interval", ["1h", "4h", "1d"])

@st.cache_data(ttl=300)
def get_data(symbol, period, interval):
    try:
        df = yf.download(symbol, period=period, interval=interval)
        if df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.reset_index(inplace=True)
        return df
    except:
        return None

df = get_data(pair, period, interval)

if df is None or df.empty:
    st.error("No data - try another pair. Yahoo may be busy.")
    st.stop()

def detect_zones(df, lookback=20):
    zones = []
    for i in range(lookback, len(df)-2):
        low = df['Low'].iloc[i]
        high = df['High'].iloc[i]
        if low == df['Low'].iloc[i-lookback:i+3].min():
            zones.append({"type": "Demand", "price": low, "index": i})
        if high == df['High'].iloc[i-lookback:i+3].max():
            zones.append({"type": "Supply", "price": high, "index": i})
    return zones[-8:]

zones = detect_zones(df)

fig = go.Figure(data=[go.Candlestick(x=df['Close'].index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
for z in zones:
    color = "green" if z["type"]=="Demand" else "red"
    fig.add_hline(y=z["price"], line_dash="dash", line_color=color, annotation_text=z["type"])

st.plotly_chart(fig, use_container_width=True)

st.subheader("Zones")
for z in zones:
    st.write(f"{z['type']} at {z['price']:.5f}")

st.success("Bweyale - Live Forex Analysis Running!")
