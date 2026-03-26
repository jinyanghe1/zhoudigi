from fastapi import APIRouter

from app.routers import articles, dynasties, authors, ai, export, search

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(dynasties.router, prefix="/dynasties", tags=["dynasties"])
api_router.include_router(authors.router, prefix="/authors", tags=["authors"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(export.router, prefix="/export", tags=["export"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
