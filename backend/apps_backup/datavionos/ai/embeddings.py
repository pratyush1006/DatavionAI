"""
Embedding model contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


@dataclass(
    frozen=True,
    slots=True,
)
class EmbeddingRequest:
    """
    Immutable embedding request.
    """

    input: tuple[str, ...]

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class Embedding:
    """
    Immutable embedding vector.
    """

    input: str

    vector: tuple[float, ...]

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class EmbeddingResponse:
    """
    Immutable embedding response.
    """

    embeddings: tuple[Embedding, ...]

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@runtime_checkable
class EmbeddingModel(
    Protocol,
):
    """
    Semantic embedding model.
    """

    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate embeddings for the supplied input.
        """


__all__ = [
    "Embedding",
    "EmbeddingModel",
    "EmbeddingRequest",
    "EmbeddingResponse",
]
