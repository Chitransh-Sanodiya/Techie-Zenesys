from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    document_type = Column(String(50))
    file_path = Column(String(500))
    status = Column(String(50), default="PROCESSING")
    extracted_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())