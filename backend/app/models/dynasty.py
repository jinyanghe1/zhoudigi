from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Dynasty(Base):
    __tablename__ = "dynasties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, index=True)
    period = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
