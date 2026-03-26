from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    content = Column(Text, nullable=False)
    translation = Column(Text)
    dynasty_id = Column(Integer, ForeignKey("dynasties.id"))
    category = Column(String(50))
    source = Column(String(200))
    is_selected = Column(Boolean, default=False)
    selection_reason = Column(Text)
    read_count = Column(Integer, default=0)
    word_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    author = relationship("Author", back_populates="articles")
    dynasty = relationship("Dynasty", back_populates="articles")
    knowledge_points = relationship("KnowledgePoint", back_populates="article")
    tags = relationship("Tag", secondary="article_tag", back_populates="articles")


# Dynasty 反向关系
from app.models.dynasty import Dynasty
Dynasty.articles = relationship("Article", back_populates="dynasty")
