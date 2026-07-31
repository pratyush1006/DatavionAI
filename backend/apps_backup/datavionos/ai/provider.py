"""
AI provider contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.ai.chat import (
    ChatModel,
)
from apps.datavionos.ai.embeddings import (
    EmbeddingModel,
)
from apps.datavionos.ai.prompt import (
    PromptEngine,
)
from apps.datavionos.ai.rag import (
    RAGEngine,
)
from apps.datavionos.ai.vector_store import (
    VectorStore,
)


@runtime_checkable
class AIProvider(
    Protocol,
):
    """
    Root AI provider contract.
    """

    @property
    def chat(
        self,
    ) -> ChatModel:
        """
        Return the chat model.
        """

    @property
    def embeddings(
        self,
    ) -> EmbeddingModel:
        """
        Return the embedding model.
        """

    @property
    def prompts(
        self,
    ) -> PromptEngine:
        """
        Return the prompt engine.
        """

    @property
    def vector_store(
        self,
    ) -> VectorStore:
        """
        Return the vector store.
        """

    @property
    def rag(
        self,
    ) -> RAGEngine:
        """
        Return the retrieval-augmented generation engine.
        """


__all__ = [
    "AIProvider",
]
