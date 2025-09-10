from fastapi import APIRouter, Query, Request
from app.utils import search_places, get_directions
from app.core import limiter, logger

router = APIRouter()

@router.get("/ping")
@limiter.limit("5/minute")
async def ping(request: Request):
    logger.info("Ping endpoint called")
    return {"status": "ok"}

@router.get("/places")
@limiter.limit("20/minute")
async def places(request: Request, query: str = Query(..., description="Search for places")):
    logger.info(f"/places requested with query: {query}")
    results = await search_places(query)
    return {"results": results}

@router.get("/directions")
@limiter.limit("15/minute")
async def directions(
    request: Request,
    origin: str = Query(..., description="Origin coordinates 'lon,lat'"),
    destination: str = Query(..., description="Destination coordinates 'lon,lat'")
):
    logger.info(f"/directions requested with origin={origin}, destination={destination}")
    results = await get_directions(origin, destination)
    return results
