from tools.graph_query import graph_query_tool
from tools.vector_search import vector_search_tool

if __name__ == "__main__":
    # Test Neo4j tool
    print("Testing graph_query_tool...")
    rows = graph_query_tool.invoke(
        {"cypher_query": "MATCH (m:Movie) RETURN m.title AS title, m.year AS year LIMIT 5"}
    )
    print(rows)

    # Test vector search (marchera une fois qu'on aura peuplé Chroma au Stage 5)
    # print("Testing vector_search_tool...")
    # print(vector_search_tool.invoke({"query": "dream within a dream", "top_k": 3}))
