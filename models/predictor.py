import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import sys
sys.path.append('utils')
from stock_data import get_stock_data
from technical_indicators import calculate_rsi, calculate_moving_averages

def prepare_features(df):
    """
    ML model కి features prepare చేస్తుంది
    """
    df = calculate_moving_averages(df)
    df['RSI'] = calculate_rsi(df['Close'])
    
    # Price changes
    df['return_1d'] = df['Close'].pct_change(1)
    df['return_5d'] = df['Close'].pct_change(5)
    df['return_10d'] = df['Close'].pct_change(10)
    
    # Volume change
    df['volume_change'] = df['Volume'].pct_change(1)
    
    # Price vs Moving Averages
    df['price_vs_ma20'] = (df['Close'] - df['MA_20']) / df['MA_20']
    df['price_vs_ma50'] = (df['Close'] - df['MA_50']) / df['MA_50']
    
    # Target: next day price up or down?
    df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    
    return df.dropna()

def train_model(ticker="AAPL"):
    """
    Model train చేస్తుంది
    """
    df, _ = get_stock_data(ticker, period="1y")
    
    if df is None:
        return None, None, None
    
    df = prepare_features(df)
    
    features = ['RSI', 'return_1d', 'return_5d', 'return_10d',
                'volume_change', 'price_vs_ma20', 'price_vs_ma50']
    
    X = df[features]
    y = df['target']
    
    # Train/test split
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    accuracy = model.score(X_test_scaled, y_test)
    
    return model, scaler, accuracy

def predict_tomorrow(ticker, sentiment_score=0):
    """
    Tomorrow's direction predict చేస్తుంది
    """
    model, scaler, accuracy = train_model(ticker)
    
    if model is None:
        return None
    
    df, summary = get_stock_data(ticker, period="90d")
    df = prepare_features(df)
    
    features = ['RSI', 'return_1d', 'return_5d', 'return_10d',
                'volume_change', 'price_vs_ma20', 'price_vs_ma50']
    
    latest = df[features].iloc[-1:].values
    latest_scaled = scaler.transform(latest)
    
    prediction = model.predict(latest_scaled)[0]
    probability = model.predict_proba(latest_scaled)[0]
    
    confidence = max(probability) * 100
    
    # Combine with sentiment
    final_score = prediction + (sentiment_score * 0.3)
    
    result = {
        'ticker': ticker,
        'current_price': summary['current_price'],
        'prediction': 'UP 📈' if prediction == 1 else 'DOWN 📉',
        'confidence': round(confidence, 1),
        'model_accuracy': round(accuracy * 100, 1),
        'sentiment_score': sentiment_score
    }
    
    return result

if __name__ == "__main__":
    print("Training model for AAPL...\n")
    result = predict_tomorrow("AAPL", sentiment_score=2)
    
    print(f"Stock: {result['ticker']}")
    print(f"Current Price: ${result['current_price']}")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Model Accuracy: {result['model_accuracy']}%")