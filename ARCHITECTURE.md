# DrDejaVu - Architecture & Implementation Plan

## 1. Development & Testing Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ / npm 9+
- Docker & Docker Compose (optional, for containerized setup)
- Eigen AI API key (from https://app.eigenai.com)

### Quick Start (Local Development)
```bash
# Clone and enter project
cd DrDejaVu

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate        # Linux/Mac
pip install -r requirements.txt
cp .env.example .env            # Edit with your API keys
uvicorn app.main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
cp .env.example .env            # Edit API URL if needed
npm run dev                     # Runs on http://localhost:5173
```

### Docker Setup (Recommended)
```bash
cp .env.example .env            # Edit with your API keys
docker-compose up --build       # Frontend: :5173, Backend: :8000
```

### Testing
```bash
# Backend tests
cd backend && pytest tests/ -v

# Frontend tests
cd frontend && npm test
```

---

## 2. Eigen AI Model Integration

### Models Used

| Model | Eigen AI URL | Purpose | Integration Point |
|-------|-------------|---------|-------------------|
| **Higgs ASR V3.0** | https://app.eigenai.com/model-library/higgs_asr_3 | Speech-to-Text transcription | `POST /api/transcribe` |
| **Higgs Audio V2.5** | https://app.eigenai.com/model-library/higgs2p5 | Conversational voice AI + TTS | `POST /api/chat/voice` |
| **Higgs Audio Understanding V3.5** | Eigen AI Platform | Sentiment/tone analysis | `POST /api/analyze` |

### How to Access Eigen AI Models

1. **Sign up** at https://app.eigenai.com
2. **Navigate** to Model Library and enable the models above
3. **Get API Key** from your account dashboard
4. **Configure** in `.env`:
   ```
   EIGEN_API_KEY=your_api_key_here
   EIGEN_API_BASE_URL=https://api.eigenai.com/v1
   ```

### API Integration Pattern

All Eigen AI models are accessed via an **OpenAI-compatible API** hosted on the Eigen platform. The backend wraps these into application-specific endpoints:

```
Patient Voice → Backend /api/transcribe → Eigen Higgs ASR V3.0
                                              ↓
                              Transcribed text returned
                                              ↓
                Backend /api/query → ChromaDB RAG retrieval
                                              ↓
                              Context + query sent to LLM
                                              ↓
                Backend /api/chat/voice → Eigen Higgs V2.5 (TTS response)
                                              ↓
                              Audio response streamed to patient
```

---

## 3. Folder Structure

```
DrDejaVu/
├── README.md                        # Project overview
├── ARCHITECTURE.md                  # This file
├── docker-compose.yml               # Full-stack orchestration
├── .env.example                     # Environment template
│
├── backend/                         # FastAPI Python backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .env.example
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Settings & env vars
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── transcribe.py        # Audio upload & ASR endpoint
│   │   │   ├── query.py             # RAG query endpoint
│   │   │   ├── chat.py              # Voice chat endpoint
│   │   │   ├── consultations.py     # CRUD for consultation records
│   │   │   └── health.py            # Health check
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── eigen_asr.py         # Higgs ASR V3.0 client
│   │   │   ├── eigen_chat.py        # Higgs Audio V2.5 client
│   │   │   ├── eigen_analysis.py    # Higgs Understanding V3.5 client
│   │   │   ├── rag_engine.py        # ChromaDB RAG pipeline
│   │   │   └── summarizer.py        # LLM summarization (Llama/Qwen)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py           # Pydantic models
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── vector_store.py      # ChromaDB setup
│   │       └── sqlite_store.py      # SQLite for consultation metadata
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_transcribe.py
│       ├── test_query.py
│       └── test_consultations.py
│
├── frontend/                        # React + Vite + TypeScript
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── .env.example
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── main.tsx                 # App entry
│   │   ├── App.tsx                  # Root component + routing
│   │   ├── index.css                # Global styles
│   │   ├── components/
│   │   │   ├── VoiceRecorder.tsx    # Mic input + recording UI
│   │   │   ├── ChatWindow.tsx       # Message history display
│   │   │   ├── ConsultationList.tsx # Past consultations sidebar
│   │   │   ├── AudioPlayer.tsx      # Play AI voice responses
│   │   │   ├── UploadPanel.tsx      # Upload consultation audio
│   │   │   └── Timeline.tsx         # Health progress timeline
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx        # Main dashboard
│   │   │   ├── Upload.tsx           # Upload consultation page
│   │   │   └── History.tsx          # Consultation history page
│   │   ├── hooks/
│   │   │   ├── useVoiceRecorder.ts  # MediaRecorder hook
│   │   │   └── useApi.ts           # API call hook
│   │   ├── services/
│   │   │   └── api.ts              # Axios API client
│   │   └── types/
│   │       └── index.ts            # TypeScript types
│   └── tests/
│       └── App.test.tsx
│
└── data/                            # Local data (gitignored)
    ├── chroma_db/                   # ChromaDB persistence
    ├── uploads/                     # Uploaded audio files
    └── sample_audio/               # Sample audio for testing
```

---

## 4. Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────────┐  │
│  │  Voice   │  │  Upload  │  │  Chat     │  │  Timeline    │  │
│  │ Recorder │  │  Panel   │  │  Window   │  │  View        │  │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  └──────────────┘  │
│       │              │              │                            │
└───────┼──────────────┼──────────────┼────────────────────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │ /transcribe │  │ /consult     │  │ /query                │  │
│  │ (ASR)       │  │ (Upload)     │  │ (RAG + Voice Reply)   │  │
│  └──────┬──────┘  └──────┬───────┘  └───────────┬───────────┘  │
│         │                │                      │               │
│  ┌──────▼──────┐  ┌──────▼───────┐  ┌───────────▼───────────┐  │
│  │ Eigen ASR   │  │ Summarizer   │  │ RAG Engine            │  │
│  │ Service     │  │ Service      │  │ (ChromaDB + LLM)      │  │
│  └─────────────┘  └──────────────┘  └───────────┬───────────┘  │
│                                                 │               │
│                                      ┌──────────▼────────────┐  │
│                                      │ Eigen Chat Service    │  │
│                                      │ (Voice Response)      │  │
│                                      └───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
        │                │                      │
        ▼                ▼                      ▼
┌───────────────┐ ┌──────────────┐  ┌────────────────────────┐
│ Eigen AI API  │ │   SQLite     │  │      ChromaDB          │
│ (Higgs Suite) │ │ (Metadata)   │  │  (Vector Embeddings)   │
└───────────────┘ └──────────────┘  └────────────────────────┘
```

---

## 5. Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Vector DB | ChromaDB | Local, no infra needed, Python-native, great for hackathon |
| Backend | FastAPI | Async support, auto docs, fast prototyping |
| Frontend | React + Vite + TS | Fast builds, type safety, modern DX |
| Metadata DB | SQLite | Zero config, file-based, sufficient for prototype |
| Audio format | WAV/MP3/M4A | All supported by Higgs ASR V3.0 |
| API pattern | OpenAI-compatible | Eigen AI uses this standard, easy integration |
