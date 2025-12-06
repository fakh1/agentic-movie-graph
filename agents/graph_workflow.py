# agents/graph_workflow.py

from typing import List

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from agents.state import AgentState
from agents.prompts import SYSTEM_PROMPT

# Tools (implémentés dans /tools, Stage 4)
# Ils devront être des LangChain tools (ou compatibles)
from tools.vector_search import vector_search_tool
from tools.graph_query import graph_query_tool
from tools.external_movie_api import external_movie_api_tool


def get_llm():
    """
    LLM local gratuit via Ollama (llama3.2).
    Assure-toi d'avoir lancé : `ollama pull llama3.2`
    puis `ollama run llama3.2` une fois pour init.
    """
    return ChatOllama(
        model="llama3.2",  # adapte au nom exact du modèle sur ta machine
        temperature=0.1,
    )



# Liste des tools exposés à l'agent
TOOLS = [vector_search_tool, graph_query_tool, external_movie_api_tool]


def assistant_node(state: AgentState) -> AgentState:
    """
    Main reasoning node.
    - Lit l'historique des messages
    - Choisit éventuellement d'appeler un ou plusieurs tools (via function calling)
    - Produit soit un tool-call, soit une réponse finale
    """
    llm = get_llm().bind_tools(TOOLS)

    # On suppose que le dernier message est la dernière question / étape
    messages = state["messages"]

    # Ajout du system prompt au début du dialogue
    if not messages or messages[0].type != "system":
        messages = [HumanMessage(role="system", content=SYSTEM_PROMPT)] + messages

    response = llm.invoke(messages)

    # Ajout de la réponse dans l'historique
    new_messages: List = [response]

    # Si le modèle renvoie une réponse finale (sans tool-calls),
    # on remplit final_answer pour que le backend puisse la récupérer.
    final_answer = None
    if isinstance(response, AIMessage) and not response.tool_calls:
        final_answer = response.content

    return {
        "messages": new_messages,
        "final_answer": final_answer,
        # On ne modifie pas les autres champs du state ici
    }


def build_workflow():
    """
    Construit et compile le workflow LangGraph.
    Schéma:
        assistant -> (si tools) tools -> assistant -> ... -> END
    """
    workflow = StateGraph(AgentState)

    # Nœuds
    workflow.add_node("assistant", assistant_node)
    workflow.add_node("tools", ToolNode(TOOLS))

    # Point d'entrée
    workflow.set_entry_point("assistant")

    # Si l'agent a demandé un tool, on va au nœud 'tools', sinon END
    workflow.add_conditional_edges(
        "assistant",
        tools_condition,  # renvoie "tools" s'il y a un tool_call, sinon END
    )

    # Une fois le tool exécuté, on renvoie le résultat à l'assistant
    workflow.add_edge("tools", "assistant")

    # END est géré automatiquement par tools_condition
    return workflow.compile()


# Petit helper pratique pour le backend ou pour des tests rapides
def run_query_with_workflow(question: str):
    """
    Helper for local testing of the graph workflow.
    """
    app = build_workflow()
    initial_state: AgentState = {
        "user_query": question,
        "messages": [HumanMessage(content=question)],
        "retrieved_docs": None,
        "graph_results": None,
        "final_answer": None,
    }
    return app.invoke(initial_state)
