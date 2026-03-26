from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

from app.schemas import ResponseModel
from app.services import WikisourceService

router = APIRouter()
wikisource_service = WikisourceService()


class ImportRequest(BaseModel):
    title: str
    author: str = ""
    dynasty: str = ""
    category: str = ""


@router.get("/wikisource")
async def search_wikisource(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50)
):
    """搜索维基文库"""
    results = await wikisource_service.search(q, limit)
    return ResponseModel(data=results)


@router.get("/wikisource/{title:path}")
async def get_wikisource_content(title: str):
    """获取维基文库页面内容"""
    content = await wikisource_service.get_content(title)
    if not content.get("content"):
        raise HTTPException(status_code=404, detail="未找到该页面内容")
    return ResponseModel(data=content)


@router.post("/wikisource/import")
async def import_from_wikisource(request: ImportRequest):
    """从维基文库导入文章到本地库"""
    from sqlalchemy.orm import Session
    from fastapi import Depends
    from app.database import get_db, SessionLocal
    from app.models import Article as ArticleModel, Author as AuthorModel, Dynasty as DynastyModel

    content_data = await wikisource_service.get_content(request.title)
    if not content_data.get("content"):
        raise HTTPException(status_code=404, detail="无法从维基文库获取内容")

    db = SessionLocal()
    try:
        # 检查是否已导入
        existing = db.query(ArticleModel).filter(ArticleModel.title == request.title).first()
        if existing:
            raise HTTPException(status_code=409, detail="文章已存在")

        # 查找或创建朝代
        dynasty_id = None
        if request.dynasty:
            dynasty = db.query(DynastyModel).filter(DynastyModel.name == request.dynasty).first()
            if dynasty:
                dynasty_id = dynasty.id

        # 查找或创建作者
        author_id = None
        if request.author:
            author = db.query(AuthorModel).filter(AuthorModel.name == request.author).first()
            if not author:
                author = AuthorModel(name=request.author, dynasty_id=dynasty_id)
                db.add(author)
                db.flush()
            author_id = author.id

        article = ArticleModel(
            title=request.title,
            content=content_data["content"],
            author_id=author_id,
            dynasty_id=dynasty_id,
            category=request.category,
            source=content_data.get("url", ""),
            word_count=len(content_data["content"])
        )
        db.add(article)
        db.commit()
        db.refresh(article)

        return ResponseModel(data={
            "id": article.id,
            "title": article.title,
            "word_count": article.word_count,
            "message": "导入成功"
        })
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")
    finally:
        db.close()
