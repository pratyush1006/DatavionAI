"""
Patient audit log model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseModel
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


class PatientAuditLog(BaseModel):
    """
    Audit log for patient changes.
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
        choices=(
            ("create", "Create"),
            ("update", "Update"),
            ("delete", "Delete"),
            ("archive", "Archive"),
            ("restore", "Restore"),
        ),
    )

    changes = models.JSONField(
        default=dict,
        blank=True,
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_audit_logs",
    )

    performed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "patient_audit_logs"

        verbose_name = "Patient Audit Log"

        verbose_name_plural = "Patient Audit Logs"

        ordering = ("-performed_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "action",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                    "performed_at",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.action} - {self.patient}"


__all__ = [
    "PatientAuditLog",
]
