"""
Patient document version model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from ..validators import (
    validate_document,
)
from .patient_document import PatientDocument


class DocumentVersion(BaseModel):
    """
    Stores immutable versions of a patient document.
    """

    document = models.ForeignKey(
        PatientDocument,
        on_delete=models.CASCADE,
        related_name="versions",
    )

    version = models.PositiveIntegerField()

    file = models.FileField(
        upload_to="patient_documents/%Y/%m/",
        validators=[
            validate_document,
        ],
    )

    original_filename = models.CharField(
        max_length=255,
    )

    mime_type = models.CharField(
        max_length=100,
    )

    file_size = models.BigIntegerField()

    checksum = models.CharField(
        max_length=128,
        blank=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_patient_document_versions",
    )

    remarks = models.TextField(
        blank=True,
    )

    is_current = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = "Document Version"

        verbose_name_plural = "Document Versions"

        ordering = ("-version",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "document",
                    "version",
                ],
                name="uq_patient_document_version",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "document",
                    "version",
                ],
            ),
            models.Index(
                fields=[
                    "is_current",
                ],
            ),
            models.Index(
                fields=[
                    "uploaded_by",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.document.document_number} (v{self.version})"


__all__ = [
    "DocumentVersion",
]
