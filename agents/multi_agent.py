# agents/multi_agent.py

from typing import Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage

from backend.dependencies import get_llm
from agents.retrieval import hybrid_retrieve


def answer_agent(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Premier agent : utilise GraphRAG pour produire une réponse initiale.
    """
    rag_result = hybrid_retrieve(question, top_k=top_k)
    context = rag_result["context"]

    system_prompt = (
        "You are an assistant answering questions about movies using the context. "
        "Be concise but informative."
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=(
                "CONTEXT:\n"
                f"{context}\n\n"
                "Using ONLY this context, answer the QUESTION at the top."
            )
        ),
    ]

    llm = get_llm()
    resp = llm.invoke(messages)

    return {
        "answer": resp.content,
        "rag_result": rag_result,
    }


def critic_agent(question: str, draft_answer: str, context: str) -> str:
    """
    Second agent : lit la question, le contexte et la réponse initiale.
    Son rôle est de :
    - vérifier la cohérence
    - corriger si besoin
    - améliorer la formulation
    """
    system_prompt = (
        "You are a critical reviewer. "
        "Your job is to check if the answer is correct and well written "
        "given the context. If it's correct, you may slightly improve the wording. "
        "If it's incomplete or slightly wrong, fix it using ONLY the context."
    )

    content = (
        f"QUESTION:\n{question}\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"INITIAL ANSWER:\n{draft_answer}\n\n"
        "Now provide a FINAL ANSWER that is accurate and well written."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=content),
    ]

    llm = get_llm()
    resp = llm.invoke(messages)
    return resp.content


def answer_with_critique(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Orchestrateur multi-agent :
    1) Answerer produit une réponse initiale
    2) Critic relit et améliore
    3) On renvoie la réponse finale + debug
    """
    # Agent 1 : answerer
    answer_result = answer_agent(question, top_k=top_k)
    draft_answer = answer_result["answer"]
    context = answer_result["rag_result"]["context"]

    # Agent 2 : critic
    final_answer = critic_agent(question, draft_answer, context)

    return {
        "question": question,
        "draft_answer": draft_answer,
        "final_answer": final_answer,
        "context": context,
        "rag_debug": {
            "vector_results": answer_result["rag_result"]["vector_results"],
            "graph_results": answer_result["rag_result"]["graph_results"],
        },
    }
