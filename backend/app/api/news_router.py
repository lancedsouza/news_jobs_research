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
from app.services.news_service import (
    get_market_news,
    get_corporate_news
)

from app.worker.tasks import process_news_task

router = APIRouter()


@router.get("/news")
async def get_market_feed():

    data = get_market_news()

    return {"results": data}


@router.get("/corporate")
async def get_corporate_feed():

    data = get_corporate_news()

    return {"results": data}


@router.get("/ingest_articles")
async def ingest_articles():

    articles = get_market_news()

    queued = 0

    for article in articles:

        title = article.get("title")
        url = article.get("url")

        if url:

            process_news_task.delay(title, url)

            queued += 1

    return {
        "status": "ingestion triggered",
        "articles_queued": queued
    }