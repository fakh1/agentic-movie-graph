# backend/routers/ask.py

from fastapi import APIRouter

from backend.models.schemas import AskRequest, AskResponse
from backend.dependencies import get_llm, build_llm_messages
from agents.retrieval import hybrid_retrieve

router = APIRouter(tags=["qa"], prefix="/ask")


@router.post("", response_model=AskResponse)
async def ask_question(payload: AskRequest):
    """
    Endpoint principal pour poser une question sur les films.
    Utilise le pipeline GraphRAG (hybrid_retrieve) + LLM local (Ollama).
    """
    # 1) Récupération hybride (vector + graph)
    rag_result = hybrid_retrieve(
        question=payload.question,
        top_k=payload.top_k,
    )

    context = rag_result["context"]

    # 2) Appel du LLM local
    llm = get_llm()
    messages = build_llm_messages(context)
    llm_response = llm.invoke(messages)

    # 3) Construction de la réponse API
    debug_data = None
    if payload.debug:
        debug_data = {
            "vector_results": rag_result["vector_results"],
            "graph_results": rag_result["graph_results"],
        }

    return AskResponse(
        question=payload.question,
        answer=llm_response.content,
        context=context if payload.return_context else None,
        debug=debug_data,
    )
