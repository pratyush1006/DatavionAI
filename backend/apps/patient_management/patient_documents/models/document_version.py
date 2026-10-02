"""Version history for Patient Documents."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patient_documents.constants import (
    DocumentVersionStatus,
)
from apps.patient_management.patient_documents.models.patient_document import (
    PatientDocument,
)
from apps.platform.accounts.models import User


class PatientDocumentVersion(BaseModel):
    """Immutable metadata record for one patient-document version."""

    patient_document = models.ForeignKey(
        PatientDocument,
        on_delete=models.CASCADE,
        related_name="versions",
    )

    version_number = models.PositiveIntegerField()

    storage_key = models.CharField(
        max_length=500,
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True,
    )

    mime_type = models.CharField(
        max_length=150,
        blank=True,
    )

    file_size = models.PositiveBigIntegerField(
        default=0,
    )

    checksum = models.CharField(
        max_length=255,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=DocumentVersionStatus.choices,
        default=DocumentVersionStatus.ACTIVE,
    )

    notes = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_patient_document_versions",
    )

    class Meta:
        """Database metadata for document versions."""

        db_table = "patient_document_versions"

        ordering = ("-version_number",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "patient_document",
                    "version_number",
                ),
                name="uq_patient_document_version_number",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    version_number__gt=0,
                ),
                name="ck_patient_document_version_positive",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "patient_document",
                    "version_number",
                ),
                name="pdv_document_version_idx",
            ),
            models.Index(
                fields=(
                    "patient_document",
                    "status",
                ),
                name="pdv_document_status_idx",
            ),
            models.Index(
                fields=("checksum",),
                name="pdv_checksum_idx",
            ),
        ]

    IMMUTABLE_FIELDS = frozenset(
        {
            "patient_document_id",
            "version_number",
            "storage_key",
            "original_filename",
            "mime_type",
            "file_size",
            "checksum",
            "notes",
            "created_by_id",
        }
    )

    def save(
        self,
        *args,
        **kwargs,
    ):
        """Prevent modification of immutable version metadata."""
        if not self._state.adding:
            existing = type(self).objects.get(
                pk=self.pk,
            )
            changed = {
                field
                for field in self.IMMUTABLE_FIELDS
                if getattr(existing, field) != getattr(self, field)
            }
            if changed:
                raise ValidationError(
                    "Document version metadata is immutable: "
                    + ", ".join(sorted(changed)),
                )
        return super().save(
            *args,
            **kwargs,
        )

    def delete(
        self,
        *args,
        **kwargs,
    ):
        """Reject deletion of document-version history."""
        raise ValidationError(
            "Document versions are immutable and cannot be deleted.",
        )

    def restore(
        self,
    ):
        """Reject restoration of document-version history."""
        raise ValidationError(
            "Document versions are immutable and cannot be restored.",
        )

    def clean(
        self,
    ) -> None:
        """Validate version metadata."""
        super().clean()
        if self.version_number < 1:
            raise ValidationError(
                "Document version number must be positive.",
            )

    def __str__(
        self,
    ) -> str:
        """Return a version label."""
        return f"{self.patient_document_id} v{self.version_number}"


__all__ = ("PatientDocumentVersion",)
