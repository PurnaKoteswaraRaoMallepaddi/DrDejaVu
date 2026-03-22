<h1 align="center">DrDejaVu</h1>
<h3 align="center">Your AI Doctor's Memory That Listens, Remembers & Speaks Back</h3>
 
<p align="center">
  <b>Voice In. Perfect Memory. Voice Out — In Your Doctor's Own Voice.</b>
</p>
 
<p align="center">
  <img src="https://img.shields.io/badge/Eigen_AI-4_Models-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/React_18-TypeScript-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/FastAPI-Python-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/ChromaDB-RAG-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-One_Command-blue?style=for-the-badge" />
</p>
 
---
 
## The Problem
 
> **80% of medical information** given to patients is forgotten immediately. Half of what's remembered is remembered **incorrectly**.
 
Every patient knows the feeling: you walk out of a doctor's office and can't remember what they said. *Was my glucose 152 or 189? Did the doctor say cut salt or cut sugar? Which medication got reduced?*
 
Now make it worse — most patients see **multiple specialists**. An internist, a cardiologist, a nutritionist, an ophthalmologist. Each gives critical advice. **None of them know what the others said.** And the patient definitely can't remember it all.
 
This memory gap kills compliance, kills confidence, and kills health outcomes.
 
---
 
## The Solution
 
**DrDejaVu** is a voice-first AI health memory that:
 
1. **Listens** — Records and transcribes doctor-patient consultations from any specialist
2. **Remembers** — Indexes every word into a searchable vector database, organized by patient
3. **Speaks Back** — Answers patient questions by cross-referencing years of visits across multiple doctors, delivered as a voice response **cloned to sound like their own doctor**
 
One question. Multiple doctors. Multiple years. One precise answer — in seconds.
 
---
 
## Live Demo — Meet Ramesh

 
## What We Built
 
### Full-Stack Voice RAG Pipeline — 2,344 lines of code
 
```
                        DrDejaVu Architecture
 
    +---------------------------------------------------------+
    |                   FRONTEND (React 18 + TS)              |
    |  Dashboard (Voice Chat)  |  Upload  |  History Timeline |
    |  VoiceRecorder | ChatWindow | AudioPlayer | UploadPanel |
    +-----------------------+--+------------------------------+
                            |  Axios
                            v
    +---------------------------------------------------------+
    |                   BACKEND (FastAPI)                      |
    |                                                         |
    |  /api/transcribe --> ASR --> Summarize --> Index         |
    |  /api/chat/voice --> [Transcribe] --> RAG --> TTS        |
    |  /api/chat/text  --> RAG --> [TTS]                       |
    |  /api/query      --> RAG (text only)                     |
    |  /api/consultations --> Patient history                  |
    +---+-----------+-----------+-----------------------------+
        |           |           |
   +----v----+ +----v----+ +----v-----------+
   | ChromaDB| | SQLite  | | Eigen AI       |
   | Vectors | | Records | | 4 Models       |
   +---------+ +---------+ +----------------+
```
 
### Backend — 1,163 lines (Python / FastAPI)
 
| Module | Lines | What It Does |
|--------|-------|-------------|
| `services/eigen_chat.py` | 170 | Higgs Audio V2.5 TTS + gpt-oss-120b chat + voice-friendly text conversion |
| `services/rag_engine.py` | 113 | ChromaDB indexing, chunking at sentence boundaries, cosine similarity retrieval |
| `routers/transcribe.py` | 98 | Full transcription pipeline: ASR -> Summarize -> Index -> Save |
| `db/sqlite_store.py` | 83 | Patient consultation metadata storage |
| `services/eigen_asr.py` | 63 | Higgs ASR V3.0 speech-to-text client |
| `models/schemas.py` | 58 | Pydantic models for type-safe API |
| `routers/chat.py` | 57 | Voice & text chat endpoints with optional TTS |
| `services/summarizer.py` | 54 | Structured medical summary extraction via LLM |
| `services/eigen_analysis.py` | 46 | Higgs Audio Understanding V3.5 sentiment analysis |
| `routers/audio.py` | 39 | Secure audio file serving |
| `config.py` | 32 | Environment configuration |
| `db/vector_store.py` | 26 | ChromaDB client initialization (HNSW, cosine) |
| `tests/` | 221 | Unit tests for pipeline, RAG, voice conversion |
 
### Frontend — 1,181 lines (React 18 + TypeScript + Vite)
 
