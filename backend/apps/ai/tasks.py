"""
Celery tasks for AI knowledge ingestion and retrieval.
"""

from __future__ import annotations

import asyncio

from celery import shared_task

from apps.ai.models import DocumentChunk, KnowledgeDocument
from apps.datavionos.ai.implementation.embeddings import OpenAIEmbeddingModel
from apps.datavionos.ai.implementation.vector_store import PostgresVectorStore

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def _split_text(
    text: str,
    size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks."""

    if len(text) <= size:
        return [text]

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += size - overlap

    return chunks


@shared_task(
    queue="ai",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    max_retries=3,
)
def ingest_knowledge_document(
    self,
    document_id: str,
) -> int:
    """
    Chunk a knowledge document, embed it and store vectors.
    """

    document = KnowledgeDocument.objects.get(pk=document_id)

    pieces = _split_text(document.content)
    embeddings = OpenAIEmbeddingModel()

    loop = asyncio.new_event_loop()
    try:
        response = loop.run_until_complete(
            embeddings.embed(
                type(
                    "Req",
                    (),
                    {"input": tuple(pieces), "metadata": {}},
                )(),
            )
        )
    finally:
        loop.close()

    DocumentChunk.objects.filter(document=document).delete()

    for index, piece in enumerate(pieces):
        vector = list(response.embeddings[index].vector)
        DocumentChunk.objects.create(
            document=document,
            organization_id=document.organization_id,
            chunk_index=index,
            content=piece,
            embedding=vector,
            token_count=len(piece.split()),
        )

    return len(pieces)


@shared_task(queue="ai")
def clear_knowledge_index(
    organization_id: str | None = None,
) -> str:
    """Clear the vector index for an organization."""

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(
            PostgresVectorStore(organization_id=organization_id).clear()
        )
    finally:
        loop.close()

    return "cleared"


__all__ = [
    "clear_knowledge_index",
    "ingest_knowledge_document",
]
