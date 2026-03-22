"""Eigen AI Higgs ASR V3.0 — Speech-to-Text service.

Model: https://app.eigenai.com/model-library/higgs_asr_3
Converts consultation audio (wav/mp3/m4a) into text transcripts.
"""

import logging

from app.config import settings
from app.services.http_client import get_http_client

logger = logging.getLogger(__name__)


async def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    """Transcribe audio bytes using Eigen Higgs ASR V3.0.

    Uses the /generate endpoint with form-data file upload.
    """
    # Determine MIME type from filename
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"
    mime_map = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}
    mime_type = mime_map.get(ext, "audio/wav")

    url = f"{settings.eigen_api_base_url}/generate"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
    }

    # Form-data parameters for ASR
    data = {
        "model": settings.eigen_asr_model,
        "language": "English",
    }

    logger.info(f"[ASR] Starting transcription for file: {filename}")
    logger.info(f"[ASR] URL: {url}")
    logger.info(f"[ASR] Model: {settings.eigen_asr_model}")
    logger.info(f"[ASR] MIME type: {mime_type}")
    logger.info(f"[ASR] Audio size: {len(audio_bytes)} bytes")
    logger.info(f"[ASR] Request data: {data}")

    client = get_http_client()
    response = await client.post(
        url,
        headers=headers,
        data=data,
        files={"file": (filename, audio_bytes, mime_type)},
        timeout=120.0,
    )

    logger.info(f"[ASR] Response status: {response.status_code}")

    response.raise_for_status()
    result = response.json()

    # Extract transcription from response
    text = result.get("transcription", "")
    logger.info(f"[ASR] Extracted text length: {len(text)} chars")
    
    return text
