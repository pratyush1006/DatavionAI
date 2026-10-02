"""
DatavionOS Embedding Provider Base.

Defines the contract for all embedding providers.

Supported providers:

- OpenAI
- Azure OpenAI
- HuggingFace
- Gemini
- Custom models
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .types import EmbeddingBatch, EmbeddingMetadata, EmbeddingVector


class BaseEmbeddingProvider(
    ABC,
):
    """
    Abstract embedding provider.

    All AI embedding providers must implement
    this interface.
    """

    name: str = ""

    model: str = ""

    dimensions: int | None = None

    supports_batch: bool = True

    @abstractmethod
    def embed(
        self,
        *,
        text: str,
        **kwargs: Any,
    ) -> EmbeddingVector:
        """
        Generate embedding vector.
        """

        raise NotImplementedError

    @abstractmethod
    def embed_batch(
        self,
        *,
        texts: list[str],
        **kwargs: Any,
    ) -> EmbeddingBatch:
        """
        Generate multiple embeddings.
        """

        raise NotImplementedError

    def metadata(
        self,
    ) -> EmbeddingMetadata:
        """
        Return provider metadata.
        """

        return {
            "provider": self.name,
            "model": self.model,
            "dimensions": self.dimensions,
        }


__all__: tuple[str, ...] = ("BaseEmbeddingProvider",)
