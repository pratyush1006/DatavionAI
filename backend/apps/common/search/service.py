"""
DatavionOS Unified Search Service.

Enterprise search orchestration facade.

Combines:

- Keyword search
- Semantic vector search
- Hybrid fusion
- Result normalization
"""

from __future__ import annotations

from typing import Any

from .engine import (
    search_engine,
)
from .hybrid import (
    hybrid_search_engine,
)
from .results import (
    search_result_normalizer,
)
from .vector import (
    vector_search_service,
)


class SearchService:
    """
    Public search service facade.
    """

    def search(
        self,
        *,
        query: str,
        mode: str = "hybrid",
        provider: str = "pgvector",
        embedding_provider: str = "local",
        tenant_id: str | None = None,
        organization_id: str | None = None,
        patient_id: str | None = None,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ):
        """
        Execute enterprise search.
        """

        if mode == "keyword":
            result = search_engine.search(
                query=query,
            )

            return search_result_normalizer.normalize(
                items=[],
                provider="postgres",
                mode="keyword",
                metadata={
                    "tenant_id": tenant_id,
                    "organization_id": organization_id,
                },
            )

        if mode == "semantic":
            result = vector_search_service.semantic_search(
                text=query,
                provider=provider,
                embedding_provider=embedding_provider,
                tenant_id=tenant_id,
                organization_id=organization_id,
                patient_id=patient_id,
                top_k=top_k,
                filters=filters,
            )

            return search_result_normalizer.normalize(
                items=result.items,
                provider=provider,
                mode="semantic",
                metadata={
                    "tenant_id": tenant_id,
                    "organization_id": organization_id,
                    "patient_id": patient_id,
                },
            )

        vector_result = vector_search_service.semantic_search(
            text=query,
            provider=provider,
            embedding_provider=embedding_provider,
            tenant_id=tenant_id,
            organization_id=organization_id,
            patient_id=patient_id,
            top_k=top_k,
            filters=filters,
        )

        hybrid_result = hybrid_search_engine.search(
            keyword_results=[],
            vector_results=vector_result.items,
            strategy="weighted",
        )

        return search_result_normalizer.normalize(
            items=hybrid_result.items,
            provider=provider,
            mode="hybrid",
            metadata={
                "tenant_id": tenant_id,
                "organization_id": organization_id,
                "patient_id": patient_id,
                "strategy": hybrid_result.strategy,
            },
        )


search_service = SearchService()


__all__: tuple[str, ...] = (
    "SearchService",
    "search_service",
)
