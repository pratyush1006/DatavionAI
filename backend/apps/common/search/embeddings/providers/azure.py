"""
Azure OpenAI embedding provider.
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


class AzureEmbeddingProvider(
    BaseEmbeddingProvider,
):
    """
    Azure OpenAI embedding provider.

    Enterprise provider for:

    - Azure OpenAI Service
    - Private deployments
    - Managed identity authentication
    - Healthcare AI workloads
    """

    name = "azure"

    model = ""

    dimensions: int | None = None

    supports_batch = True

    def embed(
        self,
        *,
        text: str,
        **kwargs: Any,
    ) -> EmbeddingVector:
        """
        Generate a single embedding vector.
        """

        raise NotImplementedError("Azure OpenAI embedding integration pending.")

    def embed_batch(
        self,
        *,
        texts: list[str],
        **kwargs: Any,
    ) -> EmbeddingBatch:
        """
        Generate multiple embedding vectors.
        """

        raise NotImplementedError("Azure OpenAI batch embedding integration pending.")


__all__: tuple[str, ...] = ("AzureEmbeddingProvider",)
