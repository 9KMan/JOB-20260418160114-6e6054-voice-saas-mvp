# Voice SaaS MVP

AI-powered voice and document processing platform.

## Stack

- **Frontend**: Next.js 14 + Tailwind CSS + TypeScript
- **Backend**: FastAPI (Python) + SQLite

## Setup

```bash
# Backend
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

## Features

- Voice upload with AI transcription
- Document upload with OCR processing
- Real-time results display
- Modern dark-themed UI
