"""
Document aggregate root.

Central document entity for DatavionOS.

Responsibilities
----------------
- Document identity
- Tenant ownership
- Organization ownership
- Document lifecycle
- Storage metadata
- AI metadata
- Version management

Non-responsibilities
--------------------
- Physical storage operations
- File upload handling
- OCR execution
- Virus scanning
- Domain-specific ownership

Those belong to:
- common.documents
- AI services
- consuming bounded contexts
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.documents.constants import (
    DEFAULT_ACCESS_LEVEL,
    DEFAULT_DOCUMENT_STATUS,
    DEFAULT_DOCUMENT_TYPE,
    DocumentAccessLevel,
    DocumentStatus,
    DocumentType,
)


class Document(
    BaseModel,
):
    """
    Central document aggregate.

    Referenced by:

    - Employee documents
    - Patient documents
    - Clinical documents
    - Laboratory documents
    - Billing documents
    """

    # ============================================================
    # Ownership
    # ============================================================

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_(
            "Tenant",
        ),
        help_text=_(
            "Tenant owning this document.",
        ),
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_(
            "Organization",
        ),
        help_text=_(
            "Organization owning this document.",
        ),
    )

    # ============================================================
    # Identity
    # ============================================================

    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_(
            "Human readable document title.",
        ),
    )

    document_type = models.CharField(
        _("Document Type"),
        max_length=50,
        choices=DocumentType.choices,
        default=DEFAULT_DOCUMENT_TYPE,
        db_index=True,
    )

    status = models.CharField(
        _("Status"),
        max_length=30,
        choices=DocumentStatus.choices,
        default=DEFAULT_DOCUMENT_STATUS,
        db_index=True,
    )

    access_level = models.CharField(
        _("Access Level"),
        max_length=30,
        choices=DocumentAccessLevel.choices,
        default=DEFAULT_ACCESS_LEVEL,
        db_index=True,
    )

    # ============================================================
    # Storage metadata
    # ============================================================

    storage_key = models.CharField(
        _("Storage Key"),
        max_length=500,
        help_text=_(
            "External storage reference.",
        ),
    )

    original_filename = models.CharField(
        _("Original Filename"),
        max_length=255,
        blank=True,
    )

    mime_type = models.CharField(
        _("Mime Type"),
        max_length=150,
        blank=True,
    )

    file_size = models.BigIntegerField(
        _("File Size"),
        default=0,
        help_text=_(
            "File size in bytes.",
        ),
    )

    checksum = models.CharField(
        _("Checksum"),
        max_length=255,
        blank=True,
        help_text=_(
            "Integrity checksum.",
        ),
    )

    # ============================================================
    # Metadata / AI
    # ============================================================

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        blank=True,
    )

    ai_metadata = models.JSONField(
        _("AI Metadata"),
        default=dict,
        blank=True,
        help_text=_(
            "AI extraction and enrichment metadata.",
        ),
    )

    # ============================================================
    # Lifecycle
    # ============================================================

    archived_at = models.DateTimeField(
        _("Archived At"),
        null=True,
        blank=True,
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "documents"

        verbose_name = _(
            "Document",
        )

        verbose_name_plural = _(
            "Documents",
        )

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "tenant",
                    "storage_key",
                ),
                name=("uq_document_tenant_storage_key"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("tenant",),
                name=("idx_document_tenant"),
            ),
            models.Index(
                fields=("organization",),
                name=("idx_document_org"),
            ),
            models.Index(
                fields=("status",),
                name=("idx_document_status"),
            ),
            models.Index(
                fields=("document_type",),
                name=("idx_document_type"),
            ),
            models.Index(
                fields=("access_level",),
                name=("idx_document_access"),
            ),
        ]

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Whether document is active.
        """

        return self.status == DocumentStatus.ACTIVE

    @property
    def is_archived(
        self,
    ) -> bool:
        """
        Whether document is archived.
        """

        return self.status == DocumentStatus.ARCHIVED

    def __str__(
        self,
    ) -> str:
        """
        Human readable representation.
        """

        return self.title


__all__ = ("Document",)
