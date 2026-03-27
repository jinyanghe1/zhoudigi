from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.dependencies import get_user_id
from app.schemas import ResponseModel
from app.models import AIChatSession as SessionModel, AIChatMessage as MessageModel, Article as ArticleModel
from app.services import MinimaxService

router = APIRouter()
minimax_service = MinimaxService()


# Schemas
class ChatMessageCreate(BaseModel):
    content: str
    selected_text: Optional[str] = None
    selected_text_context: Optional[str] = None


class ChatSessionCreate(BaseModel):
    session_type: str = "general"  # general, article, reading
    article_id: Optional[int] = None
    title: Optional[str] = None


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    selected_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionOut(BaseModel):
    id: int
    session_type: str
    article_id: Optional[int]
    title: Optional[str]
    message_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/sessions", response_model=ResponseModel[List[ChatSessionOut]])
async def get_chat_sessions(
    session_type: Optional[str] = None,
    article_id: Optional[int] = None,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """获取用户的 AI 对话会话列表"""
    query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
    
    if session_type:
        query = query.filter(SessionModel.session_type == session_type)
    if article_id is not None:
        query = query.filter(SessionModel.article_id == article_id)
    
    sessions = query.order_by(SessionModel.updated_at.desc()).all()
    
    return ResponseModel(data=sessions)


@router.get("/article-session", response_model=ResponseModel[ChatSessionOut])
async def get_or_create_article_session(
    article_id: int = Query(..., ge=1),
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """获取当前用户在指定文章下的持久化问答会话，不存在则创建。"""
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    session = db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.session_type == "reading",
        SessionModel.article_id == article_id,
    ).order_by(SessionModel.updated_at.desc()).first()

    if session:
        return ResponseModel(data=session)

    session = SessionModel(
        user_id=user_id,
        session_type="reading",
        article_id=article_id,
        title=f"《{article.title}》问AI",
        meta={
            "article_title": article.title,
            "author_name": article.author.name if article.author else None,
            "dynasty_name": article.dynasty.name if article.dynasty else None,
        },
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return ResponseModel(data=session)


@router.post("/sessions", response_model=ResponseModel[ChatSessionOut])
async def create_chat_session(
    session: ChatSessionCreate,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """创建新的 AI 对话会话"""
    # 如果有关联文章，获取文章信息
    article_title = None
    if session.article_id:
        article = db.query(ArticleModel).filter(ArticleModel.id == session.article_id).first()
        if article:
            article_title = article.title
    
    # 生成标题
    title = session.title or f"新对话 {len(db.query(SessionModel).filter(SessionModel.user_id == user_id).all()) + 1}"
    if article_title and not session.title:
        title = f"关于《{article_title}》的讨论"
    
    db_session = SessionModel(
        user_id=user_id,
        session_type=session.session_type,
        article_id=session.article_id,
        title=title,
        meta={"article_title": article_title} if article_title else {}
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return ResponseModel(data=db_session)


@router.get("/sessions/{session_id}", response_model=ResponseModel[ChatSessionOut])
async def get_chat_session(
    session_id: int,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """获取会话详情"""
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return ResponseModel(data=session)


@router.delete("/sessions/{session_id}", response_model=ResponseModel[dict])
async def delete_chat_session(
    session_id: int,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """删除会话"""
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    db.delete(session)
    db.commit()
    
    return ResponseModel(data={"message": "删除成功"})


@router.get("/sessions/{session_id}/messages", response_model=ResponseModel[List[ChatMessageOut]])
async def get_chat_messages(
    session_id: int,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """获取会话的消息列表"""
    # 验证会话归属
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    messages = db.query(MessageModel).filter(
        MessageModel.session_id == session_id
    ).order_by(MessageModel.created_at.asc()).all()
    
    return ResponseModel(data=messages)


@router.post("/sessions/{session_id}/messages", response_model=ResponseModel[List[ChatMessageOut]])
async def send_message(
    session_id: int,
    message: ChatMessageCreate,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """发送消息并获取 AI 回复"""
    # 验证会话
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 保存用户消息
    user_msg = MessageModel(
        session_id=session_id,
        role="user",
        content=message.content,
        selected_text=message.selected_text,
        selected_text_context=message.selected_text_context
    )
    db.add(user_msg)
    
    article = None
    if session.article_id:
        article = db.query(ArticleModel).filter(ArticleModel.id == session.article_id).first()

    # 构建 AI 提示
    system_prompt = """你是一位精通中国古典文学的专家。你的任务是帮助用户理解古文，回答他们的问题。

请遵循以下原则：
1. 解释要准确、清晰，适合古文学习者理解
2. 对于词语解释，提供拼音、释义和用法
3. 对于句子翻译，既要忠实原文，又要符合现代汉语表达习惯
4. 适当补充文化背景和历史典故
5. 保持谦逊友好的态度"""

    if article:
        article_context = f"""当前讨论文章信息：
标题：{article.title}
作者：{article.author.name if article.author else "未知"}
朝代：{article.dynasty.name if article.dynasty else "未知"}

请优先结合以下原文回答问题：
{article.content[:4000]}"""
    else:
        article_context = ""

    # 获取历史消息（最近10条）
    history = db.query(MessageModel).filter(
        MessageModel.session_id == session_id
    ).order_by(MessageModel.created_at.desc()).limit(10).all()
    
    messages = [{"role": "system", "content": system_prompt}]
    if article_context:
        messages.append({"role": "system", "content": article_context})
    
    # 添加选中文本信息
    if message.selected_text:
        context_info = f"\n\n用户正在阅读的原文：{message.selected_text}"
        if message.selected_text_context:
            context_info += f"\n上下文：{message.selected_text_context}"
        messages.append({"role": "system", "content": context_info})
    
    # 添加历史消息
    for h in reversed(history):
        messages.append({"role": h.role, "content": h.content})
    
    # 添加当前消息
    messages.append({"role": "user", "content": message.content})
    
    # 调用 AI
    ai_response = await minimax_service.chat(messages, temperature=0.7)
    
    # 保存 AI 回复
    assistant_msg = MessageModel(
        session_id=session_id,
        role="assistant",
        content=ai_response,
        meta={"has_context": bool(message.selected_text)}
    )
    db.add(assistant_msg)
    
    # 更新会话消息数
    session.message_count = db.query(MessageModel).filter(
        MessageModel.session_id == session_id
    ).count() + 2
    
    db.commit()
    db.refresh(user_msg)
    db.refresh(assistant_msg)
    
    return ResponseModel(data=[user_msg, assistant_msg])


@router.post("/quick-ask", response_model=ResponseModel[dict])
async def quick_ask(
    question: str,
    article_id: Optional[int] = None,
    selected_text: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """快速提问（不保存会话）"""
    system_prompt = """你是一位精通中国古典文学的专家。请简洁地回答用户的问题。"""
    
    messages = [{"role": "system", "content": system_prompt}]
    
    if selected_text:
        context = f"用户选中文字：{selected_text}\n\n问题：{question}"
        messages.append({"role": "user", "content": context})
    else:
        messages.append({"role": "user", "content": question})
    
    response = await minimax_service.chat(messages, temperature=0.7)
    
    return ResponseModel(data={
        "answer": response,
        "selected_text": selected_text
    })
