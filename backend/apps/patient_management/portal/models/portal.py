"""
Patient Portal models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.portal.constants import (
    PortalAccountStatus,
    PortalAuthProvider,
)
from apps.platform.organizations.models import Organization


class PatientPortalAccount(BaseModel):
    """
    Patient-facing portal account linked to a patient record.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_portal_accounts",
    )

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="portal_account",
    )

    username = models.CharField(
        max_length=150,
        help_text="Portal login username.",
    )

    email = models.EmailField(
        blank=True,
        help_text="Portal login email.",
    )

    status = models.CharField(
        max_length=20,
        choices=PortalAccountStatus.choices,
        default=PortalAccountStatus.INVITED,
        db_index=True,
    )

    auth_provider = models.CharField(
        max_length=20,
        choices=PortalAuthProvider.choices,
        default=PortalAuthProvider.LOCAL,
    )

    invitation_sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    activated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_login_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    email_verified = models.BooleanField(
        default=False,
    )

    two_factor_enabled = models.BooleanField(
        default=False,
    )

    preferred_language = models.CharField(
        max_length=50,
        default="English",
    )

    class Meta:
        db_table = "patient_portal_accounts"

        verbose_name = "Patient Portal Account"

        verbose_name_plural = "Patient Portal Accounts"

        ordering = ("username",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
                name="portal_org_patient_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "username",
                ],
                name="unique_portal_username_per_organization",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Portal - {self.username} ({self.get_status_display()})"


__all__ = [
    "PatientPortalAccount",
]
