"""
PostgreSQL pgvector backend.

Future integration:

- PostgreSQL
- pgvector extension
- Django ORM vector fields
"""

from __future__ import annotations

from typing import Any

from ..base import BaseVectorBackend
from ..types import (
    VectorDocument,
    VectorSearchRequest,
    VectorSearchResult,
)


class PGVectorBackend(
    BaseVectorBackend,
):
    """
    PostgreSQL vector search backend.
    """

    name = "pgvector"

    def index(
        self,
        document: VectorDocument,
        **kwargs: Any,
    ) -> None:
        """
        Store vector document.
        """

        return

    def search(
        self,
        request: VectorSearchRequest,
        **kwargs: Any,
    ) -> VectorSearchResult:
        """
        Execute similarity search.
        """

        return VectorSearchResult(
            items=[],
            total=0,
            provider=self.name,
            metadata={
                "search_type": "vector",
            },
        )

    def delete(
        self,
        document_id: str,
        **kwargs: Any,
    ) -> None:
        """
        Delete vector document.
        """

        return

    def supports_filtering(
        self,
    ) -> bool:
        return True


__all__ = ("PGVectorBackend",)
