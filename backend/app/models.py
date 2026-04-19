from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Float
from sqlalchemy.sql import func

from app.database import Base
import enum


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VoiceProcessing(Base):
    """Model for voice processing records."""

    __tablename__ = "voice_processing"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    language = Column(String(10), nullable=True)
    status = Column(
        SQLEnum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False
    )
    transcript = Column(Text, nullable=True)
    duration = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DocumentOCR(Base):
    """Model for document OCR records."""

    __tablename__ = "document_ocr"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    language = Column(String(10), nullable=True)
    status = Column(
        SQLEnum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False
    )
    extracted_text = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())