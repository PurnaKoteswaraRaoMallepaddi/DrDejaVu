"""Eigen AI Higgs Audio V2.5 — Conversational Voice AI service.

Model: https://app.eigenai.com/model-library/higgs2p5
Generates natural voice responses with ~150ms first-token latency.
Supports multilingual output (EN, ES, DE, FR, IT).
"""

import base64
import uuid
from pathlib import Path

import httpx

from app.config import settings


async def generate_voice_response(text: str, language: str = "en") -> str:
    """Generate a spoken audio response using Eigen Higgs Audio V2.5.

    Uses the OpenAI-compatible TTS endpoint on the Eigen platform.
    Returns a URL path to the generated audio file.
    """
    url = f"{settings.eigen_api_base_url}/audio/speech"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.eigen_chat_model,
        "input": text,
        "voice": "alloy",  # Default voice; can be customized
        "response_format": "wav",
    }

    audio_id = str(uuid.uuid4())
    output_path = Path(settings.upload_dir) / f"response_{audio_id}.wav"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()

        output_path.write_bytes(response.content)

    return f"/api/audio/{audio_id}"


async def chat_completion(messages: list[dict], patient_context: str = "") -> str:
    """Use Higgs Audio V2.5 as an LLM for chat completion.

    The Eigen platform supports OpenAI-compatible chat completions.
    """
    url = f"{settings.eigen_api_base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        "You are DrDejaVu, a compassionate health assistant that helps patients "
        "understand their medical history by comparing consultations over time. "
        "Provide clear, empathetic answers based on the consultation records provided. "
        "Always note the dates of consultations you reference."
    )
    if patient_context:
        system_prompt += f"\n\nRelevant consultation records:\n{patient_context}"

    payload = {
        "model": settings.eigen_chat_model,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

    return result["choices"][0]["message"]["content"]
