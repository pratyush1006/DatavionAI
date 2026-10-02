"""
DatavionOS Vector Engine.

Unified entry point for vector search operations.
"""

from __future__ import annotations

from typing import Any

from .registry import (
    get_vector_provider,
)
from .types import (
    VectorDocument,
    VectorSearchRequest,
    VectorSearchResult,
)


class VectorEngine:
    """
    Vector search orchestrator.

    Routes requests to configured vector backend.
    """

    def index(
        self,
        *,
        document: VectorDocument,
        provider: str = "pgvector",
        **kwargs: Any,
    ) -> None:
        """
        Index vector document.
        """

        backend_class = get_vector_provider(
            provider,
        )

        backend = backend_class()

        return backend.index(
            document,
            **kwargs,
        )

    def search(
        self,
        request: VectorSearchRequest,
        *,
        provider: str = "pgvector",
        **kwargs: Any,
    ) -> VectorSearchResult:
        """
        Execute vector similarity search.
        """

        backend_class = get_vector_provider(
            provider,
        )

        backend = backend_class()

        return backend.search(
            request,
            **kwargs,
        )

    def delete(
        self,
        *,
        document_id: str,
        provider: str = "pgvector",
        **kwargs: Any,
    ) -> None:
        """
        Delete vector document.
        """

        backend_class = get_vector_provider(
            provider,
        )

        backend = backend_class()

        return backend.delete(
            document_id,
            **kwargs,
        )


vector_engine = VectorEngine()


__all__: tuple[str, ...] = (
    "VectorEngine",
    "vector_engine",
)
