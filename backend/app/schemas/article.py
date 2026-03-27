from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from app.schemas.author import AuthorWithDynasty
from app.schemas.dynasty import Dynasty
from app.schemas.knowledge_point import KnowledgePoint
from app.schemas.tag import Tag


class ArticleBase(BaseModel):
    title: str
    author_id: Optional[int] = None
    content: str
    translation: Optional[str] = None
    dynasty_id: Optional[int] = None
    category: Optional[str] = None
    source: Optional[str] = None
    is_selected: bool = False
    selection_reason: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    read_count: int
    word_count: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    author: Optional[AuthorWithDynasty] = None
    dynasty: Optional['Dynasty'] = None

    class Config:
        from_attributes = True


class ArticleDetail(Article):
    author: Optional[AuthorWithDynasty]
    knowledge_points: List[KnowledgePoint] = []
    tags: List[Tag] = []
