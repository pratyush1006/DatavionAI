"""
DatavionOS Vector Search Service.

High-level semantic search service.

Connects:

EmbeddingService
        |
        v
VectorEngine
        |
        v
Vector Backends


Supports:

- RAG pipelines
- Clinical Copilot
- Patient timeline AI
- Semantic document retrieval
- Multi-provider embeddings
"""

from __future__ import annotations

from typing import Any

from apps.common.search.embeddings import (
    embedding_service,
)

from .engine import (
    vector_engine,
)
from .types import (
    VectorSearchRequest,
    VectorSearchResult,
)

DEFAULT_EMBEDDING_PROVIDER = "openai"


class VectorSearchService:
    """
    Application-level semantic search service.

    Responsible for orchestrating:

    1. Text -> Embedding
    2. Embedding -> Vector Search
    3. Vector Backend -> Results
    """

    def semantic_search(
        self,
        *,
        text: str,
        provider: str = "pgvector",
        embedding_provider: str = DEFAULT_EMBEDDING_PROVIDER,
        tenant_id: str | None = None,
        organization_id: str | None = None,
        patient_id: str | None = None,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> VectorSearchResult:
        """
        Execute semantic vector search.

        Flow:

        text
          |
          v
        Embedding Provider
          |
          v
        VectorSearchRequest
          |
          v
        VectorEngine
          |
          v
        Vector Backend
        """

        vector = embedding_service.embed(
            text=text,
            provider=embedding_provider,
        )

        request = VectorSearchRequest(
            vector=vector,
            top_k=top_k,
            tenant_id=tenant_id,
            organization_id=organization_id,
            patient_id=patient_id,
            filters=filters,
        )

        return vector_engine.search(
            request,
            provider=provider,
        )


vector_search_service = VectorSearchService()


__all__: tuple[str, ...] = (
    "VectorSearchService",
    "vector_search_service",
)
