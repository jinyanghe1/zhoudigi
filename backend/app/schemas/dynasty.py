from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DynastyBase(BaseModel):
    name: str
    period: Optional[str] = None
    description: Optional[str] = None


class DynastyCreate(DynastyBase):
    pass


class Dynasty(DynastyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
