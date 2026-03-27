from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Vocabulary(Base):
    """生词表模型"""
    __tablename__ = "vocabularies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="anonymous")  # 用户标识，支持多用户
    word = Column(String(200), nullable=False)  # 生词/句子
    pinyin = Column(String(200))  # 拼音
    explanation = Column(Text, nullable=False)  # 释义
    source_text = Column(Text)  # 原文上下文
    article_id = Column(Integer, ForeignKey("articles.id"))  # 来源文章
    article_title = Column(String(200))  # 文章标题（冗余存储，方便展示）
    dynasty_name = Column(String(50))  # 朝代名称
    
    # 学习状态
    mastery_level = Column(Integer, default=0)  # 掌握程度 0-5
    review_count = Column(Integer, default=0)  # 复习次数
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 复合索引，支持按用户和文章查询
    __table_args__ = (
        Index('idx_user_article', 'user_id', 'article_id'),
        Index('idx_user_word', 'user_id', 'word'),
    )
    
    # 关系
    article = relationship("Article", back_populates="vocabularies")


# Article 反向关系
from app.models.article import Article
Article.vocabularies = relationship("Vocabulary", back_populates="article")
