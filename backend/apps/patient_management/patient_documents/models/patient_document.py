"""Patient document aggregate."""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AllObjectsManager, BaseModel
from apps.patient_management.patient_documents.constants import (
    PatientDocumentCategory,
    PatientDocumentStatus,
)
from apps.patient_management.patient_documents.managers import (
    PatientDocumentManager,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


class PatientDocument(BaseModel):
    """Represent a document associated with a canonical patient record."""

    objects = PatientDocumentManager()
    all_objects = AllObjectsManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_documents",
        help_text=_("Organization owning the patient document."),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="patient_documents",
        help_text=_("Canonical patient owning the document."),
    )

    title = models.CharField(
        _("Title"),
        max_length=255,
    )

    category = models.CharField(
        _("Category"),
        max_length=40,
        choices=PatientDocumentCategory.choices,
        default=PatientDocumentCategory.OTHER,
        db_index=True,
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=PatientDocumentStatus.choices,
        default=PatientDocumentStatus.DRAFT,
        db_index=True,
    )

    description = models.TextField(
        _("Description"),
        blank=True,
    )

    original_filename = models.CharField(
        _("Original Filename"),
        max_length=255,
        blank=True,
    )

    storage_key = models.CharField(
        _("Storage Key"),
        max_length=500,
    )

    mime_type = models.CharField(
        _("MIME Type"),
        max_length=150,
        blank=True,
    )

    file_size = models.PositiveBigIntegerField(
        _("File Size"),
        default=0,
    )

    checksum = models.CharField(
        _("Checksum"),
        max_length=255,
        blank=True,
    )

    is_confidential = models.BooleanField(
        _("Confidential"),
        default=False,
        db_index=True,
    )

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        blank=True,
    )

    uploaded_at = models.DateTimeField(
        _("Uploaded At"),
        null=True,
        blank=True,
    )

    archived_at = models.DateTimeField(
        _("Archived At"),
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_patient_documents",
    )

    class Meta:
        """Database metadata for the patient document aggregate."""

        db_table = "patient_documents"

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "storage_key",
                ),
                name="uq_patient_document_org_storage_key",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "organization",
                    "patient",
                    "status",
                ),
                name="pd_org_patient_status_idx",
            ),
            models.Index(
                fields=(
                    "organization",
                    "category",
                    "created_at",
                ),
                name="pd_org_category_created_idx",
            ),
            models.Index(
                fields=(
                    "patient",
                    "created_at",
                ),
                name="pd_patient_created_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """Return a human-readable document label."""
        return f"{self.title} - {self.patient_id}"


__all__ = ("PatientDocument",)
