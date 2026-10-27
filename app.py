import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yaml
from src.storage.db import query
from src.indicators.technical import enrich
from src.scheduler.jobs import load_watchlist, refresh_all

st.set_page_config(page_title="Stock Monitor", layout="wide", page_icon="📈")

st.title("📈 股票行情监控")

with st.sidebar:
    st.header("自选股")
    cfg = load_watchlist()

    market = st.radio("市场", ["A股", "美股"])
    stock_list = cfg["a_share"] if market == "A股" else cfg["us_share"]
    options = {f"{s['name']} ({s['code']})": s["code"] for s in stock_list}
    label = st.selectbox("选择股票", list(options.keys()))
    code = options[label]

    days = st.slider("回看天数", min_value=30, max_value=365, value=120, step=10)

    if st.button("🔄 刷新数据", type="primary"):
        with st.spinner("正在拉取最新行情..."):
            refresh_all()
        st.success("数据已更新")

df = query(code)
if df.empty:
    st.warning("数据库暂无该股票数据，点击左侧「刷新数据」拉取。")
    st.stop()

df = df.sort_values("date").tail(days).copy()
df = enrich(df)

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest
change = latest["close"] - prev["close"]
change_pct = change / prev["close"] * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("最新价", f"{latest['close']:.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")
c2.metric("MA20", f"{latest['ma20']:.2f}" if latest["ma20"] else "-")
c3.metric("MA60", f"{latest['ma60']:.2f}" if latest["ma60"] else "-")
c4.metric("RSI(14)", f"{latest['rsi']:.1f}" if latest["rsi"] else "-")

fig = make_subplots(
    rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.03,
    row_heights=[0.6, 0.2, 0.2],
    subplot_titles=("K线 + 均线", "MACD", "RSI"),
)

fig.add_trace(go.Candlestick(
    x=df["date"], open=df["open"], high=df["high"], low=df["low"], close=df["close"],
    name="K线", increasing_line_color="#ef5350", decreasing_line_color="#26a69a",
), row=1, col=1)

for ma, color in [("ma5", "#ff9800"), ("ma20", "#2196f3"), ("ma60", "#9c27b0")]:
    fig.add_trace(go.Scatter(x=df["date"], y=df[ma], name=ma.upper(), line=dict(width=1, color=color)), row=1, col=1)

fig.add_trace(go.Bar(x=df["date"], y=df["macd"], name="MACD", marker_color=df["macd"].apply(lambda x: "#ef5350" if x >= 0 else "#26a69a")), row=2, col=1)
fig.add_trace(go.Scatter(x=df["date"], y=df["dif"], name="DIF", line=dict(width=1)), row=2, col=1)
fig.add_trace(go.Scatter(x=df["date"], y=df["dea"], name="DEA", line=dict(width=1)), row=2, col=1)

fig.add_trace(go.Scatter(x=df["date"], y=df["rsi"], name="RSI", line=dict(color="#9c27b0", width=1)), row=3, col=1)
fig.add_hline(y=70, line_dash="dash", line_color="#ef5350", row=3, col=1)
fig.add_hline(y=30, line_dash="dash", line_color="#26a69a", row=3, col=1)

fig.update_layout(
    height=800, xaxis_rangeslider_visible=False,
    margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h"),
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("原始数据"):
    st.dataframe(df.tail(20), use_container_width=True)
