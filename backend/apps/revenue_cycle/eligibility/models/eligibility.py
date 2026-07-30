"""
Eligibility models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Enrollment
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import EligibilityStatus


class EligibilityCheck(BaseModel):
    """
    Eligibility check against a payer for a planned service.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="eligibility_checks",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="eligibility_checks",
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="eligibility_checks",
    )

    check_date = models.DateField(
        help_text="Date the eligibility check was performed.",
    )

    service_code = models.CharField(
        max_length=50,
        blank=True,
        help_text="Service / procedure code being checked.",
    )

    status = models.CharField(
        max_length=20,
        choices=EligibilityStatus.choices,
        default=EligibilityStatus.PENDING,
        db_index=True,
    )

    checked_by = models.CharField(
        max_length=150,
        blank=True,
    )

    benefit_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Structured benefit response from the payer.",
    )

    notes = models.TextField(
        blank=True,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        db_table = "eligibility_checks"

        verbose_name = "Eligibility Check"

        verbose_name_plural = "Eligibility Checks"

        ordering = ("-check_date",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "status",
                ],
                name="elig_org_pat_status_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Eligibility {self.patient} ({self.get_status_display()})"


__all__ = [
    "EligibilityCheck",
]
