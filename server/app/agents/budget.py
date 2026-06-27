from .llm import call_llm

BUDGET_PROMPT = """
    You are a travel budget planner.
    Given a total budget, allocate money across:
    - flights
    - hotels
    Return JSON only.
    Format:
    {
        "flight_budget": float,
        "hotel_budget": float
    }
"""

async def allocate_budget(intent: dict):
    prompt = f"""Total Budget: {intent['budget']}
Trip Length: {intent['days']} days
People: {intent['people']}"""
    return await call_llm(prompt, system_prompt=BUDGET_PROMPT)

