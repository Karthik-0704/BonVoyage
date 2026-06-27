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
    response.raise_for_status()
    return response
async def _get_entity_id(client: httpx.AsyncClient, query: str) -> str:
    response = await _get_with_retry(
        client,
        f"https://{RAPIDAPI_HOST}/hotels/auto-complete",
        {"query": query},
    )
    data = response.json()
    if data.get("data"):
        return data["data"][0]["entityId"]
    raise ValueError(f"No entityId found for: {query}")

async def search_hotels(destination: str, days: int, people: int):
    checkin = date.today().strftime("%Y-%m-%d")
    checkout = (date.today() + timedelta(days=days)).strftime("%Y-%m-%d")
    cache_key = make_key("hotels", destination=destination, checkin=checkin, checkout=checkout, people=people)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    async with httpx.AsyncClient(timeout=30.0) as client:
        entity_id = await _get_entity_id(client, destination)
        hotel_params = {
            "entityId": entity_id,
            "checkin": checkin,
            "checkout": checkout,
            "adults": people,
            "market": "US",
            "locale": "en-US",
            "currency": "USD",
            "resultsPerPage": 10,
        }
        response = await _get_with_retry(client, f"https://{RAPIDAPI_HOST}/hotels/search", hotel_params)
        data = response.json()

        # Poll until results are complete
        while data.get("status", {}).get("completionPercentage", 100) < 100:
            await asyncio.sleep(1)
            response = await _get_with_retry(client, f"https://{RAPIDAPI_HOST}/hotels/search", hotel_params)
            data = response.json()

    hotels = []
    for hotel in data.get("data", {}).get("hotels", []):
        try:
            name = hotel["name"]
            price_per_night = hotel["price"]["lead"]["amount"]
            total_price = round(price_per_night * days, 2)
            hotels.append({
                "name": name,
                "price_per_night": round(price_per_night, 2),
                "total_price": total_price,
            })
        except (KeyError, TypeError):
            continue

    await cache_set(cache_key, hotels)
    return hotels
