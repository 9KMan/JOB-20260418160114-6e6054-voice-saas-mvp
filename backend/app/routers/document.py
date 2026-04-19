import os
import uuid
import aiofiles
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models import DocumentOCR, ProcessingStatus
from app.schemas import DocumentOCRResponse, DocumentOCRListResponse
from app.services.ocr_service import OCRService

router = APIRouter(prefix="/document", tags=["document"])


# Temporary directory for document uploads
TEMP_DOC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp", "documents")
os.makedirs(TEMP_DOC_DIR, exist_ok=True)


@router.post("/ocr", response_model=DocumentOCRResponse)
async def extract_text_from_document(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Extract text from a document/image using EasyOCR.

    Args:
        file: Image/document file (jpg, png, pdf, etc.)
        language: Optional language code (e.g., 'en', 'ch_sim', 'jpn')
        db: Database session

    Returns:
        Processing record with extracted text
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {', '.join(allowed_types)}"
        )

    # Generate unique file path
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(TEMP_DOC_DIR, unique_filename)

    # Save file temporarily
    try:
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create database record
    processing_record = DocumentOCR(
        file_name=file.filename or unique_filename,
        file_path=file_path,
        language=language,
        status=ProcessingStatus.PENDING
    )
    db.add(processing_record)
    await db.flush()

    try:
        # Update status to processing
        processing_record.status = ProcessingStatus.PROCESSING
        await db.flush()

        # Extract text using OCR
        result = await OCRService.extract_text_from_image(file_path)

        # Update record with results
        processing_record.extracted_text = result["text"]
        processing_record.confidence = result["confidence"]
        processing_record.status = ProcessingStatus.COMPLETED
        await db.flush()

        return processing_record

    except Exception as e:
        # Handle failure
        processing_record.status = ProcessingStatus.FAILED
        processing_record.error_message = str(e)
        await db.flush()
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

    finally:
        # Clean up temp file (optional, can keep for debugging)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass


@router.get("/processing/{record_id}", response_model=DocumentOCRResponse)
async def get_ocr_record(
    record_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific document OCR record by ID."""
    from sqlalchemy import select
    result = await db.execute(
        select(DocumentOCR).where(DocumentOCR.id == record_id)
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record


@router.get("/processing", response_model=DocumentOCRListResponse)
async def list_ocr_records(
    limit: int = 50,
    offset: int = 0,
    status: Optional[ProcessingStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all document OCR records with pagination."""
    from sqlalchemy import select, func

    query = select(DocumentOCR)
    count_query = select(func.count(DocumentOCR.id))

    if status:
        query = query.where(DocumentOCR.status == status)
        count_query = count_query.where(DocumentOCR.status == status)

    query = query.order_by(DocumentOCR.created_at.desc()).limit(limit).offset(offset)

    result = await db.execute(query)
    records = result.scalars().all()

    count_result = await db.execute(count_query)
    total = count_result.scalar()

    return DocumentOCRListResponse(total=total, items=records)