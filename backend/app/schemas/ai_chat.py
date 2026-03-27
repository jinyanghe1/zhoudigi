"""AI Chat schema definitions"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AIChatMessageBase(BaseModel):
    """AI Chat Message base schema"""
    role: str
    content: str
    references: Optional[List[Dict[str, Any]]] = None


class AIChatMessageCreate(AIChatMessageBase):
    """AI Chat Message create schema"""
    session_id: int


class AIChatMessage(AIChatMessageBase):
    """AI Chat Message response schema"""
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AIChatSessionBase(BaseModel):
    """AI Chat Session base schema"""
    title: Optional[str] = None
    article_id: Optional[int] = None
    session_type: str = "general"


class AIChatSessionCreate(AIChatSessionBase):
    """AI Chat Session create schema"""
    pass


class AIChatSession(AIChatSessionBase):
    """AI Chat Session response schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[AIChatMessage] = []
    
    class Config:
        from_attributes = True


class ExplainTextRequest(BaseModel):
    """Text explanation request"""
    text: str
    context: Optional[str] = None
    article_id: Optional[int] = None
