from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.dependencies import get_user_id
from app.schemas import ResponseModel, ListResponse
from app.models import Vocabulary as VocabularyModel, Article as ArticleModel
from app.services import MinimaxService

router = APIRouter()


# Schemas
class VocabularyCreate(BaseModel):
    word: str
    pinyin: Optional[str] = None
    explanation: str
    source_text: Optional[str] = None
    article_id: int


class VocabularyUpdate(BaseModel):
    pinyin: Optional[str] = None
    explanation: Optional[str] = None
    mastery_level: Optional[int] = None


class VocabularyOut(BaseModel):
    id: int
    word: str
    pinyin: Optional[str]
    explanation: str
    source_text: Optional[str]
    article_id: int
    article_title: Optional[str]
    dynasty_name: Optional[str]
    mastery_level: int
    review_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExplainTextRequest(BaseModel):
    text: str
    context: Optional[str] = None


class ExplainResult(BaseModel):
    pinyin: str = ""
    explanation: str
    translation: str = ""
    background: str = ""


@router.get("", response_model=ResponseModel[ListResponse[VocabularyOut]])
async def get_vocabularies(
    article_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """获取生词列表"""
    query = db.query(VocabularyModel).filter(VocabularyModel.user_id == user_id)
    
    if article_id:
        query = query.filter(VocabularyModel.article_id == article_id)
    
    total = query.count()
    items = query.order_by(VocabularyModel.created_at.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()
    
    return ResponseModel(data={
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }
    })


@router.post("", response_model=ResponseModel[VocabularyOut])
async def create_vocabulary(
    vocab: VocabularyCreate,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """添加生词"""
    # 检查文章是否存在
    article = db.query(ArticleModel).filter(ArticleModel.id == vocab.article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 检查是否已存在
    existing = db.query(VocabularyModel).filter(
        VocabularyModel.user_id == user_id,
        VocabularyModel.word == vocab.word,
        VocabularyModel.article_id == vocab.article_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="该生词已存在")
    
    # 创建生词
    db_vocab = VocabularyModel(
        user_id=user_id,
        word=vocab.word,
        pinyin=vocab.pinyin,
        explanation=vocab.explanation,
        source_text=vocab.source_text,
        article_id=vocab.article_id,
        article_title=article.title,
        dynasty_name=article.dynasty.name if article.dynasty else None
    )
    
    db.add(db_vocab)
    db.commit()
    db.refresh(db_vocab)
    
    return ResponseModel(data=db_vocab)


@router.get("/{vocab_id}", response_model=ResponseModel[VocabularyOut])
async def get_vocabulary(
    vocab_id: int,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """获取单个生词详情"""
    vocab = db.query(VocabularyModel).filter(
        VocabularyModel.id == vocab_id,
        VocabularyModel.user_id == user_id
    ).first()
    
    if not vocab:
        raise HTTPException(status_code=404, detail="生词不存在")
    
    return ResponseModel(data=vocab)


@router.put("/{vocab_id}", response_model=ResponseModel[VocabularyOut])
async def update_vocabulary(
    vocab_id: int,
    update: VocabularyUpdate,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """更新生词"""
    vocab = db.query(VocabularyModel).filter(
        VocabularyModel.id == vocab_id,
        VocabularyModel.user_id == user_id
    ).first()
    
    if not vocab:
        raise HTTPException(status_code=404, detail="生词不存在")
    
    # 更新字段
    if update.pinyin is not None:
        vocab.pinyin = update.pinyin
    if update.explanation is not None:
        vocab.explanation = update.explanation
    if update.mastery_level is not None:
        if update.mastery_level > vocab.mastery_level:
            vocab.review_count += 1
        vocab.mastery_level = update.mastery_level
    
    db.commit()
    db.refresh(vocab)
    
    return ResponseModel(data=vocab)


@router.delete("/{vocab_id}", response_model=ResponseModel[dict])
async def delete_vocabulary(
    vocab_id: int,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """删除生词"""
    vocab = db.query(VocabularyModel).filter(
        VocabularyModel.id == vocab_id,
        VocabularyModel.user_id == user_id
    ).first()
    
    if not vocab:
        raise HTTPException(status_code=404, detail="生词不存在")
    
    db.delete(vocab)
    db.commit()
    
    return ResponseModel(data={"message": "删除成功"})


@router.post("/{vocab_id}/review", response_model=ResponseModel[VocabularyOut])
async def review_vocabulary(
    vocab_id: int,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """复习生词（增加复习次数）"""
    vocab = db.query(VocabularyModel).filter(
        VocabularyModel.id == vocab_id,
        VocabularyModel.user_id == user_id
    ).first()
    
    if not vocab:
        raise HTTPException(status_code=404, detail="生词不存在")
    
    vocab.review_count += 1
    db.commit()
    db.refresh(vocab)
    
    return ResponseModel(data=vocab)


@router.post("/explain", response_model=ResponseModel[ExplainResult])
async def explain_text(
    request: ExplainTextRequest,
):
    """使用 AI 解释选中的文本"""
    minimax = MinimaxService()
    
    prompt = f"""请解释以下古文词语或句子的含义。

文本: {request.text}
{f"上下文: {request.context}" if request.context else ""}

请提供:
1. 拼音标注
2. 字词释义
3. 整句翻译
4. 文化背景（如有典故）

以 JSON 格式返回:
{{
    "pinyin": "拼音",
    "explanation": "详细解释",
    "translation": "现代译文",
    "background": "背景知识（可选）"
}}"""

    messages = [{"role": "user", "content": prompt}]
    response = await minimax.chat(messages, temperature=0.3)
    
    # 尝试解析 JSON
    import json
    try:
        result = json.loads(response)
    except Exception:
        result = {
            "pinyin": "",
            "explanation": response,
            "translation": "",
            "background": ""
        }
    
    return ResponseModel(data=result)
