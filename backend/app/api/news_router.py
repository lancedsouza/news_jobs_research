from fastapi import APIRouter
from app.services.news_service import fetch_news

router = APIRouter()

@router.get("/health") # Removed the colon that was here
async def health_check():
    return {"status": "ok", "service": "news-router"}

@router.get("/news")
async def get_news():
    """
    Returns news from Redis cache or fetches fresh from NewsAPI
    """
    news_data = fetch_news()
    # Using "results" matches your React frontend logic
    return {"results": news_data}