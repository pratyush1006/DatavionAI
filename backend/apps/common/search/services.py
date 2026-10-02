"""
Search services for DatavionOS.

Provides the application service layer for search operations.

Business applications should use this service instead of
directly accessing search engine, indexer, or registry.
"""

from __future__ import annotations

from apps.common.search.engine import (
    search_engine,
)
from apps.common.search.indexer import (
    search_indexer,
)
from apps.common.search.models import (
    SearchDocument,
    SearchRequest,
    SearchResponse,
)
from apps.common.search.registry import (
    SearchIndexer,
    SearchProvider,
    search_registry,
)


class SearchService:
    """
    Search application service.

    Provides:

    - Search execution
    - Document indexing
    - Provider registration
    - Indexer registration
    """

    def search(
        self,
        request: SearchRequest,
        *,
        backend: str,
    ) -> SearchResponse:
        """
        Execute search.
        """

        return search_engine.search(
            request,
            backend=backend,
        )

    def index(
        self,
        document: SearchDocument,
        *,
        backend: str,
    ) -> None:
        """
        Index document.
        """

        search_indexer.index(
            document,
            backend=backend,
        )

    def delete(
        self,
        document_id: str | int,
        *,
        backend: str,
    ) -> None:
        """
        Delete indexed document.
        """

        search_indexer.delete(
            document_id,
            backend=backend,
        )

    def register_provider(
        self,
        provider: SearchProvider,
    ) -> None:
        """
        Register search provider.
        """

        search_registry.register_provider(
            provider,
        )

    def register_indexer(
        self,
        indexer: SearchIndexer,
    ) -> None:
        """
        Register search indexer.
        """

        search_registry.register_indexer(
            indexer,
        )


search_service = SearchService()


__all__: tuple[str, ...] = (
    "SearchService",
    "search_service",
)
