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
      - embed_url (export/embed.html iframe URL)
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": limit},
            headers={"User-Agent": "maps-assistant"}
        )
        results = resp.json()

    enhanced = []
    # small bbox delta for embed (tweak as needed)
    delta = 0.005
    for r in results:
        lat = r.get("lat")
        lon = r.get("lon")
        # permalink with marker and center
        permalink = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map={zoom}/{lat}/{lon}"
        # embed uses bbox=minLon,minLat,maxLon,maxLat (commas must be percent-encoded in some contexts)
        min_lon = float(lon) - delta
        max_lon = float(lon) + delta
        min_lat = float(lat) - delta
        max_lat = float(lat) + delta
        # use %2C for commas in bbox and marker to be safe in HTML contexts
        bbox = f"{min_lon}%2C{min_lat}%2C{max_lon}%2C{max_lat}"
        embed_url = f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat}%2C{lon}"

        r["permalink"] = permalink
        r["embed_url"] = embed_url
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
    # simpler "to" query (OSM also supports '?to=' for destination names/coords)
    osm_to_link = f"https://www.openstreetmap.org/directions?to={d_lat},{d_lon}"

    data["osm_route_permalink"] = osm_route_link
    data["osm_to_permalink"] = osm_to_link
    return data
