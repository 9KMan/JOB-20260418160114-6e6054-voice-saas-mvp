import os
import uuid
import aiofiles
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models import VoiceProcessing, ProcessingStatus
from app.schemas import VoiceProcessingResponse, VoiceProcessingListResponse
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["voice"])


# Temporary directory for audio uploads
TEMP_AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp", "audio")
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)


@router.post("/transcribe", response_model=VoiceProcessingResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Transcribe an audio file to text using Whisper AI.

    Args:
        file: Audio file (mp3, wav, m4a, etc.)
        language: Optional language code (e.g., 'en', 'zh', 'ja')
        db: Database session

    Returns:
        Processing record with transcript
    """
    # Validate file type
    allowed_types = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a", "audio/m4a"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {', '.join(allowed_types)}"
        )

    # Generate unique file path
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".mp3"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(TEMP_AUDIO_DIR, unique_filename)

    # Save file temporarily
    try:
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create database record
    processing_record = VoiceProcessing(
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

        # Transcribe audio
        result = await VoiceService.transcribe_audio(file_path, language)

        # Update record with results
        processing_record.transcript = result["transcript"]
        processing_record.duration = result.get("duration")
        processing_record.status = ProcessingStatus.COMPLETED
        await db.flush()

        return processing_record

    except Exception as e:
        # Handle failure
        processing_record.status = ProcessingStatus.FAILED
        processing_record.error_message = str(e)
        await db.flush()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    finally:
        # Clean up temp file (optional, can keep for debugging)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass


@router.get("/processing/{record_id}", response_model=VoiceProcessingResponse)
async def get_processing_record(
    record_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific voice processing record by ID."""
    from sqlalchemy import select
    result = await db.execute(
        select(VoiceProcessing).where(VoiceProcessing.id == record_id)
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record


@router.get("/processing", response_model=VoiceProcessingListResponse)
async def list_processing_records(
    limit: int = 50,
    offset: int = 0,
    status: Optional[ProcessingStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all voice processing records with pagination."""
    from sqlalchemy import select, func

    query = select(VoiceProcessing)
    count_query = select(func.count(VoiceProcessing.id))

    if status:
        query = query.where(VoiceProcessing.status == status)
        count_query = count_query.where(VoiceProcessing.status == status)

    query = query.order_by(VoiceProcessing.created_at.desc()).limit(limit).offset(offset)

    result = await db.execute(query)
    records = result.scalars().all()

    count_result = await db.execute(count_query)
    total = count_result.scalar()

    return VoiceProcessingListResponse(total=total, items=records)