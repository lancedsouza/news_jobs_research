from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.news_router import router as news_router

app = FastAPI(
    title="Lead Engine - News Service",
    description="Real-time market news with Redis caching",
    version="1.0.0"
)

# Allow your Next.js frontend to talk to this API
origins = [
    "https://news-jobs-research.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register the router once. 
# Your endpoints will now be at /api/v1/news and /api/v1/corporate
app.include_router(news_router, prefix="/api/v1", tags=["Market News"])

@app.get("/")
async def root():
    return {"message": "News Service is Online", "status": "ready"}