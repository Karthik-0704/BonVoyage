import os
import httpx
import json
import re

HF_TOKEN = os.getenv("HF_TOKEN")

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

SYSTEM_PROMPT = """
    You are an intent extraction engine.
    Extract structured travel planning information.
    Return ONLY valid JSON in this format:
    {
        "origin": "string",
        "destination": "string",
        "days": int,
        "people": int,
        "budget": float
    }
    No explanation.
    No extra text.
"""

async def call_llm(user_prompt: str, system_prompt: str = SYSTEM_PROMPT):
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN not set")
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        # Prefer an explicit ```json ... ``` fence
        fence_match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
        if fence_match:
            return json.loads(fence_match.group(1))
        # Fall back to the last bare {...} block (avoids grabbing code examples mid-text)
        candidates = re.findall(r"\{[^{}]*\}", content, re.DOTALL)
        if not candidates:
            raise json.JSONDecodeError("No JSON object found", content, 0)
        return json.loads(candidates[-1])
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"LLM API error: {e.response.status_code} - {e.response.text}")
    except json.JSONDecodeError:
        raise RuntimeError(f"LLM returned invalid JSON: {content}")


async def call_llm_text(user_prompt: str, system_prompt: str) -> str:
    """Same as call_llm but returns the raw text content instead of parsed JSON."""
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN not set")
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()