# tools/graph_query.py

from typing import List, Dict

from neo4j import GraphDatabase, basic_auth
from langchain_core.tools import tool

# --- Neo4j driver (config locale, sans .env) ---

# ⚠️ Si tu changes le port ou le mot de passe dans Neo4j Desktop,
# il faudra mettre à jour ces valeurs ici.
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j123"

_driver = None


def get_neo4j_driver():
    """
    Create (or reuse) a global Neo4j driver.
    Config is hardcoded for local development.
    """
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD),
        )
    return _driver


@tool
def graph_query_tool(cypher_query: str) -> List[Dict]:
    """
    Run a read-only Cypher query against the movie knowledge graph.

    Use this tool when the question is about:
    - listing movies / actors / directors / genres
    - filtering by year, genre, person, etc.

    Returns a list of dictionaries (one per row).
    """
    driver = get_neo4j_driver()

    lowered = cypher_query.strip().lower()
    if lowered.startswith(("create", "merge", "delete", "drop", "set")):
        raise ValueError(
            "graph_query_tool is read-only. Use only MATCH / RETURN style queries."
        )

    with driver.session() as session:
        result = session.run(cypher_query)
        rows = [record.data() for record in result]

    return rows
