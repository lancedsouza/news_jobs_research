import os
import redis
import requests
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "redis") 
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

CACHE_KEY = "market_news_cache"

def fetch_raw_news():
    api_key = os.getenv("NEWS_API_KEY")
    # Change 1: Use 'everything' instead of 'top-headlines'
    # Change 2: Query for "tech OR ai OR startups india"
    url = f"https://newsapi.org/v2/everything?q=tech+OR+ai+OR+startups+india&sortBy=publishedAt&language=en&apiKey={api_key}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # Change 3: Only take the first 10 articles so the sidebar isn't massive
        articles = response.json().get("articles", [])
        return articles[:10] 
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return []

def fetch_news():
    try:
        cached_data = redis_client.get(CACHE_KEY)
        if cached_data:
            print("✅ Cache Hit: Serving from Redis")
            return json.loads(cached_data) 
        
        print("🚀 Cache Miss: Fetching from NewsAPI")
        news_list = fetch_raw_news()
        
        if news_list:
            redis_client.setex(CACHE_KEY, 3600, json.dumps(news_list))
        
        return news_list

    except redis.exceptions.ConnectionError:
        print("⚠️ Redis is down. Falling back to direct API call.")
        return fetch_raw_news()