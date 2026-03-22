import asyncio

from fastapi import APIRouter, File, Form, UploadFile

from app.models.schemas import ChatRequest, ChatResponse
from app.services.eigen_asr import transcribe_audio
from app.services.eigen_chat import generate_voice_response
from app.services.rag_engine import query_consultations

router = APIRouter()


@router.post("/chat/text", response_model=ChatResponse)
async def chat_text(req: ChatRequest):
    """Text-based chat: ask a question, get text + optional audio answer."""
    rag_result = await query_consultations(
        patient_id=req.patient_id,
        question=req.question,
    )

    response = ChatResponse(
        answer=rag_result.answer,
        sources=rag_result.sources,
    )

    if req.voice_response:
        audio_url = await generate_voice_response(rag_result.answer)
        response.audio_url = audio_url

    return response


@router.post("/chat/voice", response_model=ChatResponse)
async def chat_voice(
    audio: UploadFile = File(...),
    patient_id: str = Form(...),
):
    """Voice-based chat: send audio question, get text + audio answer.

    Reads the uploaded audio eagerly, then runs transcription.
    After RAG retrieval, generates voice response.
    """
    # Read audio bytes eagerly so the upload is consumed fast
    audio_bytes = await audio.read()

    # 1. Transcribe the question
    question = await transcribe_audio(audio_bytes, audio.filename or "query.wav")

    # 2. RAG query
    rag_result = await query_consultations(
        patient_id=patient_id,
        question=question,
    )

    # 3. Generate voice response
    audio_url = await generate_voice_response(rag_result.answer)

    return ChatResponse(
        answer=rag_result.answer,
        audio_url=audio_url,
        sources=rag_result.sources,
    )
