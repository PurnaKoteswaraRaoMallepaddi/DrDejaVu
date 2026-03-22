import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, File, Form, UploadFile

from app.models.schemas import TranscribeResponse
from app.services.eigen_asr import transcribe_audio
from app.services.summarizer import summarize_transcript
from app.services.rag_engine import index_consultation
from app.db.sqlite_store import save_consultation

logger = logging.getLogger(__name__)

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
    logger.info(
        "Starting transcription — consultation_id=%s patient_id=%s doctor=%s date=%s",
        consultation_id, patient_id, doctor_name, consultation_date,
    )

    # Read audio bytes
    try:
        audio_bytes = await audio.read()
        filename = audio.filename or "recording.wav"
        logger.info(
            "Received audio file=%s size=%d bytes", filename, len(audio_bytes)
        )
    except Exception:
        logger.exception("Failed to read uploaded audio file")
        raise

    # 1. Transcribe via Eigen Higgs ASR V3.0
    try:
        logger.info("Step 1: Calling Eigen ASR for transcription...")
        transcript = await transcribe_audio(audio_bytes, filename)
        logger.info("Transcription complete — length=%d chars", len(transcript))
    except Exception:
        logger.exception("Step 1 FAILED: Eigen ASR transcription error")
        raise

    # 2. Summarize the transcript
    try:
        logger.info("Step 2: Summarizing transcript...")
        summary = await summarize_transcript(transcript)
        logger.info("Summarization complete — length=%d chars", len(summary))
    except Exception:
        logger.exception("Step 2 FAILED: Summarization error")
        raise

    # 3. Index in vector DB for RAG retrieval
    date_str = consultation_date or datetime.now().isoformat()
    try:
        logger.info("Step 3: Indexing consultation in vector DB...")
        await index_consultation(
            consultation_id=consultation_id,
            patient_id=patient_id,
            transcript=transcript,
            summary=summary,
            consultation_date=date_str,
        )
        logger.info("Indexing complete")
    except Exception:
        logger.exception("Step 3 FAILED: RAG indexing error")
        raise

    # 4. Save metadata to SQLite
    try:
        logger.info("Step 4: Saving consultation to SQLite...")
        await save_consultation(
            consultation_id=consultation_id,
            patient_id=patient_id,
            doctor_name=doctor_name,
            consultation_date=date_str,
            transcript=transcript,
            summary=summary,
        )
        logger.info("SQLite save complete")
    except Exception:
        logger.exception("Step 4 FAILED: SQLite save error")
        raise

    logger.info("Transcription pipeline finished — consultation_id=%s", consultation_id)
    return TranscribeResponse(
        consultation_id=consultation_id,
        transcript=transcript,
        summary=summary,
    )