| Module | Lines | What It Does |
|--------|-------|-------------|
| `index.css` | 458 | Complete responsive UI styling |
| `pages/Dashboard.tsx` | 112 | Main chat interface — sidebar + message history + voice input |
| `services/api.ts` | 87 | Axios API client with typed endpoints |
| `components/UploadPanel.tsx` | 70 | Audio upload form with doctor name + date |
| `components/VoiceRecorder.tsx` | 59 | MediaRecorder API integration — record, preview, send |
| `components/ChatWindow.tsx` | 58 | Message display with timestamps, sources, audio player |
| `components/ConsultationList.tsx` | 46 | Sidebar showing all consultations per patient |
| `hooks/useVoiceRecorder.ts` | 47 | Custom hook for microphone lifecycle management |
| `types/index.ts` | 44 | TypeScript interfaces for full type safety |
| `pages/History.tsx` | 41 | Timeline visualization of health journey |
| `hooks/useApi.ts` | 38 | API state management hook |
| `components/Timeline.tsx` | 30 | Visual timeline component |
| `components/AudioPlayer.tsx` | 28 | HTML5 audio playback for TTS responses |
| `App.tsx` | 30 | React Router v7 with 3 routes |
| `pages/Upload.tsx` | 23 | Upload page layout |
 
### API Endpoints
 
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/transcribe` | Upload audio -> transcribe -> summarize -> index |
| `POST` | `/api/chat/voice` | Voice question -> ASR -> RAG -> TTS response |
| `POST` | `/api/chat/text` | Text question -> RAG -> optional TTS |
| `POST` | `/api/query` | RAG query (text-only response) |
| `GET` | `/api/consultations/{patient_id}` | List all consultations for patient |
| `GET` | `/api/consultation/{id}` | Single consultation details |
| `GET` | `/api/audio/{audio_id}` | Serve generated audio files |
| `GET` | `/health` | Health check |
 
---
 
## Eigen AI Models — The Engine
 
We orchestrate **4 Eigen AI models** into a single coherent voice-AI loop:
 
### 1. Higgs ASR V3.0 — Speech-to-Text
 
| Spec | Value |
|------|-------|
| **Task** | Transcribe doctor-patient consultations |
| **WER** | 9.12% (medical-grade accuracy) |
| **Input** | Audio files (WAV, MP3, M4A, WebM) |
| **Output** | Full text transcript |
| **Used In** | Upload pipeline, voice chat input |
 
Converts every consultation recording into searchable text. Handles medical terminology, multiple speakers, and real-world audio quality.
 
### 2. Higgs Audio V2.5 — Voice Cloning & TTS
 
| Spec | Value |
|------|-------|
| **Task** | Generate voice responses in the doctor's cloned voice |
| **Latency** | ~150ms first-token |
| **Languages** | EN, ES, DE, FR, IT |
| **Output** | WAV audio file |
| **Used In** | Chat voice responses |
 
The doctor's voice is captured from consultation recordings. When the patient asks a question, the AI answer is delivered in **their doctor's familiar voice** — not a generic robot. This builds trust and drives compliance.
 
**Voice-Friendly Text Conversion** — Before TTS, we strip all markdown, emojis, tables, and bullet points. Tables become readable sentences. Headers become natural speech. The result sounds conversational, not like a document being read aloud.
 
### 3. Higgs Audio Understanding V3.5 — Emotional Intelligence
 
| Spec | Value |
|------|-------|
| **Task** | Analyze patient tone, sentiment, and emotional state |
| **Output** | Sentiment score, wellbeing assessment, insights |
| **Used In** | Longitudinal emotional tracking |
 
Enables questions like *"Am I less anxious than last year?"* by comparing the patient's vocal tone across consultations over time.
 
### 4. gpt-oss-120b — The Brain
 
| Spec | Value |
|------|-------|
| **Task** | Summarization + RAG chat completions |
| **Context** | System prompt + patient consultation records + user question |
| **Temperature** | 0.7 |
| **Used In** | Transcript summarization, cross-consultation Q&A |
 
**Summarization** — Extracts structured data from every transcript:
- Diagnoses
- Medications (started, changed, stopped)
- Lifestyle Advice
- Follow-up Plans
- Key Metrics (glucose, A1c, BP, weight, LDL, HDL)
 
**RAG Chat** — Receives retrieved consultation chunks as context and generates comparative, timeline-aware answers that reference specific dates, numbers, and doctor names.
 
---
 
## RAG Pipeline — How Memory Works
 
```
Patient asks: "How has my blood sugar improved?"
                           |
                           v
              +---------------------------+
              | Embed question as vector  |
              | (sentence-transformers)   |
              +------------+--------------+
                           |
                           v
              +---------------------------+
              | ChromaDB Cosine Similarity|
              | Top 10 results            |
              | WHERE patient_id = "xyz"  |
              +------------+--------------+
                           |
         +-----------------+-----------------+
         |                 |                 |
   +-----v------+   +-----v------+   +-----v------+
   | Jan 2023   |   | Jul 2023   |   | Feb 2026   |
   | Transcript |   | Summary    |   | Transcript |
   | Chunk #2   |   |            |   | Chunk #1   |
   | "HbA1c is  |   | "HbA1c    |   | "A1c is    |
   |  8.4%..."  |   |  7.1%..." |   |  5.4%..."  |
   +-----+------+   +-----+------+   +-----+------+
         |                 |                 |
         +-----------------+-----------------+
                           |
                           v
              +---------------------------+
              | gpt-oss-120b generates    |
              | comparative answer with   |
              | dates, numbers, citations |
              +------------+--------------+
                           |
                           v
              +---------------------------+
              | Higgs Audio V2.5 speaks   |
              | the answer in doctor's    |
              | cloned voice              |
              +---------------------------+
