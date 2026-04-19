from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models import ProcessingStatus


# Base schemas
class ProcessingBase(BaseModel):
    file_name: str
    language: Optional[str] = None


class ProcessingCreate(ProcessingBase):
    file_path: str


class ProcessingUpdate(BaseModel):
    status: Optional[ProcessingStatus] = None
    transcript: Optional[str] = None
    extracted_text: Optional[str] = None
    duration: Optional[float] = None
    confidence: Optional[float] = None
    error_message: Optional[str] = None


# Voice Processing schemas
class VoiceProcessingBase(ProcessingBase):
    pass


class VoiceProcessingCreate(ProcessingCreate):
    pass


class VoiceProcessingResponse(ProcessingBase):
    id: int
    file_path: str
    status: ProcessingStatus
    transcript: Optional[str] = None
    duration: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VoiceProcessingListResponse(BaseModel):
    total: int
    items: List[VoiceProcessingResponse]


# Document OCR schemas
class DocumentOCRBase(ProcessingBase):
    pass


class DocumentOCRCreate(ProcessingCreate):
    pass


class DocumentOCRResponse(ProcessingBase):
    id: int
    file_path: str
    status: ProcessingStatus
    extracted_text: Optional[str] = None
    confidence: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentOCRListResponse(BaseModel):
    total: int
    items: List[DocumentOCRResponse]


# Health check schema
class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    whisper_model: str
    ocr_languages: str