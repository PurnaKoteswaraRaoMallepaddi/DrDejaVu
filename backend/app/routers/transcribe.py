import uuid
from datetime import datetime

from fastapi import APIRouter, File, Form, UploadFile

from app.models.schemas import TranscribeResponse
from app.services.eigen_asr import transcribe_audio
from app.services.summarizer import summarize_transcript
from app.services.rag_engine import index_consultation
from app.db.sqlite_store import save_consultation

router = APIRouter()


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_consultation(
    audio: UploadFile = File(...),
    patient_id: str = Form(...),
    doctor_name: str = Form(""),
    consultation_date: str = Form(""),
):
    """Upload a consultation audio file, transcribe it, summarize, and index for RAG."""
    consultation_id = str(uuid.uuid4())

    # Read audio bytes
    audio_bytes = await audio.read()
    filename = audio.filename or "recording.wav"

    # 1. Transcribe via Eigen Higgs ASR V3.0
    transcript = await transcribe_audio(audio_bytes, filename)

    # 2. Summarize the transcript
    summary = await summarize_transcript(transcript)

    # 3. Index in vector DB for RAG retrieval
    date_str = consultation_date or datetime.now().isoformat()
    await index_consultation(
        consultation_id=consultation_id,
        patient_id=patient_id,
        transcript=transcript,
        summary=summary,
        consultation_date=date_str,
    )

    # 4. Save metadata to SQLite
    await save_consultation(
        consultation_id=consultation_id,
        patient_id=patient_id,
        doctor_name=doctor_name,
        consultation_date=date_str,
        transcript=transcript,
        summary=summary,
    )

    return TranscribeResponse(
        consultation_id=consultation_id,
        transcript=transcript,
        summary=summary,
    )