```
 
### Dual-Indexing Strategy
 
Every consultation is indexed **twice**:
 
1. **Transcript Chunks** (~1,000 chars, split at sentence boundaries) — For granular detail retrieval
   - *"What was my exact LDL in March 2024?"* -> Finds the specific chunk
2. **Full Summary** — For high-level concept matching
   - *"Am I getting healthier?"* -> Matches against summary trends
 
### Patient-Scoped Retrieval
 
All queries are filtered by `patient_id` in ChromaDB metadata — ensuring complete data isolation between patients. Multi-tenant ready.
 
### Cross-Doctor Intelligence
 
The RAG engine doesn't care which doctor a consultation came from. When Ramesh asks *"Did the diet plan help my cholesterol?"*, it retrieves:
- Dr. Nair's diet advice (nutritionist)
- Dr. Mehta's cholesterol warning (cardiologist)
- Dr. Sharma's improved lab results (internist)
 
**Three doctors. One unified answer. No single doctor has this complete picture.**
 
---
 
## Multi-Specialist Support — The Differentiator
 
Real patients see multiple doctors. DrDejaVu is the **only system** that unifies them:
 
```
         +------------------+
         | Patient: Ramesh  |
         +--------+---------+
                  |
    +-------------+-------------+-------------+
    |             |             |             |
+---v----+  +----v---+  +----v----+  +------v------+
| Dr.    |  | Dr.    |  | Dr.     |  | Dr.         |
| Sharma |  | Mehta  |  | Nair    |  | Reddy       |
| (Int.) |  | (Card.)|  | (Nutr.) |  | (Ophth.)    |
+---+----+  +---+----+  +----+----+  +------+------+
    |           |             |              |
    v           v             v              v
+--------------------------------------------------------+
|              ChromaDB — Unified Vector Store            |
|   All consultations indexed with doctor metadata        |
+----------------------------+---------------------------+
                             |
                             v
                  +----------+-----------+
                  | "What did my         |
                  |  cardiologist say     |
                  |  about cholesterol,   |
                  |  and did the diet     |
                  |  plan help?"          |
                  +----------+-----------+
                             |
                             v
                  +----------+-----------+
                  | Answer pulls from    |
                  | Dr. Mehta (LDL 158)  |
                  | Dr. Nair (plate      |
                  |   method, millets)   |
                  | Dr. Sharma (LDL 94)  |
                  +----------------------+
