"""Async-safe AI task entry points; compatible with the project's task runner."""

from __future__ import annotations


def index_knowledge_document(document_id: str) -> int:
    from apps.ai.models import KnowledgeDocument
    from apps.ai.services.rag import index_document

    document = KnowledgeDocument.objects.get(uuid=document_id)
    return index_document(document=document)
