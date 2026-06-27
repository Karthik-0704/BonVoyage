import json
from .llm import call_llm

PLANNER_PROMPT = """
    You are an AI planner that decides which tools to call.
    Available tools:
    - flight_search
    - hotel_search
    Return JSON only.
    Format:
    {
        "tools": ["flight_search", "hotel_search"]
    }
"""

async def choose_tools(user_prompt: str):
    response = await call_llm(user_prompt, system_prompt=PLANNER_PROMPT)
    return response