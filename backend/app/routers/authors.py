from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ResponseModel, ListResponse, AuthorWithDynasty, Article
from app.models import Author as AuthorModel, Article as ArticleModel

router = APIRouter()


@router.get("", response_model=ResponseModel[ListResponse[AuthorWithDynasty]])
async def get_authors(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    dynasty_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取作者列表"""
    query = db.query(AuthorModel)
    
    if dynasty_id:
        query = query.filter(AuthorModel.dynasty_id == dynasty_id)
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    authors = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return ResponseModel(data={
        "items": authors,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        }
    })


@router.get("/{author_id}", response_model=ResponseModel[AuthorWithDynasty])
async def get_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    """获取作者详情"""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="作者不存在")
    return ResponseModel(data=author)


@router.get("/{author_id}/articles", response_model=ResponseModel[List[Article]])
async def get_author_articles(
    author_id: int,
    db: Session = Depends(get_db)
):
    """获取作者的文章"""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="作者不存在")
    
    articles = db.query(ArticleModel).filter(ArticleModel.author_id == author_id).all()
    return ResponseModel(data=articles)
