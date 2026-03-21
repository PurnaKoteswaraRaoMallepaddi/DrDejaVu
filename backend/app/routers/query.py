from fastapi import APIRouter

from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_engine import query_consultations

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_patient_history(req: QueryRequest):
    """Query patient consultation history using RAG.

    Retrieves relevant consultation records and generates a comparative answer.
    """
    result = await query_consultations(
        patient_id=req.patient_id,
        question=req.question,
    )
    return result
