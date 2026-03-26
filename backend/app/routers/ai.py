from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ResponseModel
from app.services import MinimaxService
from app.models import Article as ArticleModel

router = APIRouter()
minimax_service = MinimaxService()


class ChatRequest(BaseModel):
    messages: List[dict]
    temperature: Optional[float] = 0.7


class TranslateRequest(BaseModel):
    text: str


class ExplainRequest(BaseModel):
    text: str
    context: Optional[str] = None


class SelectArticlesRequest(BaseModel):
    user_input: str


@router.post("/chat", response_model=ResponseModel[str])
async def chat(
    request: ChatRequest
):
    """与 AI 对话"""
    response = await minimax_service.chat(
        messages=request.messages,
        temperature=request.temperature
    )
    return ResponseModel(data=response)


@router.post("/translate", response_model=ResponseModel[str])
async def translate(
    request: TranslateRequest
):
    """翻译古文"""
    response = await minimax_service.translate_text(request.text)
    return ResponseModel(data=response)


@router.post("/explain", response_model=ResponseModel[str])
async def explain(
    request: ExplainRequest
):
    """解释词语或句子"""
    context_text = f"上下文: {request.context}\n" if request.context else ""
    prompt = f"""请解释以下古文词语/句子的含义：

{context_text}需要解释的内容: {request.text}

请提供：
1. 字面意思
2. 深层含义
3. 相关典故（如有）"""

    messages = [{"role": "user", "content": prompt}]
    response = await minimax_service.chat(messages, temperature=0.3)
    return ResponseModel(data=response)


@router.post("/select-articles", response_model=ResponseModel[dict])
async def select_articles(
    request: SelectArticlesRequest,
    db: Session = Depends(get_db)
):
    """AI 推荐文章"""
    # 获取所有可选文章
    articles = db.query(ArticleModel).filter(ArticleModel.is_selected == True).all()
    
    if not articles:
        # 如果没有精选文章，获取所有文章
        articles = db.query(ArticleModel).limit(100).all()
    
    article_list = [
        {
            "id": a.id,
            "title": a.title,
            "author": a.author.name if a.author else "未知",
            "dynasty": a.dynasty.name if a.dynasty else "未知",
            "category": a.category
        }
        for a in articles
    ]
    
    result = await minimax_service.select_articles(
        user_input=request.user_input,
        article_list=article_list
    )
    
    return ResponseModel(data=result)


@router.post("/generate-knowledge/{article_id}", response_model=ResponseModel[List[dict]])
async def generate_knowledge(
    article_id: int,
    db: Session = Depends(get_db)
):
    """为文章生成知识点"""
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    points = await minimax_service.generate_knowledge_points(
        title=article.title,
        author=article.author.name if article.author else "未知",
        content=article.content
    )
    
    return ResponseModel(data=points)
