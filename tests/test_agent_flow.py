# tests/test_agent_flow.py

"""
Tests de haut niveau pour le pipeline agentique:

- hybrid_retrieve (GraphRAG : vector + graph + contexte)
- answer_with_critique (multi-agent : answerer + critic)
"""

from agents.retrieval import hybrid_retrieve
from agents.multi_agent import answer_with_critique


def test_hybrid_retrieve_nolan_scifi():
    """
    S1 – 'Give me a sci-fi movie directed by Christopher Nolan.'
    Le pipeline GraphRAG doit trouver au moins un film sci-fi
    réalisé par Nolan (Inception ou Interstellar) dans les résultats graph.
    """
    question = "Give me a sci-fi movie directed by Christopher Nolan."
    result = hybrid_retrieve(question, top_k=3)

    # Le résultat doit contenir les clés de base
    assert "vector_results" in result
    assert "graph_results" in result
    assert "context" in result

    assert len(result["vector_results"]) > 0
    assert len(result["graph_results"]) > 0

    titles = {m["title"] for m in result["graph_results"]}
    assert "Inception" in titles or "Interstellar" in titles


def test_hybrid_retrieve_context_not_empty():
    """
    Vérifie que le contexte construit par hybrid_retrieve n'est pas vide
    et contient la QUESTION.
    """
    question = "Which movies in the graph are sci-fi and who directed them?"
    result = hybrid_retrieve(question, top_k=3)

    context = result["context"]
    assert isinstance(context, str)
    assert "QUESTION:" in context
    assert question in context


def test_multi_agent_answer_with_critique():
    """
    Teste le pipeline multi-agent answer_with_critique :
    - doit produire un draft_answer
    - doit produire un final_answer non vide
    """
    question = "Which movies in the graph are sci-fi and who directed them?"
    result = answer_with_critique(question, top_k=3)

    draft = result.get("draft_answer", "")
    final = result.get("final_answer", "")

    assert draft
    assert final
    # Le final doit être au moins aussi informatif que le draft, mais on ne
    # teste pas la formulation exacte pour laisser de la liberté au LLM.
