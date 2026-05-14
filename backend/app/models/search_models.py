from pydantic import BaseModel




class NewsRequest(BaseModel):
     query: str
     top_k: int = 5

class NewsItem(BaseModel):
    title: str
    link: str      # We will map "url" from the JSON to this
    source: str    # We will map "source.name" to this
    date: str      # We will map "publishedAt" to this

class NewsResponse(BaseModel):
    query: str
    top_k: int
    results: list[NewsItem]