"""Deterministic RAG pipeline with pluggable embeddings/retrieval."""

from __future__ import annotations

import hashlib
import math

from apps.ai.models import KnowledgeChunk, KnowledgeDocument
from apps.ai.providers.registry import get_embedding_provider
from apps.ai.services.scope import (
    validate_document_scope,
    validate_knowledge_base_scope,
)


def chunk_text(text: str, *, chunk_size: int = 1200, overlap: int = 150) -> list[str]:
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "chunk_size must be positive and overlap must be smaller than chunk_size"
        )
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size // 5)
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(start + 1, end - overlap // 5)
    return [chunk for chunk in chunks if chunk]


def index_document(
    *,
    document: KnowledgeDocument,
    tenant,
    organization,
    embedding_provider=None,
    embedding_model=None,
    chunk_size=1200,
    overlap=150,
) -> int:
    from apps.ai.production import production_config

    deployment = production_config()
    embedding_provider = embedding_provider or deployment.embedding_provider
    embedding_model = embedding_model or deployment.embedding_model
    validate_document_scope(document, tenant=tenant, organization=organization)
    text = document.content.strip()
    document.chunks.all().delete()
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    provider = get_embedding_provider(embedding_provider)
    vectors = provider.embed(chunks, embedding_model)

    for sequence, (content, vector) in enumerate(zip(chunks, vectors)):
        KnowledgeChunk.objects.create(
            document=document,
            sequence=sequence,
            content=content,
            embedding=vector,
            embedding_model=embedding_model,
        )

    document.status = "indexed"
    document.error = ""
    document.save(update_fields=("status", "error", "updated_at"))
    return len(chunks)


def _cosine(a, b):
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def retrieve(
    *,
    knowledge_base,
    tenant,
    organization,
    query: str,
    top_k=5,
    embedding_provider=None,
    embedding_model=None,
):
    from apps.ai.production import production_config

    deployment = production_config()
    embedding_provider = embedding_provider or deployment.embedding_provider
    embedding_model = embedding_model or deployment.embedding_model
    validate_knowledge_base_scope(
        knowledge_base,
        tenant=tenant,
        organization=organization,
    )

    if not query or not query.strip():
        raise ValueError("RAG query is required.")
    if top_k <= 0:
        raise ValueError("top_k must be positive.")

    provider = get_embedding_provider(embedding_provider)
    query_vector = provider.embed([query], embedding_model)[0]

    chunks = list(
        KnowledgeChunk.objects.filter(
            document__knowledge_base=knowledge_base,
            document__organization=organization,
            document__knowledge_base__tenant=tenant,
            document__knowledge_base__organization=organization,
            document__is_active=True,
            document__is_deleted=False,
        ).select_related("document")
    )

    ranked = sorted(
        ((_cosine(query_vector, chunk.embedding), chunk) for chunk in chunks),
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        {
            "score": round(score, 6),
            "chunk_id": str(chunk.uuid),
            "document_id": str(chunk.document.uuid),
            "content": chunk.content,
            "title": chunk.document.title,
        }
        for score, chunk in ranked[:top_k]
    ]


def add_text_document(
    *,
    knowledge_base,
    tenant,
    organization,
    title: str,
    content: str,
    source_uri="",
) -> KnowledgeDocument:
    validate_knowledge_base_scope(
        knowledge_base,
        tenant=tenant,
        organization=organization,
    )

    if not title.strip():
        raise ValueError("Knowledge document title is required.")
    if not content.strip():
        raise ValueError("Knowledge document content is required.")

    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()

    document, _ = KnowledgeDocument.objects.update_or_create(
        knowledge_base=knowledge_base,
        content_hash=digest,
        defaults={
            "organization": organization,
            "title": title,
            "content": content,
            "source_type": "text",
            "source_uri": source_uri,
            "status": "pending",
            "is_active": True,
            "is_deleted": False,
            "is_published": False,
        },
    )

    validate_document_scope(
        document,
        tenant=tenant,
        organization=organization,
    )
    return document


__all__ = ("chunk_text", "index_document", "retrieve", "add_text_document")
