# agents/retrieval.py

from typing import List, Dict, Any

from tools.vector_search import vector_search_tool
from tools.graph_query import graph_query_tool


def _build_movie_list_for_cypher(movie_ids: List[str]) -> str:
    """
    Construit une liste Cypher du style ["m1","m2","m3"].
    """
    quoted = [f'"{mid}"' for mid in movie_ids]
    return ", ".join(quoted)


def graph_enrich_movies(movie_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Pour une liste de movie_id, va chercher plus de détails dans Neo4j :
    genres, acteurs, réalisateurs.
    """
    if not movie_ids:
        return []

    ids_list = _build_movie_list_for_cypher(movie_ids)
    cypher = f"""
    MATCH (m:Movie)
    WHERE m.movie_id IN [{ids_list}]
    OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
    OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
    OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
    RETURN
        m.movie_id AS movie_id,
        m.title AS title,
        m.year AS year,
        collect(DISTINCT g.name) AS genres,
        collect(DISTINCT a.name) AS actors,
        collect(DISTINCT d.name) AS directors
    """

    rows = graph_query_tool.invoke({"cypher_query": cypher})
    return rows


def build_rag_context(
    question: str,
    vector_results: List[Dict[str, Any]],
    graph_results: List[Dict[str, Any]],
) -> str:
    """
    Assemble un contexte lisible pour le LLM à partir:
    - des matches vectoriels (Chroma)
    - des infos structurées du graphe (Neo4j)
    """
    lines: List[str] = []

    lines.append("QUESTION:")
    lines.append(question)
    lines.append("")

    # --- Partie semantic search ---
    lines.append("SEMANTIC MATCHES (from vector search):")
    if not vector_results:
        lines.append("  No semantic matches found.")
    else:
        for i, res in enumerate(vector_results, start=1):
            title = res.get("title")
            year = res.get("year")
            score = res.get("score")
            lines.append(f"{i}. {title} ({year}) [score={score:.4f}]")
            snippet = (res.get("content") or "").strip()
            if snippet:
                lines.append(f"   Snippet: {snippet[:300]}...")
            lines.append("")

    # --- Partie graph facts ---
    lines.append("")
    lines.append("GRAPH FACTS (from Neo4j):")
    if not graph_results:
        lines.append("  No graph facts found.")
    else:
        for movie in graph_results:
            genres = ", ".join(movie.get("genres") or [])
            actors = ", ".join(movie.get("actors") or [])
            directors = ", ".join(movie.get("directors") or [])
            lines.append(
                f"- {movie['title']} ({movie['year']}) "
                f"| Genres: {genres} | Directors: {directors} | Actors: {actors}"
            )

    lines.append("")
    lines.append(
        "INSTRUCTIONS: Use ONLY the information above to answer the QUESTION. "
        "If the answer is not clearly supported by the data, say you don't know."
    )

    return "\n".join(lines)


def hybrid_retrieve(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Pipeline GraphRAG:
    1) vector_search_tool pour trouver des films pertinents (semantic)
    2) graph_query_tool pour récupérer les détails (graph)
    3) construction d'un contexte RAG pour le LLM
    """
    # 1) Semantic search (Chroma)
    vector_results: List[Dict[str, Any]] = vector_search_tool.invoke(
        {"query": question, "top_k": top_k}
    )

    # 2) Graph enrichment (Neo4j)
    movie_ids = [
        r.get("movie_id")
        for r in vector_results
        if r.get("movie_id") is not None
    ]
    graph_results = graph_enrich_movies(movie_ids)

    # 3) Context assembly
    context = build_rag_context(question, vector_results, graph_results)

    return {
        "question": question,
        "vector_results": vector_results,
        "graph_results": graph_results,
        "context": context,
    }
