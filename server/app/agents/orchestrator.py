from .planner import choose_tools
from .tools import execute_tools
from .optimizer import optimize_trip
from .budget import allocate_budget
from .summarizer import summarize_trip

async def plan_trip(user_prompt: str, intent: dict):
    tool_plan = await choose_tools(user_prompt)
    budget_plan = await allocate_budget(intent)
    intent["flight_budget"] = budget_plan["flight_budget"]
    intent["hotel_budget"] = budget_plan["hotel_budget"]
    tools = tool_plan.get("tools", [])
    tool_results = await execute_tools(tools, intent)
    flights = tool_results.get("flight_search", [])
    hotels = tool_results.get("hotel_search", [])
    best_plan = optimize_trip(
        flights,
        hotels,
        intent["budget"]
    )
    summary = await summarize_trip(intent, best_plan) if best_plan else ""
    return {
        "intent": intent,
        "budget_plan": budget_plan,
        "plan": best_plan,
        "summary": summary,
    }