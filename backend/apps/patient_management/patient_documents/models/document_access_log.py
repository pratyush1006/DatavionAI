"""
Patient document access log model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from ..constants import DocumentAction
from .patient_document import PatientDocument


class DocumentAccessLog(BaseModel):
    """
    Audit log for patient document access.
    """

    document = models.ForeignKey(
        PatientDocument,
        on_delete=models.CASCADE,
        related_name="access_logs",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="patient_document_access_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=DocumentAction.choices,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        verbose_name = "Document Access Log"

        verbose_name_plural = "Document Access Logs"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "document",
                ],
            ),
            models.Index(
                fields=[
                    "user",
                ],
            ),
            models.Index(
                fields=[
                    "action",
                ],
            ),
            models.Index(
                fields=[
                    "created_at",
                ],
            ),
        ]

    def __str__(self) -> str:
        """
        Return the string representation.
        """

        return f"{self.document.document_number} - {self.action}"


__all__ = [
    "DocumentAccessLog",
]
