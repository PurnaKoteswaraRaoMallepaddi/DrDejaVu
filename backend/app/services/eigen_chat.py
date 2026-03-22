"""Eigen AI Higgs Audio V2.5 — Conversational Voice AI service.

Model: https://app.eigenai.com/model-library/higgs2p5
Generates natural voice responses with ~150ms first-token latency.
Supports multilingual output (EN, ES, DE, FR, IT).
"""

import json
import logging
import uuid
from pathlib import Path

import httpx

from app.config import settings


async def generate_voice_response(text: str, language: str = "en") -> str:
    """Generate a spoken audio response using Eigen Higgs Audio V2.5.

    Uses the /generate endpoint with form-data format.
    Returns a URL path to the generated audio file.
    
    Note: HiggsAudio V2.5 has a character limit (~1000 chars), so longer text is truncated.
    """
    url = f"{settings.eigen_api_base_url}/generate"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
    }
    
    # Truncate text to avoid exceeding TTS limits (~1000 chars)
    max_chars = 1000
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
        logging.info(f"[TTS] Text truncated from {len(text)} to {max_chars} chars")
    
    audio_id = str(uuid.uuid4())
    output_path = Path(settings.upload_dir) / f"response_{audio_id}.wav"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, 
                                     json={"model": settings.eigen_chat_model, "text": text})
        logging.info(f"[TTS] Response status: {response.status_code}")
        
        # Log error response BEFORE raising
        if response.status_code != 200:
            try:
                error_json = response.json()
                logging.error(f"[TTS] Error response: {json.dumps(error_json, indent=2)}")
            except:
                logging.error(f"[TTS] Error response text: {response.text}")
        
        response.raise_for_status()
        output_path.write_bytes(response.content)
        logging.info(f"[TTS] Audio saved to {output_path}, size: {len(response.content)} bytes")

    return f"/api/audio/{audio_id}"


async def chat_completion(messages: list[dict], patient_context: str = "") -> str:
    """Use gpt-oss-120b LLM for chat completion.

    Uses /chat/completions endpoint with JSON format.
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

    logging.info(f"[Chat] System prompt length: {len(system_prompt)} chars")

    # Build messages array for LLM
    messages_array = [{"role": "system", "content": system_prompt}] + messages

    payload = {
        "model": settings.eigen_summarizer_model,  # Use gpt-oss-120b for LLM
        "messages": messages_array,
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": False,
    }
    
    logging.info(f"[Chat] Sending request to {url}")
    logging.info(f"[Chat] Model: {settings.eigen_summarizer_model}")
    logging.info(f"[Chat] Messages: {len(messages_array)} (system + user)")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        logging.info(f"[Chat] Response status: {response.status_code}")
        
        if response.status_code != 200:
            logging.error(f"[Chat] Response text: {response.text}")
        
        response.raise_for_status()
        result = response.json()

    logging.info(f"[Chat] Response received: {json.dumps(result, indent=2)}")
    return result["choices"][0]["message"]["content"]
