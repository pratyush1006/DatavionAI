"""
Knowledge base documents used for retrieval-augmented generation.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class KnowledgeDocument(BaseModel):
    """
    A document ingested into the RAG knowledge base.

    The raw text and metadata are stored here; vector embeddings are
    stored separately in :class:`DocumentChunk`.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="knowledge_documents",
        null=True,
        blank=True,
        help_text="Owning organization. Null for global knowledge.",
    )

    title = models.CharField(
        max_length=255,
        help_text="Document title.",
    )

    source_type = models.CharField(
        max_length=50,
        default="guideline",
        help_text="Kind of source, e.g. guideline, policy, ehr_context.",
    )

    content = models.TextField(
        help_text="Full document text.",
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Arbitrary document metadata.",
    )

    is_published = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether the document is available for retrieval.",
    )

    class Meta:
        db_table = "ai_knowledge_documents"

        verbose_name = "Knowledge Document"

        verbose_name_plural = "Knowledge Documents"

        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Return the document title."""

        return self.title


class DocumentChunk(BaseModel):
    """
    A retrievable chunk of a :class:`KnowledgeDocument` with its embedding.
    """

    objects = BaseManager()

    document = models.ForeignKey(
        KnowledgeDocument,
        on_delete=models.CASCADE,
        related_name="chunks",
        help_text="Parent document.",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="document_chunks",
        null=True,
        blank=True,
    )

    chunk_index = models.PositiveIntegerField(
        default=0,
        help_text="Zero-based position of the chunk in the document.",
    )

    content = models.TextField(
        help_text="Chunk text.",
    )

    embedding = models.JSONField(
        null=True,
        blank=True,
        help_text="Dense vector stored as a JSON list of floats.",
    )

    token_count = models.PositiveIntegerField(
        default=0,
        help_text="Approximate token count of the chunk.",
    )

    class Meta:
        db_table = "ai_document_chunks"

        verbose_name = "Document Chunk"

        verbose_name_plural = "Document Chunks"

        ordering = (
            "document",
            "chunk_index",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "document",
                ],
                name="ai_chunk_org_doc_idx",
            ),
        ]

    def __str__(self) -> str:
        """Return a readable label."""

        return f"{self.document.title} [{self.chunk_index}]"


__all__ = [
    "DocumentChunk",
    "KnowledgeDocument",
]
