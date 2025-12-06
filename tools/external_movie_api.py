# tools/external_movie_api.py

import os
from typing import Dict, Any

import requests
from langchain_core.tools import tool


OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # à ajouter dans ton .env plus tard
OMDB_BASE_URL = "http://www.omdbapi.com/"


@tool
def external_movie_api_tool(title: str, year: int | None = None) -> Dict[str, Any]:
    """
    Fetch movie metadata from the OMDb API.

    Use this tool when:
    - the user asks for general movie info not present in the graph,
    - or you need additional details like ratings, runtime, etc.

    Args:
        title: movie title (string)
        year: optional year to disambiguate

    Returns:
        A JSON-like dict with OMDb fields (Title, Year, Plot, etc.).
        If the API key is missing or the request fails, returns a small error dict.
    """
    if not OMDB_API_KEY:
        return {"error": "OMDB_API_KEY not configured in environment."}

    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
    }
    if year is not None:
        params["y"] = str(year)

    try:
        response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            return {"error": data.get("Error", "Movie not found.")}

        # On peut filtrer / renommer un peu les champs pour rester léger
        return {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "imdb_rating": data.get("imdbRating"),
            "genre": data.get("Genre"),
            "director": data.get("Director"),
            "actors": data.get("Actors"),
            "plot": data.get("Plot"),
            "raw": data,  # au cas où on veut tout
        }
    except Exception as e:
        return {"error": f"Request to OMDb failed: {e}"}
