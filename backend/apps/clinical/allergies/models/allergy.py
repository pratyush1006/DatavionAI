"""
Allergy model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.allergies.constants import (
    DEFAULT_ALLERGY_CATEGORY,
    DEFAULT_ALLERGY_SEVERITY,
    DEFAULT_ALLERGY_STATUS,
    AllergyCategory,
    AllergySeverity,
    AllergyStatus,
)
from apps.clinical.encounters.models import Encounter
from apps.clinical.patients.models import Patient
from apps.clinical.providers.models import Provider
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.platform.organizations.models import Organization


class Allergy(BaseModel):
    """
    Represents a patient allergy recorded during an encounter.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="allergies",
        help_text="Organization that owns this allergy.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="allergies",
        help_text="Patient with this allergy.",
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="allergies",
        help_text="Provider who recorded this allergy.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name="allergies",
        help_text="Encounter associated with this allergy.",
    )

    allergen = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Allergen name.",
    )

    category = models.CharField(
        max_length=20,
        choices=AllergyCategory.choices,
        default=DEFAULT_ALLERGY_CATEGORY,
        db_index=True,
        help_text="Allergy category.",
    )

    severity = models.CharField(
        max_length=20,
        choices=AllergySeverity.choices,
        default=DEFAULT_ALLERGY_SEVERITY,
        db_index=True,
        help_text="Allergy severity.",
    )

    status = models.CharField(
        max_length=20,
        choices=AllergyStatus.choices,
        default=DEFAULT_ALLERGY_STATUS,
        db_index=True,
        help_text="Current allergy status.",
    )

    reaction = models.TextField(
        blank=True,
        help_text="Observed allergic reaction.",
    )

    onset_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the allergy was first identified.",
    )

    resolved_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the allergy resolved.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional clinical notes.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "allergies"

        verbose_name = "Allergy"

        verbose_name_plural = "Allergies"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
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
                    "allergen",
                ],
            ),
            models.Index(
                fields=[
                    "category",
                ],
            ),
            models.Index(
                fields=[
                    "severity",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                    "allergen",
                ),
                name="unique_patient_allergy_per_organization",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return a readable title.
        """

        return f"{self.allergen} | {self.get_severity_display()}"

    def __str__(
        self,
    ) -> str:
        """
        Return allergy display name.
        """

        return self.title


__all__ = [
    "Allergy",
]
