"""
DatavionOS PostgreSQL Search Provider.

Keyword/full-text search provider.

Future integrations:

- PostgreSQL tsvector
- pg_trgm similarity
- FHIR resource search
- Clinical timeline search
"""

from __future__ import annotations

from apps.common.search.types import (
    SearchRequest,
    SearchResult,
)

from .base import BaseSearchProvider


class PostgreSQLSearchProvider(
    BaseSearchProvider,
):
    """
    PostgreSQL based search provider.
    """

    name = "postgres"

    def search(
        self,
        request: SearchRequest,
        **kwargs,
    ) -> SearchResult:
        """
        Execute PostgreSQL search.

        Future:

        - Full text indexing
        - Tenant filtering
        - Organization filtering
        - Patient filtering
        """

        return SearchResult(
            items=[],
            total=0,
            page=request.page,
            page_size=request.page_size,
            total_pages=0,
            metadata={
                "provider": self.name,
                "query": request.query,
                "search_type": "keyword",
            },
        )


__all__: tuple[str, ...] = ("PostgreSQLSearchProvider",)
