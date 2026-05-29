import streamlit as st
import os
os.environ['NEWS_API_KEY'] = st.secrets.get("NEWS_API_KEY", "")
os.environ['GROQ_API_KEY'] = st.secrets.get("GROQ_API_KEY", "")
import sys
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
sys.path.append('utils')
sys.path.append('models')

from stock_data import get_stock_data
from news_fetcher import get_stock_news
from sentiment_analyzer import analyze_multiple_articles
from technical_indicators import get_technical_signals
from predictor import predict_tomorrow

# Page config
st.set_page_config(
    page_title="MarketPulse — AI Stock Analyzer",
    page_icon="📈",
    layout="wide"
)

# Header
st.title("📈 MarketPulse")
st.subheader("AI-Powered Stock Sentiment & Prediction System")
st.markdown("---")

# Input
col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input(
        "Enter Stock Ticker Symbol",
        value="AAPL",
        placeholder="e.g. AAPL, TSLA, GOOGL, MSFT"
    ).upper()
with col2:
    analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)

if analyze_btn and ticker:
    
    # Stock Data
    with st.spinner(f"Fetching {ticker} data..."):
        df, summary = get_stock_data(ticker)
    
    if df is None:
        st.error(f"❌ Could not find stock: {ticker}. Please check the ticker symbol.")
        st.stop()
    
    # Summary Cards
    st.markdown("### 📊 Stock Overview")
    c1, c2, c3, c4 = st.columns(4)
    
    change_color = "green" if summary['change_7d_percent'] > 0 else "red"
    change_arrow = "▲" if summary['change_7d_percent'] > 0 else "▼"
    
    c1.metric("Company", summary['company'])
    c2.metric("Current Price", f"${summary['current_price']}")
    c3.metric("7-Day Change", f"{change_arrow} {abs(summary['change_7d_percent'])}%")
    c4.metric("90D High / Low", f"${summary['high_90d']} / ${summary['low_90d']}")
    
    st.markdown("---")
    
    # Price Chart
    st.markdown("### 📉 Price History (90 Days)")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=ticker
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'].rolling(20).mean(),
        name='MA20', line=dict(color='orange', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'].rolling(50).mean(),
        name='MA50', line=dict(color='blue', width=1.5)
    ))
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=400,
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Two columns for Technical + Sentiment
    left, right = st.columns(2)
    
    with left:
        st.markdown("### 🔧 Technical Analysis")
        with st.spinner("Calculating indicators..."):
            tech = get_technical_signals(df)
        
        t1, t2, t3 = st.columns(3)
        rsi_color = "🔴" if tech['rsi'] > 70 else "🟢" if tech['rsi'] < 30 else "🟡"
        t1.metric("RSI", f"{rsi_color} {tech['rsi']}")
        t2.metric("MA20", f"${tech['ma20']}")
        t3.metric("MA50", f"${tech['ma50']}")
        
        for signal in tech['signals']:
            if 'Bullish' in signal:
                st.success(f"✅ {signal}")
            elif 'Bearish' in signal:
                st.error(f"❌ {signal}")
            else:
                st.info(f"ℹ️ {signal}")
    
    with right:
        st.markdown("### 📰 News Sentiment Analysis")
        with st.spinner("Analyzing news..."):
            news = get_stock_news(ticker, summary['company'])
            sentiment_results = analyze_multiple_articles(news)
        
        total_score = sum(r['score'] for r in sentiment_results)
        
        if total_score > 2:
            st.success(f"### 📈 BULLISH (Score: +{total_score})")
        elif total_score < -2:
            st.error(f"### 📉 BEARISH (Score: {total_score})")
        else:
            st.info(f"### 😐 NEUTRAL (Score: {total_score})")
        
        for r in sentiment_results[:5]:
            emoji = "📈" if r['score'] == 1 else "📉" if r['score'] == -1 else "😐"
            with st.expander(f"{emoji} {r['title'][:60]}..."):
                st.write(f"**Sentiment:** {r['sentiment']}")
                st.write(f"**Reason:** {r['reason']}")
    
    st.markdown("---")
    
    # Final Prediction
    st.markdown("### 🤖 AI Prediction")
    with st.spinner("Running ML model..."):
        prediction = predict_tomorrow(ticker, total_score)
    
    pred_col1, pred_col2 = st.columns([1, 2])
    with pred_col1:
        if "UP" in prediction['prediction']:
            st.success(f"## {prediction['prediction']}")
            st.write("Model predicts price will go **UP** tomorrow")
        else:
            st.error(f"## {prediction['prediction']}")
            st.write("Model predicts price will go **DOWN** tomorrow")
        
        st.metric("Confidence", f"{prediction['confidence']}%")
        st.metric("Model Accuracy", f"{prediction['model_accuracy']}%")
    
    with pred_col2:
        st.warning("""
        ⚠️ **Disclaimer**
        
        This is an educational AI project for learning purposes only.
        
        **Do NOT use this for actual investment decisions.**
        
        Stock market predictions are inherently uncertain. Past performance 
        does not guarantee future results.
        """)
    
    st.markdown("---")
    st.caption("MarketPulse — Built with Python, Groq AI, yfinance & Streamlit | Educational Project")
