from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConsultationCreate(BaseModel):
    patient_id: str
    doctor_name: str = ""
    consultation_date: Optional[str] = None
    notes: str = ""


class ConsultationResponse(BaseModel):
    id: str
    patient_id: str
    doctor_name: str
    consultation_date: str
    transcript: str
    summary: str
    notes: str
    created_at: str


class TranscribeResponse(BaseModel):
    consultation_id: str
    transcript: str
    summary: str
    duration_seconds: Optional[float] = None


class QueryRequest(BaseModel):
    patient_id: str
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


class ChatRequest(BaseModel):
    patient_id: str
    question: str
    voice_response: bool = True


class ChatResponse(BaseModel):
    answer: str
    audio_url: Optional[str] = None
    sources: list[dict]


class AnalysisResponse(BaseModel):
    sentiment: str
    tone: str
    wellbeing_score: float
    insights: list[str]
