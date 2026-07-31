"""
Postgres-backed vector store.

Stores embeddings as JSON lists on :class:`DocumentChunk` and performs
cosine similarity in Python. This avoids a hard dependency on ``pgvector``
while remaining correct for moderate document volumes.
"""

from __future__ import annotations

import math
from typing import Any

from apps.ai.models import DocumentChunk
from apps.datavionos.ai.vector_store import (
    VectorDocument,
    VectorSearchRequest,
    VectorSearchResponse,
    VectorSearchResult,
)


def _cosine_similarity(
    a: tuple[float, ...],
    b: tuple[float, ...],
) -> float:
    if len(a) != len(b) or not a:
        return 0.0

    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot / (norm_a * norm_b)


class PostgresVectorStore:
    """
    Vector store backed by the Django ORM and ``DocumentChunk`` rows.
    """

    def __init__(
        self,
        *,
        organization_id: Any | None = None,
    ) -> None:
        self._organization_id = organization_id

    async def upsert(
        self,
        documents: tuple[VectorDocument, ...],
    ) -> None:
        """Insert or update vector documents."""

        for document in documents:
            DocumentChunk.objects.update_or_create(
                pk=document.id,
                defaults={
                    "content": document.content,
                    "embedding": list(document.vector),
                    "metadata": document.metadata,
                    "organization_id": self._organization_id,
                },
            )

    async def delete(
        self,
        identifiers: tuple[str, ...],
    ) -> None:
        """Delete vector documents."""

        DocumentChunk.objects.filter(pk__in=identifiers).delete()

    async def search(
        self,
        request: VectorSearchRequest,
    ) -> VectorSearchResponse:
        """Perform a cosine similarity search."""

        queryset = DocumentChunk.objects.all()

        if self._organization_id is not None:
            queryset = queryset.filter(
                organization_id=self._organization_id,
            )

        results: list[VectorSearchResult] = []

        for chunk in queryset.exclude(embedding__isnull=True):
            embedding = tuple(float(x) for x in chunk.embedding)
            score = _cosine_similarity(request.vector, embedding)

            results.append(
                VectorSearchResult(
                    document=VectorDocument(
                        id=str(chunk.pk),
                        vector=embedding,
                        content=chunk.content,
                        metadata=chunk.metadata or {},
                    ),
                    score=score,
                )
            )

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return VectorSearchResponse(
            results=tuple(results[: request.limit]),
            metadata={"count": len(results)},
        )

    async def clear(
        self,
        namespace: str | None = None,
    ) -> None:
        """Remove documents from the store."""

        queryset = DocumentChunk.objects.all()

        if self._organization_id is not None:
            queryset = queryset.filter(organization_id=self._organization_id)

        queryset.delete()

    async def exists(
        self,
        identifier: str,
    ) -> bool:
        """Determine whether a vector document exists."""

        return DocumentChunk.objects.filter(pk=identifier).exists()


__all__ = [
    "PostgresVectorStore",
]
