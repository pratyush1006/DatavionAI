"""
Diagnosis model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.diagnoses.constants import (
    DiagnosisStatus,
    DiagnosisType,
)
from apps.encounters.models import Encounter
from apps.organizations.models import Organization


class Diagnosis(BaseModel):
    """
    Represents an ICD-10 diagnosis recorded during an encounter.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="diagnoses",
        help_text="Organization that owns this diagnosis.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name="diagnoses",
        help_text="Encounter associated with this diagnosis.",
    )

    diagnosis_code = models.CharField(
        max_length=20,
        db_index=True,
        help_text="ICD-10 diagnosis code.",
    )

    diagnosis_description = models.TextField(
        help_text="Diagnosis description.",
    )

    diagnosis_type = models.CharField(
        max_length=20,
        choices=DiagnosisType.choices,
        default=DiagnosisType.PRIMARY,
        db_index=True,
        help_text="Diagnosis type.",
    )

    status = models.CharField(
        max_length=20,
        choices=DiagnosisStatus.choices,
        default=DiagnosisStatus.ACTIVE,
        db_index=True,
        help_text="Diagnosis status.",
    )

    is_primary = models.BooleanField(
        default=False,
        help_text="Whether this is the primary diagnosis.",
    )

    present_on_admission = models.BooleanField(
        default=False,
        help_text="Whether the diagnosis was present on admission.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional clinical notes.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "diagnoses"

        verbose_name = "Diagnosis"

        verbose_name_plural = "Diagnoses"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "diagnosis_code",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "diagnosis_type",
                ],
            ),
            models.Index(
                fields=[
                    "encounter",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                ],
            ),
            models.Index(
                fields=[
                    "encounter",
                    "is_primary",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "encounter",
                    "diagnosis_code",
                ],
                name="unique_diagnosis_per_encounter",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return diagnosis title.
        """

        return f"{self.diagnosis_code} | {self.diagnosis_description}"

    def __str__(
        self,
    ) -> str:
        """
        Return diagnosis display string.
        """

        return f"{self.diagnosis_code} | {self.diagnosis_description}"


__all__ = [
    "Diagnosis",
]
