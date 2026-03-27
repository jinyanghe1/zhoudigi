"""Vocabulary schema definitions"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class VocabularyBase(BaseModel):
    """Vocabulary base schema"""
    word: str
    pinyin: Optional[str] = None
    meaning: str
    source_text: Optional[str] = None
    article_id: Optional[int] = None


class VocabularyCreate(VocabularyBase):
    """Vocabulary create schema"""
    pass


class VocabularyUpdate(BaseModel):
    """Vocabulary update schema"""
    word: Optional[str] = None
    pinyin: Optional[str] = None
    meaning: Optional[str] = None
    source_text: Optional[str] = None
    mastery_level: Optional[int] = None


class Vocabulary(VocabularyBase):
    """Vocabulary response schema"""
    id: int
    mastery_level: int = 0
    review_count: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True
