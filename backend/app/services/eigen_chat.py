"""Eigen AI Higgs Audio V2.5 — Conversational Voice AI service.

Model: https://app.eigenai.com/model-library/higgs2p5
Generates natural voice responses with ~150ms first-token latency.
Supports multilingual output (EN, ES, DE, FR, IT).
"""

import json
import logging
import re
import uuid
from pathlib import Path

from app.config import settings
from app.services.http_client import get_http_client


def _is_straightforward_question(question: str) -> bool:
    """Detect if a question is straightforward (factual/quick) or needs explanation.
    
    Straightforward: factual, quantitative, or yes/no questions.
    Explanation-needed: why, how, compare, impact, explain, etc.
    """
    question_lower = question.lower().strip()
    
    # Explanation-demanding keywords indicate complex questions
    explanation_keywords = [
        "why", "how", "explain", "what does", "what caused",
        "compare", "difference", "relationship", "impact", "affect",
        "effect", "cause", "tell me about", "describe", "elaborate"
    ]
    
    # Check for explanation keywords
    for keyword in explanation_keywords:
        if keyword in question_lower:
            return False
    
    # Straightforward patterns: factual, quick answers
    straightforward_patterns = [
        r"^what is\s",
        r"^when is\s",
        r"^where is\s",
        r"^who is\s",
        r"^how much\s",
        r"^how many\s",
        r"\?$",  # Yes/no or short questions ending with ?
    ]
    
    for pattern in straightforward_patterns:
        if re.search(pattern, question_lower):
            return True
    
    # If question is very short and doesn't contain explanation keywords, likely straightforward
    if len(question_lower) < 50 and "explain" not in question_lower:
        return True
    
    return False


def convert_to_voice_friendly_text(text: str) -> str:
    """Convert formatted text (markdown, tables, emojis) to natural speech.
    
    Transforms visual formatting into conversational, voice-optimized text
    that sounds natural when read aloud.
    """
    # Remove markdown formatting
    text = text.replace("**", "")  # Remove bold
    text = text.replace("__", "")  # Remove alternative bold
    text = text.replace("_", "")   # Remove italics
    text = text.replace("`", "")   # Remove inline code
    text = text.replace("~~", "")  # Remove strikethrough
    
    # Remove emojis and special symbols
    text = re.sub(r'[📋🩺💊📊✅❌⚠️🔔🏥💉📝🔗📈📉]', '', text)
    
    # Convert markdown headers to plain text
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove markdown table formatting
    lines = text.split('\n')
    processed_lines = []
    skip_table_separator = False
    
    for line in lines:
        # Skip table separators (lines with just |, -, and spaces)
        if re.match(r'^[\s|:-]+$', line):
            skip_table_separator = True
            continue
        
        # Convert table cells to readable format
        if '|' in line:
            # Extract table content, remove pipes
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            line = ' - '.join(cells)
        
        # Remove multiple spaces
        line = re.sub(r'\s+', ' ', line).strip()
        
        if line:
            processed_lines.append(line)
    
    text = '\n'.join(processed_lines)
    
    # Fix common patterns for natural speech
    text = text.replace('---', '.')  # Section breaks become periods
    text = re.sub(r'•\s*', ' ', text)  # Convert bullet points
    text = re.sub(r'\n{2,}', '\n', text)  # Remove excessive line breaks
    
    # Add pauses for natural speech (periods get emphasis)
    text = text.replace('\n', '. ')  # Convert newlines to sentence breaks
    
    # Clean up any artifacts
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


async def generate_voice_response(text: str, language: str = "en") -> str:
    """Generate a spoken audio response using Eigen Higgs Audio V2.5.

    Uses the /generate endpoint with form-data format.
    Converts formatted text to natural speech before TTS generation.
    Returns a URL path to the generated audio file.
    
    Note: HiggsAudio V2.5 has a character limit (~1000 chars), so longer text is truncated.
    """
    # Convert formatted text to voice-friendly version
    voice_text = convert_to_voice_friendly_text(text)
    
    url = f"{settings.eigen_api_base_url}/generate"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
    }
    
    audio_id = str(uuid.uuid4())
    output_path = Path(settings.upload_dir) / f"response_{audio_id}.wav"

    client = get_http_client()
    response = await client.post(url, headers=headers,
                                 json={"model": settings.eigen_chat_model, "text": voice_text})
    logging.info(f"[TTS] Response status: {response.status_code}")

    if response.status_code != 200:
        try:
            error_json = response.json()
            logging.error(f"[TTS] Error response: {json.dumps(error_json, indent=2)}")
        except Exception:
            logging.error(f"[TTS] Error response text: {response.text}")

    response.raise_for_status()
    output_path.write_bytes(response.content)

    return f"/api/audio/{audio_id}"


async def chat_completion(messages: list[dict], patient_context: str = "") -> str:
    """Use gpt-oss-120b LLM for chat completion.

    Uses /chat/completions endpoint with JSON format.
    Dynamically adjusts response length based on question complexity.
    """
    url = f"{settings.eigen_api_base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
        "Content-Type": "application/json",
    }

    # Extract user question to determine response style
    user_question = ""
    if messages:
        user_question = messages[-1].get("content", "") if messages[-1].get("role") == "user" else ""
    
    # Determine if question is straightforward or needs explanation
    is_straightforward = _is_straightforward_question(user_question)
    
    # Build base system prompt
    base_prompt = (
        "You are DrDejaVu, a compassionate health assistant that helps patients "
        "understand their medical history by comparing consultations over time. "
        "Provide clear, empathetic answers based on the consultation records provided. "
        "Always note the dates of consultations you reference. "
        "When giving voice responses, be conversational and natural, as if speaking to a friend. "
        "Use everyday language rather than overly technical terms. "
        "Break information into short, digestible points. "
        "Sound warm, understanding, and genuinely interested in helping the patient."
    )
    
    # Add dynamic instructions based on question type
    if is_straightforward:
        # Quick answer: 5-10 seconds, minimal explanation
        response_instruction = (
            " Keep your response brief and direct (1-2 sentences). "
            "Aim for a response that takes 5-10 seconds to speak aloud."
        )
        max_tokens = 150
    else:
        # Explanation needed: 50-100 words, more detail
        response_instruction = (
            " Provide a clear but concise explanation (50-100 words). "
            "Include key points and relevant dates from consultation records."
        )
        max_tokens = 350
    
    system_prompt = base_prompt + response_instruction
    
    if patient_context:
        system_prompt += f"\n\nRelevant consultation records:\n{patient_context}"

    logging.info(f"[Chat] Question type: {'straightforward' if is_straightforward else 'explanation-needed'}")
    logging.info(f"[Chat] Max tokens: {max_tokens}")
    logging.info(f"[Chat] System prompt length: {len(system_prompt)} chars")

    # Build messages array for LLM
    messages_array = [{"role": "system", "content": system_prompt}] + messages

    payload = {
        "model": settings.eigen_summarizer_model,
        "messages": messages_array,
        "temperature": 0.7,
        "max_tokens": max_tokens,
        "reasoning_effort": "low",
        "stream": False,
    }

    logging.info(f"[Chat] Sending request, model={settings.eigen_summarizer_model}")

    client = get_http_client()
    response = await client.post(url, headers=headers, json=payload)
    logging.info(f"[Chat] Response status: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"[Chat] Response text: {response.text}")

    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
