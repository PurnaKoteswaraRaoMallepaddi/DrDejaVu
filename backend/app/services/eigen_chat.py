"""Eigen AI Higgs Audio V2.5 — Conversational Voice AI service.

Model: https://app.eigenai.com/model-library/higgs2p5
Generates natural voice responses with ~150ms first-token latency.
Supports multilingual output (EN, ES, DE, FR, IT).
"""

import json
import uuid
from pathlib import Path

import httpx

from app.config import settings


async def generate_voice_response(text: str, language: str = "en") -> str:
    """Generate a spoken audio response using Eigen Higgs Audio V2.5.

    Uses the /generate endpoint with form-data format.
    Returns a URL path to the generated audio file.
    """
    url = f"{settings.eigen_api_base_url}/generate"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
    }
    
    audio_id = str(uuid.uuid4())
    output_path = Path(settings.upload_dir) / f"response_{audio_id}.wav"

    data = {
        "model": settings.eigen_chat_model,
        "text": text,
        "voice": "Linda",  # Default voice; options: Linda, Jack, etc.
        "stream": "false",
        "sampling": json.dumps({"temperature": 0.85, "top_p": 0.95, "top_k": 50}),
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()

        output_path.write_bytes(response.content)

    return f"/api/audio/{audio_id}"


async def chat_completion(messages: list[dict], patient_context: str = "") -> str:
    """Use Higgs Audio V2.5 as an LLM for chat completion.

    Uses form-data format with /generate endpoint.
    """
    url = f"{settings.eigen_api_base_url}/generate"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
    }

    system_prompt = (
        "You are DrDejaVu, a compassionate health assistant that helps patients "
        "understand their medical history by comparing consultations over time. "
        "Provide clear, empathetic answers based on the consultation records provided. "
        "Always note the dates of consultations you reference."
    )
    if patient_context:
        system_prompt += f"\n\nRelevant consultation records:\n{patient_context}"

    # Combine system prompt with latest user message
    last_message = messages[-1]["content"] if messages else ""
    full_prompt = f"{system_prompt}\n\nUser: {last_message}"

    data = {
        "model": settings.eigen_chat_model,
        "text": full_prompt,
        "voice": "Linda",  # Default voice
        "stream": "false",
        "sampling": json.dumps({"temperature": 0.7, "top_p": 0.95, "top_k": 50}),
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()

    return result.get("text", result.get("output", ""))