```
 
### Example Cross-Doctor Queries
 
| Question | Doctors Referenced | Answer |
|----------|--------------------|--------|
| *"Did the diet plan help my cholesterol?"* | Nair + Mehta + Sharma | "Dr. Nair's plate method + millet swaps helped drop your LDL from 158 to 94. Dr. Mehta would be pleased." |
| *"What medications have I stopped?"* | Sharma + Mehta | "Metformin stopped Feb 2026, Lisinopril stopped Mar 2024. You still take Atorvastatin and Aspirin (Dr. Mehta's recommendation)." |
| *"Did my eye doctor find any diabetes problems?"* | Reddy + Sharma | "No retinopathy found in May 2024. Dr. Reddy attributes this to your excellent glucose control under Dr. Sharma." |
| *"What should I eat before carbs?"* | Nair + Sharma | "Both Dr. Nair and Dr. Sharma agree: vegetables and protein first, carbs last. Reduces post-meal glucose spikes by up to 30%." |
 
---
 
## Voice Cloning — Trust Through Familiarity
 
Patients trust their doctor's voice. When a follow-up answer comes in **Dr. Sharma's voice**, Ramesh doesn't feel like he's talking to a machine — he feels like he's getting a callback from his doctor.
 
**How it works:**
1. Doctor's voice is captured from consultation audio recordings
2. Higgs Audio V2.5 creates a voice profile (with consent)
3. When the patient asks a question, the AI answer is generated by gpt-oss-120b
4. The text is converted to voice-friendly format (strip markdown, emojis, tables)
5. Higgs Audio V2.5 synthesizes speech using the doctor's cloned voice
6. Patient hears their doctor's voice delivering the answer
 
**Why it matters:** Voice familiarity drives patient compliance. A robotic voice feels like a tool. A doctor's voice feels like care.
 
---
 
## Use Cases — Beyond the Demo
 
| Use Case | Who Benefits | Example Query |
|----------|-------------|---------------|
| **Chronic Disease Management** | Diabetes, hypertension, cancer patients | *"How has my A1c trended over 3 years?"* |
| **Elderly Patients** | Patients who genuinely forget | *"What did my doctor say about my blood pressure medication?"* |
| **Caregiver Coordination** | Family members managing care | *"What did Mom's oncologist say about her last scan?"* |
| **Multi-Specialist Tracking** | Patients seeing 3+ doctors | *"Did the cardiologist and endocrinologist agree on my treatment?"* |
| **Mental Health** | Therapy patients | *"Am I less anxious than I was 6 months ago?"* (voice sentiment) |
| **Post-Surgery Follow-up** | Surgical patients | *"What restrictions did my surgeon give me?"* |
| **Medication Reconciliation** | Patients on complex regimens | *"Which doctor prescribed which medication, and what's been stopped?"* |
 
---
 
## Tech Stack
 
| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | React 18 + TypeScript + Vite | Type-safe, fast dev, modern UI |
| **Backend** | FastAPI (Python) | Async-native, auto-docs, fast |
| **Vector DB** | ChromaDB (HNSW, cosine) | Lightweight, embeddable, fast similarity search |
| **Metadata DB** | SQLite | Zero-config, reliable, embedded |
| **Speech-to-Text** | Eigen Higgs ASR V3.0 | 9.12% WER, medical-grade |
| **Text-to-Speech** | Eigen Higgs Audio V2.5 | 150ms latency, voice cloning, multilingual |
| **Audio Analysis** | Eigen Higgs Audio Understanding V3.5 | Tone, sentiment, emotional tracking |
| **LLM** | Eigen gpt-oss-120b | Summarization + RAG chat |
| **Deployment** | Docker Compose | One command: `docker-compose up` |
 
---
 
## Quick Start
 
```bash
# Clone & configure
git clone <repo-url> && cd DrDejaVu
cp .env.example .env
# Add your EIGEN_API_KEY and EIGEN_API_BASE_URL
 
# Launch everything
docker-compose up --build
 
# Open
# Frontend:  http://localhost:5173
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
```
 
---
 
## What Makes DrDejaVu Different
 
| Feature | Voice Recorders | Patient Portals | DrDejaVu |
|---------|:-:|:-:|:-:|
| Records consultations | Yes | No | **Yes** |
| Auto-transcribes | No | No | **Yes** |
| Structured summaries | No | Partial | **Yes** |
| Cross-consultation Q&A | No | No | **Yes** |
| Multi-doctor unification | No | No | **Yes** |
| Voice responses | No | No | **Yes** |
| Doctor voice cloning | No | No | **Yes** |
| Emotional tracking | No | No | **Yes** |
| Runs locally (privacy) | Varies | No | **Yes** |
 
---
 
## The Numbers
 
| Metric | Value |
|--------|-------|
| **Lines of Code** | 2,344 (1,163 backend + 1,181 frontend) |
| **Eigen AI Models** | 4 |
| **API Endpoints** | 8 |
| **Frontend Pages** | 3 (Dashboard, Upload, History) |
| **React Components** | 6 |
| **Sample Consultations** | 8 (4 specialists, 3-year timeline) |
| **Unit Tests** | 4 test files, 221 lines |
| **Deployment** | 1 command (`docker-compose up`) |
 
---
 
<h3 align="center"><i>"Your doctor's advice shouldn't expire when you walk out the door."</i></h3>
 
<p align="center"><b>DrDejaVu</b> — Voice In. Perfect Memory. Voice Out.</p>

