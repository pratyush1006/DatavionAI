"""
Document version model.

Maintains immutable document version history.

Responsibilities
----------------
- Version tracking
- File snapshot metadata
- Storage reference
- Version lifecycle
- Integrity validation

Non-responsibilities
--------------------
- File upload
- Storage operations
- OCR processing
- AI extraction execution

Those belong to:
- common.documents
- storage services
- AI services
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import (
    BaseModel,
)
from apps.documents.constants import (
    DocumentVersionStatus,
)


class DocumentVersion(
    BaseModel,
):
    """
    Represents a document version snapshot.

    Example:

        Document
            |
            +-- Version 1
            |
            +-- Version 2
            |
            +-- Version 3 (current)
    """

    # ============================================================
    # Relationship
    # ============================================================

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name=_(
            "Document",
        ),
        help_text=_(
            "Parent document.",
        ),
    )

    # ============================================================
    # Version Information
    # ============================================================

    version_number = models.PositiveIntegerField(
        _("Version Number"),
        default=1,
        help_text=_(
            "Sequential document version number.",
        ),
    )

    status = models.CharField(
        _("Version Status"),
        max_length=30,
        choices=DocumentVersionStatus.choices,
        default=(DocumentVersionStatus.CURRENT),
        db_index=True,
    )

    # ============================================================
    # Storage Snapshot
    # ============================================================

    storage_key = models.CharField(
        _("Storage Key"),
        max_length=500,
        help_text=_(
            "Storage reference for this version.",
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
    )

    checksum = models.CharField(
        _("Checksum"),
        max_length=255,
        blank=True,
    )

    # ============================================================
    # Upload Information
    # ============================================================

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_document_versions",
        verbose_name=_(
            "Uploaded By",
        ),
    )

    # ============================================================
    # AI Metadata
    # ============================================================

    extraction_metadata = models.JSONField(
        _("Extraction Metadata"),
        default=dict,
        blank=True,
        help_text=_(
            "AI/OCR extraction output.",
        ),
    )

    # ============================================================
    # Metadata
    # ============================================================

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        blank=True,
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "document_versions"

        verbose_name = _(
            "Document Version",
        )

        verbose_name_plural = _(
            "Document Versions",
        )

        ordering = (
            "document",
            "-version_number",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "document",
                    "version_number",
                ),
                name=("uq_document_version_number"),
            ),
            models.CheckConstraint(
                condition=Q(
                    version_number__gte=1,
                ),
                name=("ck_document_version_positive"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("document",),
                name=("idx_document_version_document"),
            ),
            models.Index(
                fields=("status",),
                name=("idx_document_version_status"),
            ),
            models.Index(
                fields=("checksum",),
                name=("idx_document_version_checksum"),
            ),
        ]

    @property
    def is_current(
        self,
    ) -> bool:
        """
        Return whether this is current version.
        """

        return self.status == DocumentVersionStatus.CURRENT

    def __str__(
        self,
    ) -> str:
        """
        Human readable representation.
        """

        return f"{self.document.title} v{self.version_number}"


__all__ = ("DocumentVersion",)
