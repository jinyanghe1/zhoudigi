from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    type = Column(String(20))  # vocab, background, analysis
    content = Column(Text, nullable=False)
    explanation = Column(Text)
    position_start = Column(Integer)
    position_end = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    article = relationship("Article", back_populates="knowledge_points")
