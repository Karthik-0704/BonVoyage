import asyncio
from .flights import search_flights
from .hotels import search_hotels

TOOLS = {
    "flight_search": search_flights,
    "hotel_search": search_hotels
}

async def execute_tools(tool_list, intent):
    tasks = []
    results = {}
    for tool_name in tool_list:
        if tool_name not in TOOLS:
            continue
        tool = TOOLS[tool_name]
        if tool_name == "flight_search":
            tasks.append(
                tool(
                    intent["origin"],
                    intent["destination"],
                    intent["people"],
                    intent["days"]
                )
            )
        elif tool_name == "hotel_search":
            tasks.append(
                tool(
                    intent["destination"],
                    intent["days"],
                    intent["people"]
                )
            )
    outputs = await asyncio.gather(*tasks)
    idx = 0
    for tool_name in tool_list:
        if tool_name in TOOLS:
            results[tool_name] = outputs[idx]
            idx += 1

    return results

