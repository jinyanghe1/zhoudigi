from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class AIChatSession(Base):
    """AI 对话会话模型"""
    __tablename__ = "ai_chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="anonymous")
    session_type = Column(String(50), default="general")  # general, article, reading
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)  # 关联文章（可选）
    title = Column(String(200))  # 会话标题
    
    # 会话元数据
    meta = Column("metadata", JSON, default=dict)  # 存储额外信息如文章标题、阅读位置等
    
    # 统计
    message_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    messages = relationship("AIChatMessage", back_populates="session", cascade="all, delete-orphan")
    article = relationship("Article", back_populates="chat_sessions")
    
    __table_args__ = (
        Index('idx_user_type', 'user_id', 'session_type'),
    )


class AIChatMessage(Base):
    """AI 对话消息模型"""
    __tablename__ = "ai_chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("ai_chat_sessions.id"), nullable=False)
    
    # 消息内容
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    
    # 消息元数据（如引用的原文、生成的解释等）
    meta = Column("metadata", JSON, default=dict)
    
    # 选中的文本（如果是阅读时提问）
    selected_text = Column(Text)
    selected_text_context = Column(Text)  # 选中文字的上下文
    
    # Token 统计（如果有）
    tokens_used = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    session = relationship("AIChatSession", back_populates="messages")
    
    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
    )


# Article 反向关系
from app.models.article import Article
Article.chat_sessions = relationship("AIChatSession", back_populates="article")
