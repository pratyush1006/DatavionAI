"""
AI service contracts.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.ai.chat import (
    ChatModel,
)
from apps.datavionos.ai.embeddings import (
    EmbeddingModel,
)
from apps.datavionos.ai.prompt import (
    PromptEngine,
)
from apps.datavionos.ai.provider import (
    AIProvider,
)
from apps.datavionos.ai.rag import (
    RAGEngine,
)
from apps.datavionos.ai.vector_store import (
    VectorStore,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AIServices:
    """
    AI service collection.
    """

    provider: AIProvider

    chat: ChatModel

    embeddings: EmbeddingModel

    prompts: PromptEngine

    vector_store: VectorStore

    rag: RAGEngine


__all__ = [
    "AIServices",
]
