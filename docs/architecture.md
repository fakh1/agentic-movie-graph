# Architecture – Agentic Movie Graph 🎬

Ce document décrit l’architecture complète du projet :

- Knowledge graph Neo4j
- Pipeline GraphRAG (hybrid retrieval)
- Tools (Neo4j / Chroma / API)
- Workflow agentique (LangGraph + multi-agent)
- Backend FastAPI
- Stratégie de tests

---

## 1. Objectif du système

L’objectif est de construire un **mini système agentique** capable de :

1. Comprendre une question utilisateur sur des films
2. Combiner :
   - **recherche vectorielle** dans un index de descriptions de films
   - **traversée de graphe** dans Neo4j (Cypher)
3. Assembler un **contexte RAG** structuré
4. Utiliser un **LLM local (Ollama + Llama)** pour rédiger la réponse
5. Exposer ce pipeline via une **API FastAPI** + un **CLI**

Le tout sans dépendre d’API payantes.

---

## 2. Vue d’ensemble

```mermaid
flowchart LR
    User[User / CLI / HTTP client]
    User -->|HTTP| FastAPI

    subgraph Backend[FastAPI Backend]
        ASK[/POST /api/ask/]
        GRAPHINFO[/GET /api/graph/info/]
    end

    FastAPI -->|call| GraphRAG[GraphRAG Pipeline\n(agents/retrieval.py)]
    GraphRAG -->|vector_search_tool| Chroma[(Chroma\nVector DB)]
    GraphRAG -->|graph_query_tool| Neo4j[(Neo4j\nMovie Graph)]
    GraphRAG --> Context[Context RAG\n(string)]

    Context --> LLM[Local LLM\n(Ollama + Llama)]
    LLM --> FastAPI

Composants principaux :

Neo4j : knowledge graph structuré

Chroma + embeddings : index vectoriel des films

GraphRAG : combine Neo4j + Chroma

LLM local : modèle Ollama pour la génération de texte

FastAPI : point d’entrée HTTP

CLI : client texte simple par-dessus l’API 
