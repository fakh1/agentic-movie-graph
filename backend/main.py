# backend/main.py

from fastapi import FastAPI

from backend.routers.ask import router as ask_router
from backend.routers.graph_info import router as graph_info_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Agentic Movie Graph API",
        description="Agentic + GraphRAG backend for the movie knowledge graph.",
        version="0.1.0",
    )

    # Routers
    app.include_router(ask_router, prefix="/api")
    app.include_router(graph_info_router, prefix="/api")

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
