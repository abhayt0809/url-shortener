from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    code = Column(String(32), unique=True, index=True)
    original_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    clicks = Column(Integer, default=0)