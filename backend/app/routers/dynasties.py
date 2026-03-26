from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ResponseModel, Dynasty, Author
from app.models import Dynasty as DynastyModel, Author as AuthorModel

router = APIRouter()


@router.get("", response_model=ResponseModel[List[Dynasty]])
async def get_dynasties(db: Session = Depends(get_db)):
    """获取所有朝代"""
    dynasties = db.query(DynastyModel).order_by(DynastyModel.id).all()
    return ResponseModel(data=dynasties)


@router.get("/{dynasty_id}", response_model=ResponseModel[Dynasty])
async def get_dynasty(
    dynasty_id: int,
    db: Session = Depends(get_db)
):
    """获取朝代详情"""
    dynasty = db.query(DynastyModel).filter(DynastyModel.id == dynasty_id).first()
    if not dynasty:
        raise HTTPException(status_code=404, detail="朝代不存在")
    return ResponseModel(data=dynasty)


@router.get("/{dynasty_id}/authors", response_model=ResponseModel[List[Author]])
async def get_dynasty_authors(
    dynasty_id: int,
    db: Session = Depends(get_db)
):
    """获取朝代下的作者"""
    dynasty = db.query(DynastyModel).filter(DynastyModel.id == dynasty_id).first()
    if not dynasty:
        raise HTTPException(status_code=404, detail="朝代不存在")
    
    authors = db.query(AuthorModel).filter(AuthorModel.dynasty_id == dynasty_id).all()
    return ResponseModel(data=authors)
