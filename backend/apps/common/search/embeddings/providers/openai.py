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
    """
    OpenAI embedding provider.

    Future integration:

    - OpenAI Embeddings API
    - Azure OpenAI compatible mode
    - Batch embedding jobs
    - Usage tracking
    """

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
        """
        Generate single text embedding.

        Implementation will be added when
        AI provider integration is enabled.
        """

        raise NotImplementedError("OpenAI embedding integration pending.")

    def embed_batch(
        self,
        *,
        texts: list[str],
        **kwargs: Any,
    ) -> EmbeddingBatch:
        """
        Generate multiple embeddings.

        Supports future:

        - bulk indexing
        - document ingestion
        - clinical knowledge ingestion
        """

        raise NotImplementedError("OpenAI batch embedding integration pending.")


__all__: tuple[str, ...] = ("OpenAIEmbeddingProvider",)
