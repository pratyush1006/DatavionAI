"""
DatavionOS Embedding Service.

Application-facing service layer for embedding operations.

Responsibilities:

- Provider-independent embedding generation
- Provider validation
- Metadata exposure
- Future telemetry hooks
- AI usage tracking integration

Applications should use this service instead of directly
calling embedding providers.
"""

from __future__ import annotations

from typing import Any

from apps.common.search.embeddings.engine import (
    embedding_engine,
)
from apps.common.search.embeddings.registry import (
    has_embedding_provider,
)
from apps.common.search.embeddings.types import (
    EmbeddingBatch,
    EmbeddingMetadata,
    EmbeddingVector,
)


class EmbeddingService:
    """
    High-level embedding operations service.
    """

    def embed(
        self,
        *,
        text: str,
        provider: str = "openai",
        **kwargs: Any,
    ) -> EmbeddingVector:
        """
        Generate embedding vector.

        Raises
        ------
        LookupError
            If provider is not registered.
        """

        self.validate_provider(
            provider,
        )

        return embedding_engine.embed(
            text=text,
            provider=provider,
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
        Generate batch embeddings.
        """

        self.validate_provider(
            provider,
        )

        return embedding_engine.embed_batch(
            texts=texts,
            provider=provider,
            **kwargs,
        )

    def validate_provider(
        self,
        provider: str,
    ) -> None:
        """
        Validate embedding provider availability.
        """

        if not has_embedding_provider(
            provider,
        ):
            raise LookupError(f"Unknown embedding provider '{provider}'.")

    def metadata(
        self,
        provider: str = "openai",
    ) -> EmbeddingMetadata:
        """
        Return provider metadata.
        """

        self.validate_provider(
            provider,
        )

        instance = embedding_engine.get_provider(
            provider,
        )

        return instance.metadata()


embedding_service = EmbeddingService()


__all__: tuple[str, ...] = (
    "EmbeddingService",
    "embedding_service",
)
