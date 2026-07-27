"""
DatavionOS Embedding Engine.

High-level orchestration layer for embedding generation.

Applications should use this service instead of
direct provider implementations.
"""

from __future__ import annotations

from typing import Any

from .registry import (
    get_embedding_provider,
)
from .types import (
    EmbeddingBatch,
    EmbeddingVector,
)


class EmbeddingEngine:
    """
    Provider-independent embedding engine.
    """

    def get_provider(
        self,
        name: str,
    ):
        """
        Return embedding provider instance.
        """

        provider_class = get_embedding_provider(
            name,
        )

        return provider_class()

    def embed(
        self,
        *,
        text: str,
        provider: str = "openai",
        **kwargs: Any,
    ) -> EmbeddingVector:
        """
        Generate a single embedding.
        """

        embedding_provider = self.get_provider(
            provider,
        )

        return embedding_provider.embed(
            text=text,
            **kwargs,
        )

    def embed_batch(
        self,
        *,
        texts: list[str],
        provider: str = "openai",
        **kwargs: Any,
    ) -> EmbeddingBatch:
        """
        Generate multiple embeddings.
        """

        embedding_provider = self.get_provider(
            provider,
        )

        return embedding_provider.embed_batch(
            texts=texts,
            **kwargs,
        )


embedding_engine = EmbeddingEngine()


__all__: tuple[str, ...] = (
    "EmbeddingEngine",
    "embedding_engine",
)
