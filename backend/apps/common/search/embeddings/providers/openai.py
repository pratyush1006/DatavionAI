"""
OpenAI embedding provider.
"""

from __future__ import annotations

from typing import Any

from apps.common.search.embeddings.base import (
    BaseEmbeddingProvider,
)
from apps.common.search.embeddings.types import (
    EmbeddingBatch,
    EmbeddingVector,
)


class OpenAIEmbeddingProvider(
    BaseEmbeddingProvider,
):
    """Production OpenAI embedding adapter backed by the shared AI client."""

    name = "openai"

    model = "text-embedding-3-large"

    dimensions = 3072

    supports_batch = True

    def embed(
        self,
        *,
        text: str,
        **kwargs: Any,
    ) -> EmbeddingVector:
        """Generate one embedding with the configured OpenAI deployment."""
        model = kwargs.pop("model", None) or self.model
        provider = self._provider(kwargs.pop("api_key", None))
        return provider.embed([text], model)[0]

    def embed_batch(
        self,
        *,
        texts: list[str],
        **kwargs: Any,
    ) -> EmbeddingBatch:
        """Generate embeddings for a batch of texts."""
        model = kwargs.pop("model", None) or self.model
        provider = self._provider(kwargs.pop("api_key", None))
        return provider.embed(texts, model)

    @staticmethod
    def _provider(api_key: str | None = None):
        """Reuse the shared provider implementation and its timeout controls."""
        from apps.ai.providers.implementation.embeddings import (
            OpenAIEmbeddingProvider as AIEmbeddingProvider,
        )

        return AIEmbeddingProvider(api_key=api_key)


__all__: tuple[str, ...] = ("OpenAIEmbeddingProvider",)
