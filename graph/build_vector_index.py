# graph/build_vector_index.py

from typing import List

from neo4j import GraphDatabase, basic_auth
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# --- Neo4j config (mêmes valeurs que dans tools/graph_query.py) ---
NEO4J_URI = "neo4j://localhost:7687"  # adapte si tu utilises bolt://localhost:7687
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j123"

# --- Chroma config ---
CHROMA_DB_DIR = "data/chroma_movies"
CHROMA_COLLECTION_NAME = "movie_descriptions"


def get_neo4j_driver():
    """Create a Neo4j driver for the local DB."""
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD),
    )


def fetch_movies() -> List[dict]:
    """
    Récupère les films et leur contexte (genres, acteurs, réalisateurs)
    depuis Neo4j pour construire les textes à embedder.
    """
    driver = get_neo4j_driver()
    cypher = """
    MATCH (m:Movie)
    OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
    OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
    OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
    RETURN
        m.movie_id AS movie_id,
        m.title AS title,
        m.year AS year,
        m.description AS description,
        collect(DISTINCT g.name) AS genres,
        collect(DISTINCT a.name) AS actors,
        collect(DISTINCT d.name) AS directors
    """

    with driver.session() as session:
        result = session.run(cypher)
        movies = [record.data() for record in result]

    return movies


def build_documents(movies: List[dict]) -> List[Document]:
    """
    Transforme chaque film en un Document riche pour la recherche sémantique.
    """
    docs: List[Document] = []

    for movie in movies:
        genres_list = movie.get("genres") or []
        actors_list = movie.get("actors") or []
        directors_list = movie.get("directors") or []

        genres = ", ".join(genres_list)
        actors = ", ".join(actors_list)
        directors = ", ".join(directors_list)
        description = movie.get("description") or ""

        text = f"""Title: {movie['title']}
Year: {movie['year']}
Genres: {genres}
Directors: {directors}
Actors: {actors}

Description:
{description}
"""

        # IMPORTANT : Chroma n'accepte que des types simples en metadata
        metadata = {
            "movie_id": movie["movie_id"],
            "title": movie["title"],
            "year": movie["year"],
            "genres": genres,        # string, plus liste
            "actors": actors,        # string
            "directors": directors,  # string
        }

        docs.append(Document(page_content=text, metadata=metadata))

    return docs


def build_vector_index():
    print("🔄 Fetching movies from Neo4j...")
    movies = fetch_movies()
    print(f"✅ Retrieved {len(movies)} movies")

    print("📝 Building documents...")
    docs = build_documents(movies)

    print("🧠 Initializing embeddings & Chroma (HuggingFace, free)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_DB_DIR,
    )

    vectorstore.persist()
    print(f"✅ Vector index built and persisted in '{CHROMA_DB_DIR}'")


if __name__ == "__main__":
    build_vector_index()
