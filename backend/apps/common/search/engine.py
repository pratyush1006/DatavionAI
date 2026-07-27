"""
DatavionOS Search Engine.

Unified search orchestration layer.

Responsibilities:

- Provider resolution
- Search request routing
- Capability discovery
- Future hybrid search orchestration
"""

from __future__ import annotations

from typing import Any

from .registry import (
    get_search_provider,
)
from .types import (
    SearchRequest,
    SearchResult,
)


class SearchEngine:
    """
    Platform search orchestrator.

    Supports:

    - PostgreSQL search
    - Vector semantic search
    - Hybrid AI search
    - Healthcare timeline search
    """

    def get_provider(
        self,
        name: str,
    ):
        """
        Resolve search provider instance.
        """

        provider_class = get_search_provider(
            name,
        )

        return provider_class()

    def search(
        self,
        request: SearchRequest,
        *,
        provider: str = "postgres",
        **kwargs: Any,
    ) -> SearchResult:
        """
        Execute search using selected provider.

        Example:

        search_engine.search(
            SearchRequest(
                query="diabetes",
                tenant_id="tenant-1",
                patient_id="patient-1",
            )
        )
        """

        search_provider = self.get_provider(
            provider,
        )

        return search_provider.search(
            request,
            **kwargs,
        )

    def provider_health(
        self,
        provider: str,
    ) -> bool:
        """
        Check provider availability.
        """

        search_provider = self.get_provider(
            provider,
        )

        return search_provider.health_check()

    def supports_semantic_search(
        self,
        provider: str,
    ) -> bool:
        """
        Check AI semantic search support.
        """

        search_provider = self.get_provider(
            provider,
        )

        return search_provider.supports_semantic_search()


search_engine = SearchEngine()


__all__: tuple[str, ...] = (
    "SearchEngine",
    "search_engine",
)
