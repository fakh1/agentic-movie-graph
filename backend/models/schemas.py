# backend/models/schemas.py

from typing import Optional, Any, Dict

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    top_k: int = 5
    debug: bool = False
    return_context: bool = False


class AskResponse(BaseModel):
    question: str
    answer: str
    context: Optional[str] = None
    debug: Optional[Dict[str, Any]] = None


class GraphInfoResponse(BaseModel):
    movie_count: int
    person_count: int
    genre_count: int
    relationship_count: int
