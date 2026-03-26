from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    dynasty_id = Column(Integer, ForeignKey("dynasties.id"))
    bio = Column(Text)
    literary_group = Column(String(50))
    style = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    dynasty = relationship("Dynasty", back_populates="authors")
    articles = relationship("Article", back_populates="author")


# Dynasty 反向关系
from app.models.dynasty import Dynasty
Dynasty.authors = relationship("Author", back_populates="dynasty")
