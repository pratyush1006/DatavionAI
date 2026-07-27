# apps/patient_management/identifiers/models/identifier_verification.py

"""
Patient identifier verification model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditableModel
from apps.patient_management.identifiers.constants import (
    IdentifierSource,
    VerificationStatus,
)

from .patient_identifier import PatientIdentifier


class IdentifierVerification(AuditableModel):
    """
    Stores verification history for patient identifiers.
    """

    identifier = models.ForeignKey(
        PatientIdentifier,
        on_delete=models.CASCADE,
        related_name="verification_history",
    )

    status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    verification_source = models.CharField(
        max_length=30,
        choices=IdentifierSource.choices,
        default=IdentifierSource.STAFF,
    )

    reference_number = models.CharField(
        max_length=150,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="identifier_verifications",
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Identifier Verification")
        verbose_name_plural = _("Identifier Verifications")
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=[
                    "identifier",
                ],
                name="identifier_verify_identifier_idx",
            ),
            models.Index(
                fields=[
                    "status",
                ],
                name="identifier_verify_status_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.identifier.identifier_type} - {self.status}"


__all__ = [
    "IdentifierVerification",
]
