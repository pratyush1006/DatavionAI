"""
Prescription model.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.clinical.encounters.models import Encounter
from apps.clinical.medications.models import Medication
from apps.clinical.patients.models import Patient
from apps.clinical.prescriptions.constants import (
    DEFAULT_PRESCRIPTION_FREQUENCY,
    DEFAULT_PRESCRIPTION_STATUS,
    PrescriptionFrequency,
    PrescriptionStatus,
)
from apps.clinical.providers.models import Provider
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.platform.organizations.models import Organization


class Prescription(BaseModel):
    """
    Represents a medication prescription issued during an encounter.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="prescriptions",
        help_text="Organization that owns this prescription.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="prescriptions",
        help_text="Patient receiving this prescription.",
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="prescriptions",
        help_text="Provider issuing this prescription.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name="prescriptions",
        help_text="Encounter associated with this prescription.",
    )

    medication = models.ForeignKey(
        Medication,
        on_delete=models.PROTECT,
        related_name="prescriptions",
        help_text="Medication prescribed.",
    )

    prescription_number = models.CharField(
        max_length=30,
        db_index=True,
        help_text="Unique prescription number.",
    )

    status = models.CharField(
        max_length=20,
        choices=PrescriptionStatus.choices,
        default=DEFAULT_PRESCRIPTION_STATUS,
        db_index=True,
        help_text="Prescription status.",
    )

    dosage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("1.00"),
        help_text="Dose to administer.",
    )

    dosage_unit = models.CharField(
        max_length=20,
        default="tablet",
        help_text="Dosage unit.",
    )

    frequency = models.CharField(
        max_length=20,
        choices=PrescriptionFrequency.choices,
        default=DEFAULT_PRESCRIPTION_FREQUENCY,
        db_index=True,
        help_text="Medication frequency.",
    )

    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("1.00"),
        help_text="Total quantity prescribed.",
    )

    duration_days = models.PositiveIntegerField(
        default=1,
        help_text="Treatment duration in days.",
    )

    refills = models.PositiveSmallIntegerField(
        default=0,
        help_text="Number of allowed refills.",
    )

    start_date = models.DateField(
        help_text="Prescription start date.",
    )

    end_date = models.DateField(
        help_text="Prescription end date.",
    )

    instructions = models.TextField(
        blank=True,
        help_text="Medication instructions.",
    )

    is_prn = models.BooleanField(
        default=False,
        help_text="Whether medication is taken as needed.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional clinical notes.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "prescriptions"

        verbose_name = "Prescription"

        verbose_name_plural = "Prescriptions"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "prescription_number",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "provider",
                ],
            ),
            models.Index(
                fields=[
                    "encounter",
                ],
            ),
            models.Index(
                fields=[
                    "medication",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                ],
            ),
            models.Index(
                fields=[
                    "start_date",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "prescription_number",
                ),
                name="unique_prescription_number_per_organization",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return a readable title.
        """

        return f"{self.medication.title} | {self.patient.full_name}"

    def __str__(
        self,
    ) -> str:
        """
        Return prescription display name.
        """

        return f"{self.prescription_number} | {self.title}"


__all__ = [
    "Prescription",
]
