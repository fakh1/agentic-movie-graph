# agents/state.py
from typing import Annotated, TypedDict, List, Dict, Optional
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage


class AgentState(TypedDict):
    """
    Global state of the agent.
    - messages: conversation history (used by LangGraph)
    - user_query: original user question
    - retrieved_docs: results from vector search
    - graph_results: results from Neo4j Cypher queries
    - final_answer: last answer returned to the user
    """
    messages: Annotated[List[AnyMessage], add_messages]
    user_query: str
    retrieved_docs: Optional[List[Dict]]
    graph_results: Optional[List[Dict]]
    final_answer: Optional[str]
