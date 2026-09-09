"""
Patient Consent model.

Stores tenant-scoped consent decisions and their lifecycle metadata.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import (
    BaseModel,
)
from apps.patient_management.consents.constants import (
    ConsentPurpose,
    ConsentStatus,
)
from apps.patient_management.consents.managers import (
    ConsentManager,
)
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class PatientConsent(BaseModel):
    """
    Represent a consent granted, pending, revoked, or expired for a patient.

    Patient and organization are deliberately both stored to make tenant and
    organization boundaries explicit and queryable.
    """

    objects = ConsentManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_consents",
        help_text="Organization that owns the consent.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="patient_consents",
        help_text="Patient to whom the consent applies.",
    )

    purpose = models.CharField(
        max_length=30,
        choices=ConsentPurpose.choices,
        help_text="Purpose covered by the consent.",
    )

    status = models.CharField(
        max_length=20,
        choices=ConsentStatus.choices,
        default=ConsentStatus.PENDING,
        db_index=True,
    )

    granted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    revoked_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="granted_patient_consents",
    )

    notes = models.TextField(
        blank=True,
    )

    version = models.CharField(
        max_length=50,
        blank=True,
        default="1",
    )

    evidence_reference = models.CharField(
        max_length=255,
        blank=True,
        help_text="Reference to the consent evidence or source record.",
    )

    class Meta:
        """
        Configure persistence and indexes for Patient Consents.
        """

        db_table = "patient_management_consents"
        verbose_name = "Patient Consent"
        verbose_name_plural = "Patient Consents"
        ordering = ("-created_at",)
        constraints = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "status",
                ],
                name="pm_consent_org_patient_status_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return a stable human-readable representation.
        """
        return f"{self.patient_id} - {self.purpose} - {self.status}"

    @property
    def is_granted(
        self,
    ) -> bool:
        """
        Return whether the consent is currently granted.
        """
        if self.status != ConsentStatus.GRANTED:
            return False

        if self.expires_at is not None and self.expires_at <= timezone.now():
            return False

        return True


__all__ = ("PatientConsent",)
