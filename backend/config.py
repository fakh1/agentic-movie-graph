# backend/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Global configuration for the backend.
    Values can be overridden via environment variables or a .env file,
    but defaults are chosen for local dev.
    """

    # Neo4j
    NEO4J_URI: str = "neo4j://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j123"

    # Chroma
    CHROMA_DB_DIR: str = "data/chroma_movies"
    CHROMA_COLLECTION_NAME: str = "movie_descriptions"

    # Local LLM (via Ollama)
    OLLAMA_MODEL: str = "llama3.2"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
