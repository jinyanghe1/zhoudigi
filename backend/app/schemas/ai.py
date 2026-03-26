from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    """AI 对话请求"""
    messages: List[Dict[str, str]]
    temperature: Optional[float] = 0.7


class TranslateRequest(BaseModel):
    """翻译请求"""
    text: str


class ExplainRequest(BaseModel):
    """解释请求"""
    text: str
    context: Optional[str] = None


class SelectArticlesRequest(BaseModel):
    """AI 选文请求"""
    user_input: str


class ArticleRecommendation(BaseModel):
    """文章推荐"""
    article_index: int
    reason: str


class SelectArticlesResponse(BaseModel):
    """AI 选文响应"""
    recommendations: List[ArticleRecommendation]
    summary: str
    raw_response: Optional[str] = None


class GenerateKnowledgeRequest(BaseModel):
    """生成知识点请求"""
    article_id: int
