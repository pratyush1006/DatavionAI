"""
Compliance models: consent and PHI access audit.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.compliance.constants import (
    ConsentPurpose,
    ConsentStatus,
    PhiAccessAction,
)
from apps.core.models import BaseManager, BaseModel
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


class Consent(BaseModel):
    """
    Patient consent for a specific purpose.
    """

    objects = BaseManager()

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="consents",
        help_text="Patient granting consent.",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="consents",
        help_text="Organization the consent applies to.",
    )

    purpose = models.CharField(
        max_length=30,
        choices=ConsentPurpose.CHOICES,
        help_text="Purpose the consent covers.",
    )

    status = models.CharField(
        max_length=20,
        choices=ConsentStatus.CHOICES,
        default=ConsentStatus.PENDING,
        db_index=True,
    )

    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="granted_consents",
        null=True,
        blank=True,
    )

    granted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "compliance_consents"

        verbose_name = "Consent"

        verbose_name_plural = "Consents"

        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Return a readable label."""

        return f"Consent {self.purpose} ({self.status})"


class PhiAccessLog(BaseModel):
    """
    Audit record for any access to protected health information.
    """

    objects = BaseManager()

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="phi_access_logs",
        null=True,
        blank=True,
        help_text="User or system actor that accessed PHI.",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="phi_access_logs",
        null=True,
        blank=True,
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        related_name="phi_access_logs",
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=20,
        choices=PhiAccessAction.CHOICES,
        help_text="Type of PHI access performed.",
    )

    resource_type = models.CharField(
        max_length=60,
        blank=True,
        help_text="Affected model, e.g. ClinicalNote.",
    )

    resource_id = models.CharField(
        max_length=60,
        blank=True,
        help_text="Primary key of the affected record.",
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    justification = models.TextField(
        blank=True,
        help_text="Business reason for access, where required.",
    )

    class Meta:
        db_table = "compliance_phi_access_logs"

        verbose_name = "PHI Access Log"

        verbose_name_plural = "PHI Access Logs"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=["patient", "action"],
                name="phi_log_patient_action_idx",
            ),
            models.Index(
                fields=["actor", "created_at"],
                name="phi_log_actor_time_idx",
            ),
        ]

    def __str__(self) -> str:
        """Return a readable label."""

        return f"PHI {self.action} by {self.actor_id}"


__all__ = [
    "Consent",
    "PhiAccessLog",
]
