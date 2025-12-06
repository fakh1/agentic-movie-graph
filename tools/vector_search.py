# tools/vector_search.py

import os
from typing import List, Dict, Any

from langchain_core.tools import tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Chroma config ---
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "data/chroma_movies")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "movie_descriptions")

_embeddings = None
_vectorstore = None


def get_embeddings():
    """
    Embeddings gratuits via Sentence Transformers (HuggingFace).
    Aucun besoin d'API key.
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings


def get_vectorstore():
    """
    Initialise Chroma sur le dossier déjà rempli par build_vector_index.py.
    """
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=get_embeddings(),
            persist_directory=CHROMA_DB_DIR,
        )
    return _vectorstore


@tool
def vector_search_tool(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Semantic search over movie descriptions and metadata.

    Args:
        query: natural language query.
        top_k: number of results to return.

    Returns:
        A list of dicts, each containing:
        - movie_id
        - title
        - year
        - score (similarity)
        - content (text chunk)
        - metadata (full metadata)
    """
    vs = get_vectorstore()

    docs_and_scores = vs.similarity_search_with_score(query, k=top_k)

    results: List[Dict[str, Any]] = []
    for doc, score in docs_and_scores:
        meta = doc.metadata or {}
        results.append(
            {
                "movie_id": meta.get("movie_id"),
                "title": meta.get("title"),
                "year": meta.get("year"),
                "score": float(score),
                "content": doc.page_content,
                "metadata": meta,
            }
        )

    return results
