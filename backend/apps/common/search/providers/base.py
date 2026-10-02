"""
DatavionOS Search Provider Contract.

Defines the interface implemented by all
search backends.

Supported providers:

- PostgreSQL full-text search
- Vector semantic search
- Hybrid AI search
- Future Elasticsearch/OpenSearch
- Healthcare FHIR resource search
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.common.search.types import (
    SearchRequest,
    SearchResult,
)


class BaseSearchProvider(
    ABC,
):
    """
    Abstract search provider.

    Every search backend must implement
    this contract.

    Providers must support:

    - tenant isolation
    - organization filtering
    - patient filtering
    - pagination
    - relevance scoring
    - metadata enrichment
    """

    name: str = ""

    @abstractmethod
    def search(
        self,
        request: SearchRequest,
        **kwargs: Any,
    ) -> SearchResult:
        """
        Execute search.

        Parameters
        ----------
        request:
            Standardized search request.

        kwargs:
            Provider-specific options.

        Examples:

        - vector index
        - ranking model
        - database hints
        - FHIR resource type
        """

        raise NotImplementedError

    def health_check(
        self,
    ) -> bool:
        """
        Provider health validation.

        External providers can override.
        """

        return True

    def supports_semantic_search(
        self,
    ) -> bool:
        """
        Whether provider supports AI semantic search.
        """

        return False

    def supports_pagination(
        self,
    ) -> bool:
        """
        Whether provider supports pagination.
        """

        return True


__all__: tuple[str, ...] = ("BaseSearchProvider",)
