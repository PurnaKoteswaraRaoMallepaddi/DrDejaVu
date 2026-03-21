"""Eigen AI Higgs ASR V3.0 — Speech-to-Text service.

Model: https://app.eigenai.com/model-library/higgs_asr_3
Converts consultation audio (wav/mp3/m4a) into text transcripts.
"""

import base64
import httpx

from app.config import settings


async def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    """Transcribe audio bytes using Eigen Higgs ASR V3.0.

    The Eigen AI platform exposes an OpenAI-compatible API.
    For audio transcription, we send the audio file to the
    transcription endpoint.
    """
    # Determine MIME type from filename
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"
    mime_map = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}
    mime_type = mime_map.get(ext, "audio/wav")

    # Eigen AI uses OpenAI-compatible audio transcription API
    url = f"{settings.eigen_api_base_url}/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url,
            headers=headers,
            data={"model": settings.eigen_asr_model},
            files={"file": (filename, audio_bytes, mime_type)},
        )
        response.raise_for_status()
        result = response.json()

    return result.get("text", "")
