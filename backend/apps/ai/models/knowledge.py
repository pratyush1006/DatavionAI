"""Tenant-scoped knowledge and RAG persistence."""

from __future__ import annotations

import uuid

from django.db import models


class KnowledgeBase(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_knowledge_bases"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_knowledge_bases",
    )
    application = models.ForeignKey(
        "ai.AIApplication", on_delete=models.CASCADE, related_name="knowledge_bases"
    )
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    embedding_model = models.CharField(max_length=160, blank=True)
    vector_store = models.CharField(max_length=80, default="database")
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_knowledge_bases"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "name"), name="ai_kb_org_name_uniq"
            )
        ]


class KnowledgeDocument(models.Model):
    # Compatibility bridge for the historical AI schema. These fields map to
    # columns that must remain physically present because legacy AI data and
    # foreign keys still depend on them. They are intentionally retained in
    # the runtime model while the new UUID remains the Django primary key.
    legacy_id = models.UUIDField(
        db_column="id",
        default=uuid.uuid4,
        editable=False,
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    deleted_by_id = models.UUIDField(null=True, blank=True, editable=False)
    is_published = models.BooleanField(default=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_knowledge_documents",
        null=True,
        blank=True,
    )
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
    )
    source_type = models.CharField(max_length=30)
    source_uri = models.TextField(blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    content_hash = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=30, default="pending")
    metadata = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_knowledge_documents"
        constraints = [
            models.UniqueConstraint(
                fields=("knowledge_base", "content_hash"), name="ai_kdoc_kb_hash_uniq"
            )
        ]


class KnowledgeChunk(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    document = models.ForeignKey(
        KnowledgeDocument, on_delete=models.CASCADE, related_name="chunks"
    )
    sequence = models.PositiveIntegerField()
    content = models.TextField()
    embedding = models.JSONField(default=list, blank=True)
    embedding_model = models.CharField(max_length=160, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_knowledge_chunks"
        constraints = [
            models.UniqueConstraint(
                fields=("document", "sequence"), name="ai_chunk_doc_seq_uniq"
            )
        ]
        indexes = [
            models.Index(fields=("document", "sequence"), name="ai_chunk_doc_seq_idx")
        ]
