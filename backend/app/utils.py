import os
from dotenv import load_dotenv
import httpx

load_dotenv()

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
ORS_API_KEY = os.getenv("ORS_API_KEY")  # set in .env

async def search_places(query: str, limit: int = 5, zoom: int = 15):
    """
    Uses Nominatim to search places. Returns results augmented with:
      - permalink (openstreetmap.org URL with marker)
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": limit},
            headers={"User-Agent": "maps-assistant"}
        )
        results = resp.json()

    enhanced = []
    for r in results:
        osm_id = r.get("osm_id")
        lat = r.get("lat")
        lon = r.get("lon")
        # permalink with marker and center
        permalink = f"https://www.openstreetmap.org/node/{osm_id}#map={zoom}/{lat}/{lon}"

        r["permalink"] = permalink
        enhanced.append(r)

    return enhanced


async def get_directions(origin: str, destination: str):
    """
    origin and destination string format in your router: "lon,lat"
    - Calls OpenRouteService with [[lon,lat], [lon,lat]] (their expected order)
    - Returns API response + correct OpenStreetMap directions URL (which expects lat,lon order)
    """
    if not ORS_API_KEY:
        return {"error": "ORS_API_KEY not set in environment variables"}

    # origin,destination expected as "lon,lat"
    o_parts = origin.split(",")
    d_parts = destination.split(",")
    if len(o_parts) != 2 or len(d_parts) != 2:
        return {"error": "origin/destination must be 'lon,lat'"}

    o_lon, o_lat = o_parts[0].strip(), o_parts[1].strip()
    d_lon, d_lat = d_parts[0].strip(), d_parts[1].strip()

    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
    body = {
        "coordinates": [
            [float(o_lon), float(o_lat)],  # ORS expects [lon, lat]
            [float(d_lon), float(d_lat)]
        ]
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(ORS_URL, headers=headers, json=body)
        data = resp.json()

    # OSM web directions route param expects lat,lon pairs
    osm_route_link = (
        f"https://www.openstreetmap.org/directions?"
        f"engine=fossgis_osrm_car&route={o_lat},{o_lon};{d_lat},{d_lon}"
    )

    data["osm_route_permalink"] = osm_route_link
    return data
