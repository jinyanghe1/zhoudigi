from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.schemas.dynasty import Dynasty


class AuthorBase(BaseModel):
    name: str
    dynasty_id: Optional[int] = None
    bio: Optional[str] = None
    literary_group: Optional[str] = None
    style: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuthorWithDynasty(Author):
    dynasty: Optional[Dynasty] = None
