"""
Vital model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.encounters.models import Encounter
from apps.clinical.patients.models import Patient
from apps.clinical.providers.models import Provider
from apps.clinical.vitals.constants import (
    DEFAULT_TEMPERATURE_UNIT,
    DEFAULT_VITAL_STATUS,
    TemperatureUnit,
    VitalStatus,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.platform.organizations.models import Organization


class Vital(BaseModel):
    """
    Represents a complete set of patient vital signs.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="vitals",
        help_text="Organization that owns this vital record.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="vitals",
        help_text="Patient associated with this vital record.",
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="vitals",
        help_text="Provider who recorded the vitals.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name="vitals",
        help_text="Encounter during which vitals were recorded.",
    )

    recorded_at = models.DateTimeField(
        db_index=True,
        help_text="Date and time the vitals were recorded.",
    )

    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Patient height in centimeters.",
    )

    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Patient weight in kilograms.",
    )

    bmi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Calculated body mass index.",
    )

    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Body temperature.",
    )

    temperature_unit = models.CharField(
        max_length=20,
        choices=TemperatureUnit.choices,
        default=DEFAULT_TEMPERATURE_UNIT,
        db_index=True,
        help_text="Temperature measurement unit.",
    )

    pulse = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Heart rate in beats per minute.",
    )

    respiratory_rate = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Respiratory rate per minute.",
    )

    systolic_bp = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Systolic blood pressure (mmHg).",
    )

    diastolic_bp = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Diastolic blood pressure (mmHg).",
    )

    oxygen_saturation = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Oxygen saturation percentage (SpO₂).",
    )

    pain_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Pain score (0–10).",
    )

    status = models.CharField(
        max_length=20,
        choices=VitalStatus.choices,
        default=DEFAULT_VITAL_STATUS,
        db_index=True,
        help_text="Current status of the vital record.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional clinical notes.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "vitals"

        verbose_name = "Vital"

        verbose_name_plural = "Vitals"

        ordering = ("-recorded_at",)

        indexes = [
            models.Index(
                fields=["organization"],
            ),
            models.Index(
                fields=["patient"],
            ),
            models.Index(
                fields=["provider"],
            ),
            models.Index(
                fields=["encounter"],
            ),
            models.Index(
                fields=["recorded_at"],
            ),
            models.Index(
                fields=["status"],
            ),
            models.Index(
                fields=[
                    "patient",
                    "recorded_at",
                ],
            ),
            models.Index(
                fields=[
                    "encounter",
                    "recorded_at",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "encounter",
                    "recorded_at",
                ),
                name="unique_vital_record_per_encounter_time",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return a human-readable title.
        """

        return f"{self.patient.full_name} | {self.recorded_at:%Y-%m-%d %H:%M}"

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return self.title


__all__ = [
    "Vital",
]
