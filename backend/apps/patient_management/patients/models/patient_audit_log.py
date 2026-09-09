"""
Patient Core audit log model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models.patient import Patient
from apps.platform.organizations.models import Organization


class PatientAuditAction(models.TextChoices):
    """
    Supported patient lifecycle audit actions.
    """

    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    DELETE = "delete", "Delete"
    ARCHIVE = "archive", "Archive"
    RESTORE = "restore", "Restore"


class PatientAuditLog(BaseModel):
    """
    Immutable-oriented audit record for patient lifecycle operations.

    Audit records are associated with both the organization and patient so
    tenant-scoped audit queries remain efficient and explicit.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_audit_logs",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=PatientAuditAction.choices,
    )

    changes = models.JSONField(
        default=dict,
        blank=True,
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="patient_audit_logs",
        null=True,
        blank=True,
    )

    performed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "patient_audit_logs"

        ordering = ("-performed_at",)

        verbose_name = "Patient Audit Log"
        verbose_name_plural = "Patient Audit Logs"

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "action",
                ],
                name="patient_aud_organiz_7c4759_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "performed_at",
                ],
                name="patient_aud_organiz_373d9b_idx",
            ),
        ]


__all__ = [
    "PatientAuditAction",
    "PatientAuditLog",
]
