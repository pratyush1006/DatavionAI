"""
HuggingFace embedding provider.
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


class HuggingFaceEmbeddingProvider(
    BaseEmbeddingProvider,
):
    """
    Local HuggingFace embedding provider.

    Future support:

    - BGE models
    - E5 models
    - Sentence Transformers
    """

    name = "huggingface"

    model = ""

    dimensions = None

    def embed(
        self,
        *,
        text: str,
        **kwargs: Any,
    ) -> EmbeddingVector:
        """
        Generate embedding.
        """

        raise NotImplementedError("HuggingFace integration pending.")

    def embed_batch(
        self,
        *,
        texts: list[str],
        **kwargs: Any,
    ) -> EmbeddingBatch:
        """
        Generate batch embeddings.
        """

        raise NotImplementedError("HuggingFace integration pending.")


__all__: tuple[str, ...] = ("HuggingFaceEmbeddingProvider",)
