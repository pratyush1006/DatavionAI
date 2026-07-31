"""
Referrals models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.referrals.constants import (
    ReferralPriority,
    ReferralStatus,
    ReferralUrgency,
)
from apps.platform.organizations.models import Organization


class PatientReferral(BaseModel):
    """
    A referral of a patient to another provider or department.
    """

    objects = BaseManager()

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
        help_text="Unique referral reference number.",
    )

    referring_provider = models.CharField(
        max_length=150,
        blank=True,
        help_text="Provider making the referral.",
    )

    referred_to = models.CharField(
        max_length=150,
        help_text="Provider / department referred to.",
    )

    referred_to_organization = models.CharField(
        max_length=255,
        blank=True,
        help_text="External organization being referred to.",
    )

    reason = models.TextField(
        help_text="Reason for the referral.",
    )

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
        default=ReferralStatus.PENDING,
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

    class Meta:
        db_table = "patient_referrals"

        verbose_name = "Patient Referral"

        verbose_name_plural = "Patient Referrals"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "status",
                ],
                name="referral_org_pat_status_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "referral_number",
                ],
                name="unique_referral_number_per_organization",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Referral {self.referral_number} ({self.get_status_display()})"


__all__ = [
    "PatientReferral",
]
