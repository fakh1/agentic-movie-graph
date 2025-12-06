# backend/dependencies.py

from functools import lru_cache

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from backend.config import settings


@lru_cache
def get_llm():
    """
    Local LLM via Ollama.
    Assure-toi que le modèle est installé:
      ollama pull llama3.2
    """
    return ChatOllama(
        model=settings.OLLAMA_MODEL,
        temperature=0.1,
    )


def build_llm_messages(context: str):
    """
    Construit les messages pour le LLM à partir du contexte RAG.
    On encode la question + contexte dans un HumanMessage.
    """
    system_prompt = (
        "You are a helpful assistant that answers questions about movies. "
        "Use ONLY the information in the context. "
        "If the answer is not clearly supported, say you don't know."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=(
                "Here is the context for the question:\n\n"
                f"{context}\n\n"
                "Answer the QUESTION at the top of the context."
            )
        ),
    ]
    return messages
