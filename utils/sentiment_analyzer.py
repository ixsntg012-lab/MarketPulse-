import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_sentiment(title, description):
    prompt = f"""You are a financial analyst. Analyze this news article about a stock.

Title: {title}
Description: {description}

Respond in EXACT JSON only, no markdown, no extra text:
{{"sentiment": "Bullish", "score": 1, "reason": "one sentence explanation"}}

Rules: Bullish=score 1, Bearish=score -1, Neutral=score 0"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant" 
,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        text = response.choices[0].message.content.strip()
        text = text.replace('```json', '').replace('```', '').strip()
        result = json.loads(text)
        time.sleep(0.5)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return {"sentiment": "Neutral", "score": 0, "reason": "Could not analyze"}

def analyze_multiple_articles(articles):
    results = []
    for article in articles[:10]:
        sentiment = analyze_sentiment(
            article['title'],
            article.get('description', '')
        )
        results.append({
            'title': article['title'],
            'published_at': article['published_at'],
            'sentiment': sentiment['sentiment'],
            'score': sentiment['score'],
            'reason': sentiment['reason']
        })
        emoji = '📈' if sentiment['score']==1 else '📉' if sentiment['score']==-1 else '😐'
        print(f"{emoji} {article['title'][:50]}...")
        print(f"   → {sentiment['sentiment']}: {sentiment['reason']}\n")
    return results

if __name__ == "__main__":
    from news_fetcher import get_stock_news
    import sys
    sys.path.append('..')

    print("Fetching Apple news...\n")
    news = get_stock_news("AAPL", "Apple")

    print("Analyzing sentiment...\n")
    results = analyze_multiple_articles(news)

    total_score = sum(r['score'] for r in results)
    print(f"\n{'='*50}")
    print(f"Overall Sentiment Score: {total_score}")
    if total_score > 2:
        print("Overall: BULLISH 📈")
    elif total_score < -2:
        print("Overall: BEARISH 📉")
    else:
        print("Overall: NEUTRAL 😐")