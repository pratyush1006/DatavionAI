"""
Default AI provider wiring.

Assembles the concrete chat, embedding, vector store, prompt engine and RAG
engine into an :class:`AIServices` collection. Designed to be swappable so
alternative providers can be injected without touching call sites.
"""

from __future__ import annotations

from typing import Any

from apps.datavionos.ai.implementation.chat import OpenAIChatModel
from apps.datavionos.ai.implementation.embeddings import OpenAIEmbeddingModel
from apps.datavionos.ai.implementation.prompt_engine import JinjaPromptEngine
from apps.datavionos.ai.implementation.rag_engine import SimpleRAGEngine
from apps.datavionos.ai.implementation.vector_store import PostgresVectorStore
from apps.datavionos.ai.services import AIServices


def build_ai_services(
    *,
    organization_id: Any | None = None,
    chat_model: str = "gpt-4o-mini",
    embedding_model: str = "text-embedding-3-small",
) -> AIServices:
    """
    Build the concrete AI service collection.
    """

    chat = OpenAIChatModel(model=chat_model)
    embeddings = OpenAIEmbeddingModel(model=embedding_model)
    vector_store = PostgresVectorStore(organization_id=organization_id)
    prompts = JinjaPromptEngine(organization_id=organization_id)
    rag = SimpleRAGEngine(
        chat=chat,
        embeddings=embeddings,
        vector_store=vector_store,
        prompts=prompts,
    )

    return AIServices(
        provider=None,  # type: ignore[arg-type]
        chat=chat,
        embeddings=embeddings,
        prompts=prompts,
        vector_store=vector_store,
        rag=rag,
    )


__all__ = [
    "build_ai_services",
]
