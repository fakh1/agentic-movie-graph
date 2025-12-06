# Agentic Movie Graph 🎬  
_Tanit AI – Generative AI Internship Assignment_

Ce projet est un mini système **Agentic + GraphRAG** autour d’un petit graphe de films.  
Il montre comment :

- interroger un **knowledge graph Neo4j**
- combiner **recherche vectorielle + graph traversal** (GraphRAG)
- orchestrer des **tools** dans un pipeline agentique
- exposer le tout via une **API FastAPI** et un **CLI**
- utiliser un **LLM local (Ollama)** → pas besoin de clé API payante

---

## 1. Features & Deliverables

### 1. GitHub Repository

Le repo contient :

- ✅ Agent code (LangGraph + custom pipeline)
- ✅ Tool implementations (`tools/`)
- ✅ GraphRAG pipeline (`agents/retrieval.py`)
- ✅ Backend FastAPI (`backend/`)
- ✅ CLI simple (`cli/chat_cli.py`)
- ✅ README détaillé (ce fichier)

### 2. Knowledge Graph (Neo4j)

- ✅ Scripts Cypher pour créer le graphe :
  - `graph/schema.cypher`
  - `graph/seed_data.cypher`
- ✅ Schéma documenté + diagramme Mermaid (section [3.2](#32-diagramme-de-schéma))

### 3. Agentic Workflow

- ✅ Workflow agentique (LangGraph + multi-agent) :
  - `agents/graph_workflow.py`
  - `agents/multi_agent.py`
- ✅ Tools définis dans `tools/`
- ✅ Logs de tool usage via :
  - `test_hybrid_retrieval.py`
  - `tests/test_api.py` (avec `debug=true` dans `/api/ask`)

### 4. GraphRAG Pipeline

- ✅ Hybrid retrieval (vector + graph) dans `agents/retrieval.py`
- ✅ Construction de contexte RAG lisible
- ✅ Exemples de requêtes et résultats (via `/api/ask` + tests)

### 5. Backend API (FastAPI)

- ✅ App FastAPI : `backend/main.py`
- ✅ Routers & modèles Pydantic :
  - `backend/routers/ask.py` → `/api/ask`
  - `backend/routers/graph_info.py` → `/api/graph/info`
  - `backend/models/schemas.py`
- ✅ Exemples cURL / Postman (section [7](#7-exemples-de-requêtes-api))

### 6. Frontend / CLI (optional)

- ✅ CLI minimal :
  - `cli/chat_cli.py`
  - permet de chatter avec l’API `/api/ask` depuis le terminal

### 7. Documentation

- ✅ Ce README (setup + usage)
- ✅ `graph/README.md` → graph design & Cypher
- ✅ `docs/architecture.md` → architecture, workflow, tools, pipeline & tests
- ✅ `docs/demo_script.md` → script détaillé pour la vidéo de démo

### 8. Demo Video (à faire à partir du code)

Le code + `docs/demo_script.md` permettent de tourner une vidéo 5–10 min montrant :

- les objectifs du système
- le fonctionnement de l’agent
- les requêtes Neo4j / tools en action
- le pipeline GraphRAG end-to-end
- l’architecture globale

---

## 2. Stack & Project Structure

### 2.1. Technologies principales

- **Python 3.11**
- **Neo4j** (Desktop / Local DB)
- **Chroma** (Vector DB)
- **HuggingFace embeddings** `sentence-transformers/all-MiniLM-L6-v2`
- **Ollama + Llama (ex: llama3.2)** → LLM local, gratuit
- **FastAPI** + **Uvicorn**
- **LangChain / LangGraph**
- **Pytest** pour les tests

### 2.2. Structure du repo

```bash
agentic-movie-graph/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings (Neo4j, Chroma, LLM)
│   ├── dependencies.py         # LLM factory, message builders
│   ├── routers/
│   │   ├── ask.py              # /api/ask endpoint
│   │   └── graph_info.py       # /api/graph/info endpoint
│   └── models/
│       └── schemas.py          # Pydantic schemas
│
├── agents/
│   ├── graph_workflow.py       # LangGraph workflow (agent + tools)
│   ├── state.py                # AgentState dataclass
│   ├── prompts.py              # System + tool prompts
│   ├── retrieval.py            # GraphRAG pipeline (hybrid_retrieve)
│   └── multi_agent.py          # Answerer + Critic agents
│
├── tools/
│   ├── vector_search.py        # Chroma + HuggingFace embeddings
│   ├── graph_query.py          # Cypher tool (Neo4j)
│   └── external_movie_api.py   # OMDb API wrapper (optionnel)
│
├── graph/
│   ├── schema.cypher           # Constraints / indexes / labels
│   ├── seed_data.cypher        # Sample data (movies, people, genres)
│   ├── build_vector_index.py   # Construct & persist Chroma index
│   └── README.md               # Graph schema & examples
│
├── cli/
│   └── chat_cli.py             # Simple CLI chat over /api/ask
│
├── tests/
│   ├── test_tools.py           # unit tests for tools
│   ├── test_agent_flow.py      # tests for GraphRAG + multi-agent
│   └── test_api.py             # tests for FastAPI endpoints
│
├── docs/
│   ├── architecture.md         # Detailed architecture & reasoning
│   ├── diagrams/               # Place for exported PNG/SVG
│   └── demo_script.md          # Script for demo video
│
├── README.md                   # (ce fichier)
├── requirements.txt
└── .env.example                # Example env vars (optionnel)
