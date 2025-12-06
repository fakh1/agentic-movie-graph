# backend/routers/graph_info.py

from fastapi import APIRouter

from backend.models.schemas import GraphInfoResponse
from tools.graph_query import graph_query_tool

router = APIRouter(tags=["graph"], prefix="/graph")


@router.get("/info", response_model=GraphInfoResponse)
async def get_graph_info():
    """
    Retourne quelques stats sur le graphe Neo4j.
    """
    movies = graph_query_tool.invoke(
        {"cypher_query": "MATCH (m:Movie) RETURN count(m) AS count"}
    )
    persons = graph_query_tool.invoke(
        {"cypher_query": "MATCH (p:Person) RETURN count(p) AS count"}
    )
    genres = graph_query_tool.invoke(
        {"cypher_query": "MATCH (g:Genre) RETURN count(g) AS count"}
    )
    rels = graph_query_tool.invoke(
        {"cypher_query": "MATCH ()-[r]->() RETURN count(r) AS count"}
    )

    movie_count = movies[0]["count"] if movies else 0
    person_count = persons[0]["count"] if persons else 0
    genre_count = genres[0]["count"] if genres else 0
    relationship_count = rels[0]["count"] if rels else 0

    return GraphInfoResponse(
        movie_count=movie_count,
        person_count=person_count,
        genre_count=genre_count,
        relationship_count=relationship_count,
    )
