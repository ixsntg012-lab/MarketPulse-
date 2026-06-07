# MarketPulse 📈

<div align="center">

**AI-powered stock sentiment analyzer — real-time news analysis, technical indicators, ML price prediction**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_AI-LLaMA_3.1-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

## What It Does

1. Enter any **stock ticker** (AAPL, TSLA, GOOGL, MSFT...)
2. System fetches **real-time news articles** via NewsAPI
3. Groq's LLaMA 3.1 **analyzes sentiment** of each article (Bullish 📈 / Bearish 📉 / Neutral 😐)
4. **Technical indicators** calculated — RSI, MA20, MA50 from 90-day price history
5. **Random Forest ML model** predicts tomorrow's price direction
6. Everything displayed in an **interactive Streamlit dashboard** with candlestick charts

> **Problem:** Retail investors are overwhelmed by the volume of financial news. Reading 20+ articles manually to gauge market sentiment is time-consuming and inconsistent. MarketPulse automates this — one click, instant AI-powered analysis for any stock.

---

## Features

| Feature | Description |
|---------|-------------|
| LLM Sentiment Analysis | Groq LLaMA 3.1 classifies each news article as Bullish/Bearish/Neutral |
| Technical Indicators | RSI, 20-day MA, 50-day MA calculated from historical data |
| ML Price Prediction | Random Forest trained on 1-year data predicts direction + confidence % |
| Candlestick Chart | Interactive 90-day price chart with MA overlays via Plotly |
| News Breakdown | Per-article sentiment with reason shown in expandable cards |
| Any stock ticker | Works for any publicly traded stock on US markets |
| Live deployment | Deployed on Streamlit Cloud — no setup required |

---

## How It Works
