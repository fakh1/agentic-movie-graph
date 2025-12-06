# tests/test_tools.py

"""
Tests unitaires simples pour les tools de bas niveau.

On veut surtout vérifier que :
- le tool Neo4j répond bien à une requête Cypher de base
- le tool vectoriel renvoie quelque chose de cohérent
"""

from tools.graph_query import graph_query_tool
from tools.vector_search import vector_search_tool


def test_graph_query_tool_inception():
    """
    Le tool Cypher doit retourner Inception avec la bonne année.
    Supposition : les données de seed contiennent ce film.
    """
    rows = graph_query_tool.invoke(
        {
            "cypher_query": """
            MATCH (m:Movie {title: 'Inception'})
            RETURN m.title AS title, m.year AS year
            """
        }
    )

    assert len(rows) == 1
    row = rows[0]
    assert row["title"] == "Inception"
    assert row["year"] == 2010


def test_graph_query_tool_counts():
    """
    Vérifie que le tool peut compter les noeuds Movie.
    """
    rows = graph_query_tool.invoke(
        {"cypher_query": "MATCH (m:Movie) RETURN count(m) AS c"}
    )
    assert len(rows) == 1
    assert rows[0]["c"] >= 1  # au moins un film dans le graphe


def test_vector_search_tool_basic():
    """
    Le tool Chroma doit renvoyer au moins un résultat pour une requête
    liée aux rêves (Inception).
    """
    results = vector_search_tool.invoke(
        {"query": "dreams inside dreams", "top_k": 3}
    )

    assert len(results) > 0
    first = results[0]
    # On vérifie que la structure de base est là
    assert "title" in first
    assert "year" in first
    assert "score" in first
    assert "content" in first
    assert "metadata" in first
