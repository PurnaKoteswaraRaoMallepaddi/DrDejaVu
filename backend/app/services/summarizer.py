"""Consultation transcript summarizer.

Uses the Eigen AI chat model to extract structured summaries
(diagnoses, medications, lifestyle advice) from consultation transcripts.
"""

import httpx

from app.config import settings


SUMMARIZE_PROMPT = """\
You are a medical transcript summarizer. Given a doctor-patient consultation \
transcript, extract and organize the key information into these categories:

1. **Diagnoses**: Any conditions diagnosed or discussed
2. **Medications**: Prescriptions, dosage changes, or medication discussions
3. **Lifestyle Advice**: Diet, exercise, sleep, stress management recommendations
4. **Follow-up**: Next appointment, tests ordered, referrals
5. **Key Metrics**: Any vital signs, lab results, or measurements mentioned

Be concise but thorough. Use bullet points."""


async def summarize_transcript(transcript: str) -> str:
    """Summarize a consultation transcript into structured categories."""
    url = f"{settings.eigen_api_base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.eigen_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.eigen_chat_model,
        "messages": [
            {"role": "system", "content": SUMMARIZE_PROMPT},
            {"role": "user", "content": f"Summarize this consultation:\n\n{transcript}"},
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

    return result["choices"][0]["message"]["content"]
