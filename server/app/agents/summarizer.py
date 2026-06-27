import json
from .llm import call_llm_text

SUMMARIZER_PROMPT = """
You are a friendly travel assistant.
You will receive a JSON object describing a planned trip.
Write a concise 2-3 sentence plain-English summary that covers:
- Where the traveler is going and for how long
- The flight they will take (airline and price)
- The hotel they will stay at (name and price)
- The total estimated cost

Write in a warm, conversational tone. No bullet points. No JSON. Just a short paragraph.
"""


async def summarize_trip(intent: dict, plan: dict) -> str:
    trip_info = {
        "origin": intent.get("origin"),
        "destination": intent.get("destination"),
        "days": intent.get("days"),
        "people": intent.get("people"),
        "budget": intent.get("budget"),
        "flight": plan.get("flight"),
        "hotel": plan.get("hotel"),
        "total_cost": plan.get("total_cost"),
    }
    prompt = f"Trip plan:\n{json.dumps(trip_info, indent=2)}"
    return await call_llm_text(prompt, system_prompt=SUMMARIZER_PROMPT)
