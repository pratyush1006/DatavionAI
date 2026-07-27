"""
Patient insurance enrollment model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models.plan import InsurancePlan
from apps.platform.organizations.models import Organization


class Enrollment(BaseModel):
    """
    Represents a patient's enrollment in an insurance plan.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Organization that owns the enrollment.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Patient covered by the enrollment.",
    )

    plan = models.ForeignKey(
        InsurancePlan,
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Insurance plan the patient is enrolled in.",
    )

    member_id = models.CharField(
        max_length=100,
        help_text="Member identifier assigned by the insurer.",
    )

    group_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Insurance group number.",
    )

    effective_date = models.DateField(
        help_text="Date the coverage becomes effective.",
    )

    expiration_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the coverage expires.",
    )

    coverage_percentage = models.PositiveSmallIntegerField(
        default=100,
        help_text="Percentage of costs covered by the plan.",
    )

    is_primary = models.BooleanField(
        default=True,
        help_text="Whether this is the patient's primary coverage.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether the enrollment is currently active.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the enrollment was created.",
    )

    class Meta:
        db_table = "insurance_enrollments"

        verbose_name = "Enrollment"

        verbose_name_plural = "Enrollments"

        ordering = (
            "patient",
            "effective_date",
        )

        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "is_active",
                ],
                name="enrollment_patient_active_idx",
            ),
            models.Index(
                fields=[
                    "plan",
                    "effective_date",
                ],
                name="enrollment_plan_effective_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name="enrollment_org_active_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Return the enrollment display name.
        """

        return f"{self.patient} - {self.plan} ({self.member_id})"


__all__ = [
    "Enrollment",
]
