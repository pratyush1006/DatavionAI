"""
Patient document model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization

from ..constants import (
    DEFAULT_DOCUMENT_SOURCE,
    DEFAULT_DOCUMENT_STATUS,
    DEFAULT_DOCUMENT_VISIBILITY,
    DEFAULT_STORAGE_BACKEND,
    DocumentCategory,
    DocumentSource,
    DocumentStatus,
    DocumentVisibility,
    StorageBackend,
)
from ..managers import PatientDocumentManager


class PatientDocument(BaseModel):
    """
    Stores patient document metadata.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_documents",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_number = models.CharField(
        max_length=50,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    category = models.CharField(
        max_length=30,
        choices=DocumentCategory.choices,
    )

    source = models.CharField(
        max_length=30,
        choices=DocumentSource.choices,
        default=DEFAULT_DOCUMENT_SOURCE,
    )

    status = models.CharField(
        max_length=20,
        choices=DocumentStatus.choices,
        default=DEFAULT_DOCUMENT_STATUS,
    )

    visibility = models.CharField(
        max_length=20,
        choices=DocumentVisibility.choices,
        default=DEFAULT_DOCUMENT_VISIBILITY,
    )

    storage_backend = models.CharField(
        max_length=20,
        choices=StorageBackend.choices,
        default=DEFAULT_STORAGE_BACKEND,
    )

    current_version = models.PositiveIntegerField(
        default=1,
    )

    tags = models.JSONField(
        default=list,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects: PatientDocumentManager = PatientDocumentManager()

    class Meta:
        verbose_name = "Patient Document"
        verbose_name_plural = "Patient Documents"

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "document_number",
                ],
                name="uq_patient_document_org_number",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
                name="idx_pd_org_patient",
            ),
            models.Index(
                fields=[
                    "organization",
                    "document_number",
                ],
                name="idx_pd_org_doc_no",
            ),
            models.Index(
                fields=[
                    "organization",
                    "category",
                ],
                name="idx_pd_org_category",
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="idx_pd_org_status",
            ),
            models.Index(
                fields=[
                    "patient",
                    "category",
                ],
                name="idx_pd_patient_category",
            ),
            models.Index(
                fields=[
                    "expires_at",
                ],
                name="idx_pd_expiry",
            ),
            models.Index(
                fields=[
                    "created_at",
                ],
                name="idx_pd_created",
            ),
        ]

    def clean(self) -> None:
        """
        Validate and normalize the model.
        """

        super().clean()

        self.document_number = self.document_number.strip().upper()
        self.title = self.title.strip()

        if (
            self.expires_at is not None
            and self.expires_at <= timezone.now()
            and self.status != DocumentStatus.EXPIRED
        ):
            raise ValidationError(
                {
                    "expires_at": (
                        "Expiry date must be in the future unless "
                        "the document status is EXPIRED."
                    ),
                },
            )

    @property
    def is_verified(self) -> bool:
        """
        Return whether the document is verified.
        """

        return self.status == DocumentStatus.VERIFIED

    @property
    def is_expired(self) -> bool:
        """
        Return whether the document has expired.
        """

        return self.expires_at is not None and self.expires_at <= timezone.now()

    @property
    def display_name(self) -> str:
        """
        Human-readable document name.
        """

        return f"{self.document_number} - {self.title}"

    def __str__(self) -> str:
        """
        String representation.
        """

        return self.display_name


__all__ = ("PatientDocument",)
