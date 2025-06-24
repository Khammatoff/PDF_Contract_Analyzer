from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from .database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    conditions = Column(JSON, nullable=False)
    parties = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
