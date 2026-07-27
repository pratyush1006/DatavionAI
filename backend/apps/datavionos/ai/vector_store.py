"""
Vector store contracts.
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
class VectorDocument:
    """
    Immutable vector document.
    """

    id: str

    vector: tuple[float, ...]

    content: str

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class VectorSearchRequest:
    """
    Immutable vector search request.
    """

    vector: tuple[float, ...]

    limit: int = 10

    namespace: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class VectorSearchResult:
    """
    Immutable vector search result.
    """

    document: VectorDocument

    score: float


@dataclass(
    frozen=True,
    slots=True,
)
class VectorSearchResponse:
    """
    Immutable vector search response.
    """

    results: tuple[VectorSearchResult, ...]

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@runtime_checkable
class VectorStore(
    Protocol,
):
    """
    Vector database abstraction.
    """

    async def upsert(
        self,
        documents: tuple[VectorDocument, ...],
    ) -> None:
        """
        Insert or update vector documents.
        """

    async def delete(
        self,
        identifiers: tuple[str, ...],
    ) -> None:
        """
        Delete vector documents.
        """

    async def search(
        self,
        request: VectorSearchRequest,
    ) -> VectorSearchResponse:
        """
        Perform a similarity search.
        """

    async def clear(
        self,
        namespace: str | None = None,
    ) -> None:
        """
        Remove documents from a namespace.
        """

    async def exists(
        self,
        identifier: str,
    ) -> bool:
        """
        Determine whether a vector document exists.
        """


__all__ = [
    "VectorDocument",
    "VectorSearchRequest",
    "VectorSearchResponse",
    "VectorSearchResult",
    "VectorStore",
]
