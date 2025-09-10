import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
ORS_API_KEY = "YOUR_ORS_API_KEY"  # put in .env later

async def search_places(query: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": 5},
            headers={"User-Agent": "maps-assistant"}
        )
        return resp.json()

async def get_directions(origin: str, destination: str):
    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
    body = {
        "coordinates": [
            [float(origin.split(",")[0]), float(origin.split(",")[1])],
            [float(destination.split(",")[0]), float(destination.split(",")[1])]
        ]
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(ORS_URL, headers=headers, json=body)
        return resp.json()
