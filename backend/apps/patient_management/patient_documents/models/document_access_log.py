"""Audit log for patient-document access."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patient_documents.constants import (
    DocumentAccessAction,
)
from apps.patient_management.patient_documents.models.patient_document import (
    PatientDocument,
)
from apps.platform.accounts.models import User


class PatientDocumentAccessLog(BaseModel):
    """Record an auditable access operation against a patient document."""

    patient_document = models.ForeignKey(
        PatientDocument,
        on_delete=models.CASCADE,
        related_name="access_logs",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_document_access_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=DocumentAccessAction.choices,
    )

    accessed_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.CharField(
        max_length=1000,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    def save(
        self,
        *args,
        **kwargs,
    ):
        """Prevent modification of an existing access audit record."""
        if not self._state.adding:
            raise ValidationError(
                "Document access audit records are immutable.",
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
        """Reject deletion of document access audit history."""
        raise ValidationError(
            "Document access audit records cannot be deleted.",
        )

    def restore(
        self,
    ):
        """Reject restoration of document access audit history."""
        raise ValidationError(
            "Document access audit records cannot be restored.",
        )

    class Meta:
        """Database metadata for document access audit records."""

        db_table = "patient_document_access_logs"

        ordering = ("-accessed_at",)

        indexes = [
            models.Index(
                fields=(
                    "patient_document",
                    "accessed_at",
                ),
                name="pdal_document_access_idx",
            ),
            models.Index(
                fields=(
                    "user",
                    "accessed_at",
                ),
                name="pdal_user_access_idx",
            ),
            models.Index(
                fields=(
                    "action",
                    "accessed_at",
                ),
                name="pdal_action_access_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """Return an audit-log label."""
        return f"{self.action} - {self.patient_document_id}"


__all__ = ("PatientDocumentAccessLog",)
