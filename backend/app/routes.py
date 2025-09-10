from fastapi import APIRouter, Query
from app.utils import search_places, get_directions

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok"}

@router.get("/places")
async def places(query: str = Query(..., description="Search for places")):
    results = await search_places(query)
    return results

@router.get("/directions")
async def directions(
    origin: str = Query(..., description="Origin coordinates 'lon,lat'"),
    destination: str = Query(..., description="Destination coordinates 'lon,lat'")
):
    results = await get_directions(origin, destination)
    return results
