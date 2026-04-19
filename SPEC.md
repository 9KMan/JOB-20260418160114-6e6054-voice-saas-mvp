# Voice SaaS MVP — Specification

## Overview

AI-powered voice and document processing SaaS platform. Phase 1 MVP with voice/chat input, document OCR, structured data storage, and financial tracking.

## Tech Stack

| Layer   | Technology                          |
|---------|-------------------------------------|
| Frontend | Next.js 14, React, Tailwind CSS, TypeScript |
| Backend  | FastAPI (Python), SQLite           |
| AI/ML    | Whisper (voice), OCR (document)    |

## Features

### Voice Processing
- Voice upload with AI transcription
- Chat-based text input alternative
- Real-time processing status

### Document Processing
- Document upload (receipts, PDFs, images)
- OCR and data extraction
- Structured data output

### Financial Tracking
- Spreadsheet-style data storage
- Basic financial calculations
- Structured record management

### UI/UX
- Modern dark-themed interface
- Real-time results display
- Progress indicators

## Architecture

```
frontend/          Next.js 14 web app
  app/             App router pages
  components/      React components
  lib/             Utilities

backend/           FastAPI Python server
  app/
    routers/       API endpoints (document, voice)
    services/      Business logic (ocr, voice)
    models.py      Data models
    schemas.py     Pydantic schemas
  main.py          FastAPI app entry
```

## API Endpoints

| Method | Path               | Description              |
|--------|--------------------|--------------------------|
| POST   | /api/voice/transcribe | Transcribe voice file   |
| POST   | /api/document/ocr    | OCR document upload     |

## Setup

```bash
# Backend
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
cp .env.example .env.local
npm install
npm run dev
```
