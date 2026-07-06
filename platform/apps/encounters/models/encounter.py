"""
Encounter model.
"""

from __future__ import annotations

from django.db import models

from apps.appointments.models import Appointment
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.encounters.constants import (
    DEFAULT_ENCOUNTER_STATUS,
    EncounterStatus,
)
from apps.organizations.models import Organization
from apps.patients.models import Patient
from apps.providers.models import Provider


class Encounter(BaseModel):
    """
    Represents a patient clinical encounter.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="encounters",
        help_text="Organization that owns this encounter.",
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="encounter",
        help_text="Appointment associated with this encounter.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="encounters",
        help_text="Patient for this encounter.",
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="encounters",
        help_text="Healthcare provider for this encounter.",
    )

    encounter_number = models.CharField(
        max_length=30,
        help_text="Unique encounter number.",
    )

    status = models.CharField(
        max_length=20,
        choices=EncounterStatus.choices,
        default=DEFAULT_ENCOUNTER_STATUS,
        db_index=True,
        help_text="Encounter status.",
    )

    chief_complaint = models.TextField(
        blank=True,
        help_text="Primary reason for the encounter.",
    )

    history_of_present_illness = models.TextField(
        blank=True,
        help_text="History of present illness.",
    )

    assessment = models.TextField(
        blank=True,
        help_text="Clinical assessment.",
    )

    plan = models.TextField(
        blank=True,
        help_text="Treatment plan.",
    )

    clinical_notes = models.TextField(
        blank=True,
        help_text="Clinical notes.",
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Encounter start time.",
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Encounter end time.",
    )

    duration_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Encounter duration in minutes.",
    )

    is_billable = models.BooleanField(
        default=True,
        help_text="Whether the encounter is billable.",
    )

    class Meta:
        db_table = "encounters"

        verbose_name = "Encounter"

        verbose_name_plural = "Encounters"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "encounter_number",
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
                    "appointment",
                ],
            ),
            models.Index(
                fields=[
                    "started_at",
                ],
            ),
            models.Index(
                fields=[
                    "provider",
                    "started_at",
                ],
            ),
            models.Index(
                fields=[
                    "patient",
                    "started_at",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "encounter_number",
                ],
                name="unique_encounter_number_per_organization",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return encounter title.
        """

        return (
            f"{self.encounter_number} | "
            f"{self.patient.full_name} - "
            f"{self.provider.employee.full_name}"
        )

    def __str__(
        self,
    ) -> str:
        """
        Return encounter display string.
        """

        return (
            f"{self.encounter_number} | "
            f"{self.patient.full_name} | "
            f"{self.provider.employee.full_name}"
        )


__all__ = [
    "Encounter",
]
