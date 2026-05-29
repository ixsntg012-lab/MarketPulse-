import yfinance as yf
import pandas as pd

def get_stock_data(ticker, period="90d"):
    """
    Stock historical data fetch చేస్తుంది
    ticker: "AAPL", "TSLA" etc
    period: "7d", "30d", "90d", "1y"
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    if df.empty:
        return None, None
    
    # Basic info
    info = stock.info
    company_name = info.get('longName', ticker)
    current_price = df['Close'].iloc[-1]
    
    # Price change
    price_7d_ago = df['Close'].iloc[-7] if len(df) >= 7 else df['Close'].iloc[0]
    change_7d = ((current_price - price_7d_ago) / price_7d_ago) * 100
    
    summary = {
        'ticker': ticker,
        'company': company_name,
        'current_price': round(current_price, 2),
        'change_7d_percent': round(change_7d, 2),
        'high_90d': round(df['High'].max(), 2),
        'low_90d': round(df['Low'].min(), 2),
    }
    
    return df, summary

# Test చేయడానికి
if __name__ == "__main__":
    df, summary = get_stock_data("AAPL")
    print(summary)
    print(df.tail())