from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Ensure app.api.news_router is correctly mapped to your file structure
from app.api.news_router import router as news_router

app = FastAPI(
    title="Lead Engine - News Service",
    description="Real-time market news with Redis caching",
    version="1.0.0"
)

# Explicitly defining your Vercel frontend origin
# origins = [
#     "https://news-jobs-research.vercel.app",
#     "http://localhost:3000" # Keeping local dev support
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # WARNING: Only use this if the API is not yet handling private user data
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router registered with the v1 prefix
app.include_router(news_router, prefix="/api/v1", tags=["Market News"])

@app.get("/")
async def root():
    return {"message": "News Service is Online", "status": "ready"}