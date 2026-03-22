"""Eigen AI Higgs Audio Understanding V3.5 — Audio Analysis service.

Analyzes tone, sentiment, and well-being from patient voice recordings.
Used for longitudinal comparison of patient emotional state across visits.
"""

from app.config import settings
from app.models.schemas import AnalysisResponse
from app.services.http_client import get_http_client


async def analyze_audio(audio_bytes: bytes, filename: str) -> AnalysisResponse:
    """Analyze audio for sentiment, tone, and well-being indicators.

    Uses Higgs Audio Understanding V3.5 for advanced audio comprehension
    beyond simple transcription.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"
    mime_map = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}
    mime_type = mime_map.get(ext, "audio/wav")

    url = f"{settings.eigen_api_base_url}/audio/analysis"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
    }

    client = get_http_client()
    response = await client.post(
        url,
        headers=headers,
        data={
            "model": settings.eigen_understanding_model,
            "analysis_type": "sentiment,tone,wellbeing",
        },
        files={"file": (filename, audio_bytes, mime_type)},
        timeout=120.0,
    )
    response.raise_for_status()
    result = response.json()

    return AnalysisResponse(
        sentiment=result.get("sentiment", "neutral"),
        tone=result.get("tone", "calm"),
        wellbeing_score=result.get("wellbeing_score", 0.5),
        insights=result.get("insights", []),
    )
