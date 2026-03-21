from fastapi import APIRouter

from app.models.schemas import ConsultationResponse
from app.db.sqlite_store import get_consultations, get_consultation_by_id

router = APIRouter()


@router.get("/consultations/{patient_id}", response_model=list[ConsultationResponse])
async def list_consultations(patient_id: str):
    """List all consultations for a patient, ordered by date."""
    return await get_consultations(patient_id)


@router.get("/consultation/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation(consultation_id: str):
    """Get a single consultation by ID."""
    return await get_consultation_by_id(consultation_id)
