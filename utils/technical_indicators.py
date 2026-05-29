import pandas as pd
import numpy as np

def calculate_rsi(prices, period=14):
    """
    RSI calculate చేస్తుంది
    RSI > 70 = Overbought (Bearish signal)
    RSI < 30 = Oversold (Bullish signal)
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_averages(df):
    """
    Moving averages calculate చేస్తుంది
    """
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    return df

def get_technical_signals(df):
    """
    Technical signals based on indicators
    """
    df = calculate_moving_averages(df)
    df['RSI'] = calculate_rsi(df['Close'])
    
    latest = df.iloc[-1]
    signals = []
    score = 0
    
    # RSI signal
    rsi_value = latest['RSI']
    if rsi_value < 30:
        signals.append(f"RSI={rsi_value:.1f} — Oversold (Bullish)")
        score += 1
    elif rsi_value > 70:
        signals.append(f"RSI={rsi_value:.1f} — Overbought (Bearish)")
        score -= 1
    else:
        signals.append(f"RSI={rsi_value:.1f} — Neutral")
    
    # Moving Average signal
    current_price = latest['Close']
    ma20 = latest['MA_20']
    ma50 = latest['MA_50']
    
    if current_price > ma20 and current_price > ma50:
        signals.append(f"Price above MA20 & MA50 — Bullish Trend")
        score += 1
    elif current_price < ma20 and current_price < ma50:
        signals.append(f"Price below MA20 & MA50 — Bearish Trend")
        score -= 1
    else:
        signals.append(f"Price mixed vs Moving Averages — Neutral")
    
    # Volume signal
    avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
    current_volume = latest['Volume']
    if current_volume > avg_volume * 1.5:
        signals.append(f"High volume — Strong momentum")
        score += 1
    
    return {
        'rsi': round(rsi_value, 2),
        'ma20': round(ma20, 2),
        'ma50': round(ma50, 2),
        'current_price': round(current_price, 2),
        'technical_score': score,
        'signals': signals
    }

# Test చేయడానికి
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from stock_data import get_stock_data
    
    df, summary = get_stock_data("AAPL", period="90d")
    tech = get_technical_signals(df)
    
    print(f"Current Price: ${tech['current_price']}")
    print(f"RSI: {tech['rsi']}")
    print(f"MA20: ${tech['ma20']}")
    print(f"MA50: ${tech['ma50']}")
    print(f"\nTechnical Score: {tech['technical_score']}")
    print("\nSignals:")
    for signal in tech['signals']:
        print(f"  • {signal}")