import requests
from pydantic import Field


class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints and descriptions

    def get_places(
        self,
        query: str = Field(
            ...,
            description="The search query for the place, e.g., 'Eiffel Tower', 'restaurant in Paris', or '1600 Amphitheatre Pkwy, Mountain View, CA'.",
        ),
    ) -> dict:
        """
        Searches for places, landmarks, or addresses using a text query. This is useful for finding locations to be used as origins or destinations. Returns a list of potential places with their coordinates.
        """
        url = "http://host.docker.internal:8000/places"
        params = {"query": query}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_directions(
        self,
        origin: str = Field(
            ...,
            description="The starting point for the directions, e.g., 'Eiffel Tower' or a specific address.",
        ),
        destination: str = Field(
            ...,
            description="The destination for the directions, e.g., 'Louvre Museum' or '123 Main Street'.",
        ),
    ) -> dict:
        """
        Calculates driving directions between a specified origin and destination. The tool first finds the coordinates for the origin and destination and then uses them to get the driving route.
        """

        def _get_coords(query):
            url = "http://host.docker.internal:8000/places"
            params = {"query": query}
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data["results"]:
                raise ValueError(f"Could not find coordinates for: {query}")
            result = data["results"][0]
            # The FastAPI /places endpoint returns lat,lon. The /directions endpoint needs lon,lat.
            return f"{result['lon']},{result['lat']}"

        try:
            origin_coords = _get_coords(origin)
            destination_coords = _get_coords(destination)
        except ValueError as e:
            return {"error": str(e)}

        directions_url = "http://host.docker.internal:8000/directions"
        params = {"origin": origin_coords, "destination": destination_coords}
        response = requests.get(directions_url, params=params)
        response.raise_for_status()
        return response.json()
