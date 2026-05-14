from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.news_router import router as news_router

app = FastAPI(
    title="Lead Engine - News Service",
    description="Real-time market news with Redis caching",
    version="1.0.0"
)

# Allow your Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register only the news router
app.include_router(news_router, prefix="/api/v1", tags=["Market News"])

@app.get("/")
async def root():
    return {"message": "News Service is Online", "status": "ready"}