from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import voice_router, document_router
from app.schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Cleanup resources (if needed)
    pass


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Voice SaaS MVP - Voice-to-text and OCR processing API",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(voice_router)
app.include_router(document_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint returning basic info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs_url": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        System health status including database and AI model info
    """
    # Check database connectivity
    db_status = "healthy"
    try:
        from app.database import engine
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
    except Exception:
        db_status = "unhealthy"

    return HealthResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        version=settings.app_version,
        database=db_status,
        whisper_model=settings.whisper_model,
        ocr_languages=settings.ocr_languages
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )