from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class KnowledgePointBase(BaseModel):
    article_id: int
    type: str  # vocab, background, analysis
    content: str
    explanation: Optional[str] = None
    position_start: Optional[int] = None
    position_end: Optional[int] = None


class KnowledgePointCreate(KnowledgePointBase):
    pass


class KnowledgePoint(KnowledgePointBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
