import httpx
import asyncio
from datetime import date, timedelta
import os
from app.services.cache import cache_get, cache_set, make_key

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "c16a6ab152msh6d909e7fd7b1ad1p126e5djsnf6256fb3ec4c")
RAPIDAPI_HOST = "flights-sky.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
}

async def _get_with_retry(client: httpx.AsyncClient, url: str, params: dict, retries: int = 3) -> httpx.Response:
    for attempt in range(retries):
        response = await client.get(url, params=params, headers=HEADERS)
        if response.status_code == 429:
            wait = 2 ** attempt
            await asyncio.sleep(wait)
            continue
        response.raise_for_status()
        return response
    response.raise_for_status()  # raise after exhausting retries
    return response

async def _get_sky_id(client: httpx.AsyncClient, query: str) -> str:
    response = await _get_with_retry(
        client,
        f"https://flights-sky.p.rapidapi.com/flights/auto-complete",
        {"query": query, "placeTypes": "CITY,AIRPORT"},
    )
    data = response.json()
    if data.get("data"):
        return data["data"][0]["navigation"]["relevantFlightParams"]["skyId"]
    raise ValueError(f"No skyId found for: {query}")

async def search_flights(origin: str, destination: str, people: int, days: int):
    depart_date = (date.today() + timedelta(days=days)).strftime("%Y-%m-%d")
    cache_key = make_key("flights", origin=origin, destination=destination, people=people, depart_date=depart_date)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    async with httpx.AsyncClient(timeout=30.0) as client:
        from_id, to_id = (
            await _get_sky_id(client, origin),
            await _get_sky_id(client, destination),
        )
        response = await _get_with_retry(
            client,
            f"https://flights-sky.p.rapidapi.com/flights/search-one-way",
            {
                "fromEntityId": from_id,
                "toEntityId": to_id,
                "adults": people,
                "departDate": depart_date,
                "market": "US",
                "locale": "en-US",
                "currency": "USD",
                "cabinClass": "economy",
            },
        )
        data = response.json()

    flights = []
    # Some response shapes nest under data.itineraries, others at top level
    raw_data = data.get("data")
    if isinstance(raw_data, dict):
        itineraries = raw_data.get("itineraries", [])
    else:
        itineraries = data.get("itineraries", [])
    for itinerary in itineraries:
        try:
            total_price = itinerary["price"]["raw"]
            leg = itinerary["legs"][0]
            airline = leg["carriers"]["marketing"][0]["name"]
            duration_hours = round(leg["durationInMinutes"] / 60, 1)
            flights.append({
                "airline": airline,
                "price_per_person": round(total_price / people, 2),
                "total_price": round(total_price, 2),
                "duration_hours": duration_hours,
            })
        except (KeyError, IndexError, ZeroDivisionError):
            continue

    await cache_set(cache_key, flights)
    return flights
