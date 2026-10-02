"""
Patient Referral domain model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.referrals.constants import (
    ReferralPriority,
    ReferralStatus,
    ReferralUrgency,
)
from apps.patient_management.referrals.managers import PatientReferralManager
from apps.platform.organizations.models import Organization


class PatientReferral(BaseModel):
    """
    Referral of a patient to an internal or external provider or service.

    The organization and patient must belong to the same tenant and
    organization boundary. Lifecycle changes are performed by services.
    """

    objects = PatientReferralManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_referrals",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="referrals",
    )
    referral_number = models.CharField(
        max_length=40,
        help_text="Unique referral reference number within the organization.",
    )
    referring_provider = models.CharField(
        max_length=150,
        blank=True,
    )
    referred_to = models.CharField(
        max_length=150,
    )
    referred_to_organization = models.CharField(
        max_length=255,
        blank=True,
    )
    reason = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=ReferralPriority.choices,
        default=ReferralPriority.ROUTINE,
    )
    urgency = models.CharField(
        max_length=20,
        choices=ReferralUrgency.choices,
        default=ReferralUrgency.ROUTINE,
    )
    status = models.CharField(
        max_length=20,
        choices=ReferralStatus.choices,
        default=ReferralStatus.DRAFT,
        db_index=True,
    )
    clinical_notes = models.TextField(
        blank=True,
    )
    requested_date = models.DateField(
        null=True,
        blank=True,
    )
    appointment_date = models.DateField(
        null=True,
        blank=True,
    )
    completed_date = models.DateField(
        null=True,
        blank=True,
    )
    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_by_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
    )
    updated_by_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        """Database metadata for Patient Referral."""

        db_table = "patient_referrals"
        verbose_name = "Patient Referral"
        verbose_name_plural = "Patient Referrals"
        ordering = ("-created_at",)
        indexes = (
            models.Index(
                fields=("organization", "patient", "status"),
                name="referral_org_pat_status_idx",
            ),
            models.Index(
                fields=("organization", "referral_number"),
                name="referral_org_number_idx",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "referral_number"),
                name="unique_referral_number_per_organization",
            ),
        )

    def clean(self) -> None:
        """Validate model-level referral invariants."""

        super().clean()

        if self.organization_id and self.patient_id:
            if self.patient.organization_id != self.organization_id:
                raise ValidationError(
                    "Patient and referral organization must match.",
                )

            if self.patient.tenant_id != self.organization.tenant_id:
                raise ValidationError(
                    "Patient and referral tenant must match.",
                )

    def __str__(self) -> str:
        """Return a human-readable referral representation."""

        return f"Referral {self.referral_number} ({self.get_status_display()})"


__all__ = ("PatientReferral",)
