"""
Medication model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.medications.constants import (
    DEFAULT_DOSAGE_FORM,
    DEFAULT_ROUTE,
    MedicationDosageForm,
    MedicationRoute,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.platform.organizations.models import Organization


class Medication(BaseModel):
    """
    Represents a medication in the master catalog.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="medications",
        help_text="Organization that owns this medication.",
    )

    medication_code = models.CharField(
        max_length=30,
        help_text="Unique medication code.",
    )

    generic_name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Generic medication name.",
    )

    brand_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Brand name.",
    )

    strength = models.CharField(
        max_length=50,
        help_text="Medication strength.",
    )

    strength_unit = models.CharField(
        max_length=20,
        help_text="Strength unit.",
    )

    dosage_form = models.CharField(
        max_length=30,
        choices=MedicationDosageForm.choices,
        default=DEFAULT_DOSAGE_FORM,
        db_index=True,
        help_text="Medication dosage form.",
    )

    route = models.CharField(
        max_length=30,
        choices=MedicationRoute.choices,
        default=DEFAULT_ROUTE,
        db_index=True,
        help_text="Administration route.",
    )

    manufacturer = models.CharField(
        max_length=255,
        blank=True,
        help_text="Medication manufacturer.",
    )

    description = models.TextField(
        blank=True,
        help_text="Medication description.",
    )

    is_controlled = models.BooleanField(
        default=False,
        help_text="Whether this medication is a controlled substance.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "medications"

        verbose_name = "Medication"

        verbose_name_plural = "Medications"

        ordering = ("generic_name",)

        indexes = [
            models.Index(
                fields=[
                    "medication_code",
                ],
            ),
            models.Index(
                fields=[
                    "generic_name",
                ],
            ),
            models.Index(
                fields=[
                    "brand_name",
                ],
            ),
            models.Index(
                fields=[
                    "dosage_form",
                ],
            ),
            models.Index(
                fields=[
                    "route",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                ],
            ),
            models.Index(
                fields=[
                    "generic_name",
                    "strength",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "medication_code",
                ),
                name="unique_medication_code_per_organization",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return medication title.
        """

        if self.brand_name:
            return (
                f"{self.generic_name} "
                f"{self.strength}{self.strength_unit} "
                f"({self.brand_name})"
            )

        return f"{self.generic_name} {self.strength}{self.strength_unit}"

    def __str__(
        self,
    ) -> str:
        """
        Return medication display string.
        """

        return f"{self.medication_code} | {self.title}"


__all__ = [
    "Medication",
]
