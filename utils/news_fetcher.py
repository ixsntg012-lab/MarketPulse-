import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_stock_news(ticker, company_name, days=30):
    """
    Company గురించి recent news fetch చేస్తుంది
    """
    # 30 days back date calculate చేయడం
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': f"{company_name} OR {ticker} stock",
        'from': from_date,
        'sortBy': 'relevancy',
        'language': 'en',
        'pageSize': 20,
        'apiKey': NEWS_API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['status'] != 'ok':
        print(f"Error: {data.get('message')}")
        return []
    
    articles = []
    for article in data['articles']:
        if article['title'] and article['description']:
            articles.append({
                'title': article['title'],
                'description': article['description'],
                'published_at': article['publishedAt'],
                'source': article['source']['name']
            })
    
    return articles

# Test చేయడానికి
if __name__ == "__main__":
    news = get_stock_news("AAPL", "Apple")
    print(f"Found {len(news)} articles\n")
    for article in news[:3]:
        print(f"📰 {article['title']}")
        print(f"   {article['published_at']}")
        print()