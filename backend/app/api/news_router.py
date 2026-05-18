# from fastapi import APIRouter
# from app.services.news_service import fetch_news

# router = APIRouter()

# @router.get("/health") # Removed the colon that was here
# async def health_check():
#     return {"status": "ok", "service": "news-router"}

# @router.get("/news")
# async def get_news():
#     """
#     Returns news from Redis cache or fetches fresh from NewsAPI
#     """
#     news_data = fetch_news()
#     # Using "results" matches your React frontend logic
#     return {"results": news_data}

# 
# --------------------------------------------------------------------------------------------------
# This is the API router for news-related endpoints. It defines the routes and connects them to the news service logic.

# app/api/news_router.py
from fastapi import APIRouter
from app.services.news_service import get_market_news, get_corporate_news  # Assuming script name

router = APIRouter()

@router.get("/news")
async def get_market_feed():
    """Serves the right-hand Market Insights feed"""
    data = get_market_news()
    return {"results": data}

@router.get("/corporate")
async def get_corporate_feed():
    """Serves the left-hand Corporate Intelligence feed"""
    data = get_corporate_news()
    return {"results": data}