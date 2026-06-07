# MarketPulse 📈

<div align="center">

**AI-powered stock sentiment analyzer — real-time news analysis, technical indicators, ML price prediction**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_AI-LLaMA_3.1-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

🚀 **[Live Demo](https://swetha-marketpulse.streamlit.app)**

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

```
User enters ticker (e.g., AAPL)
        │
        ▼
yfinance → 90-day OHLCV price history
NewsAPI  → Last 30 days of news articles
        │
        ▼
Groq LLaMA 3.1 — Analyze each article → structured JSON
  {
    "sentiment": "Bullish",
    "score": 1,
    "reason": "Apple Mac Studio shortage indicates high demand"
  }
        │
        ▼
Technical Indicators calculated
  RSI=84.3 → Overbought (Bearish signal)
  Price > MA20 & MA50 → Bullish trend
        │
        ▼
Random Forest ML Model
  Features: RSI, 1d/5d/10d returns, volume change, price vs MA
  Output: UP 📈 or DOWN 📉 + confidence %
        │
        ▼
Streamlit Dashboard
  Candlestick chart + sentiment breakdown + AI prediction
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM Sentiment | Groq API (LLaMA 3.1-8b-instant) |
| Stock Data | yfinance (Yahoo Finance) |
| News Data | NewsAPI |
| ML Prediction | Scikit-learn (Random Forest Classifier) |
| Technical Indicators | RSI, MA20, MA50, Volume ratio |
| Visualization | Plotly (Candlestick + line charts) |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## Installation

```bash
git clone https://github.com/ixsntg012-lab/MarketPulse-.git
cd MarketPulse-
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_newsapi_key
```

Get free API keys:
- 🔑 Groq API: [console.groq.com](https://console.groq.com)
- 🔑 NewsAPI: [newsapi.org](https://newsapi.org)

---

## Usage

```bash
streamlit run app.py
```

Open browser: `http://localhost:8501`

---

## Project Structure

```
MarketPulse/
│
├── utils/
│   ├── stock_data.py           ← yfinance data fetching + summary
│   ├── news_fetcher.py         ← NewsAPI integration
│   ├── sentiment_analyzer.py   ← Groq LLM sentiment analysis
│   └── technical_indicators.py ← RSI, MA20, MA50 calculations
│
├── models/
│   └── predictor.py            ← Random Forest training + prediction
│
├── app.py                      ← Main Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## Limitations & Future Work

**Phase 1 — Better Sentiment**
- Multi-window weighted sentiment (7d, 30d, 90d) with recency bias
- Social media sentiment from Reddit WallStreetBets + Twitter
- Filter irrelevant articles with semantic similarity scoring

**Phase 2 — Better Prediction**
- Replace Random Forest with LSTM for temporal pattern capture
- Add earnings dates, options flow, and sector momentum as features
- Proper backtesting framework with walk-forward validation

**Phase 3 — More Features**
- Portfolio tracker — monitor multiple stocks simultaneously
- Email/SMS alerts when sentiment shifts significantly
- Competitor comparison (AAPL vs MSFT vs GOOGL side-by-side)

**Phase 4 — Production**
- Real-time WebSocket price updates
- User accounts with watchlists
- Paid data sources for higher API limits

---

## ⚠️ Disclaimer

> This is an **educational AI project** for learning purposes only.
> **Do NOT use for actual investment decisions.**
> Stock market predictions are inherently uncertain. Past performance does not guarantee future results.

---

## Author

**Swetha Kiran Veernapu**  
MS Computer Science @ UCF  
[LinkedIn](https://linkedin.com/in/swetha-kiran-veernapu) · [GitHub](https://github.com/ixsntg012-lab)

---

## License

MIT License
