"""
Patient Portal account model.

The Patient foreign key is intentionally bound to the canonical Patient
aggregate in apps.patient_management.patients.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.portal.constants import (
    PortalAccountStatus,
    PortalAuthProvider,
)
from apps.patient_management.portal.managers import PatientPortalAccountManager
from apps.platform.organizations.models import Organization


class PatientPortalAccount(BaseModel):
    """Patient-facing portal account linked to exactly one patient."""

    objects = PatientPortalAccountManager()

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
    )

    email = models.EmailField(
        blank=True,
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
        """Database metadata for portal accounts."""

        db_table = "patient_portal_accounts"
        ordering = ("username",)

        indexes = [
            models.Index(
                fields=("organization", "patient", "status"),
                name="portal_org_patient_status_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=("organization", "username"),
                name="unique_portal_username_per_org",
            ),
        ]

    def __str__(self) -> str:
        """Return a human-readable account representation."""

        return f"Portal - {self.username} ({self.get_status_display()})"


__all__ = ("PatientPortalAccount",)
