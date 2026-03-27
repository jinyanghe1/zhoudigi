from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ResponseModel, ListResponse, Article, ArticleDetail
from app.models import Article as ArticleModel

router = APIRouter()


@router.get("", response_model=ResponseModel[ListResponse[Article]])
async def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    dynasty_id: Optional[int] = None,
    author_id: Optional[int] = None,
    category: Optional[str] = None,
    is_selected: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    from sqlalchemy.orm import joinedload
    query = db.query(ArticleModel).options(
        joinedload(ArticleModel.author),
        joinedload(ArticleModel.dynasty)
    )
    
    # 筛选条件
    if dynasty_id:
        query = query.filter(ArticleModel.dynasty_id == dynasty_id)
    if author_id:
        query = query.filter(ArticleModel.author_id == author_id)
    if category:
        query = query.filter(ArticleModel.category == category)
    if is_selected is not None:
        query = query.filter(ArticleModel.is_selected == is_selected)
    
    # 分页
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    articles = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return ResponseModel(data={
        "items": articles,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        }
    })


@router.get("/search", response_model=ResponseModel[ListResponse[Article]])
async def search_articles(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索文章"""
    query = db.query(ArticleModel).filter(
        ArticleModel.title.contains(q) | ArticleModel.content.contains(q)
    )
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    articles = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return ResponseModel(data={
        "items": articles,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        }
    })


@router.get("/{article_id}", response_model=ResponseModel[ArticleDetail])
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """获取文章详情"""
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 增加阅读计数
    article.read_count += 1
    db.commit()
    
    return ResponseModel(data=article)


@router.get("/{article_id}/knowledge", response_model=ResponseModel[List[dict]])
async def get_article_knowledge(
    article_id: int,
    db: Session = Depends(get_db)
):
    """获取文章知识点"""
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    knowledge_points = [
        {
            "id": kp.id,
            "type": kp.type,
            "content": kp.content,
            "explanation": kp.explanation,
            "position_start": kp.position_start,
            "position_end": kp.position_end
        }
        for kp in article.knowledge_points
    ]
    
    return ResponseModel(data=knowledge_points)
