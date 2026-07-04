"""
Appointment model.
"""

from __future__ import annotations

from django.db import models

from apps.appointments.constants import (
    AppointmentPriority,
    AppointmentStatus,
    AppointmentType,
    DEFAULT_APPOINTMENT_PRIORITY,
    DEFAULT_APPOINTMENT_STATUS,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.organizations.models import Organization
from apps.patients.models import Patient
from apps.providers.models import Provider


class Appointment(BaseModel):
    """
    Represents a patient appointment.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="appointments",
        help_text="Organization that owns this appointment.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
        help_text="Patient for the appointment.",
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="appointments",
        help_text="Healthcare provider assigned to the appointment.",
    )

    appointment_number = models.CharField(
        max_length=30,
        help_text="Unique appointment number.",
    )

    appointment_type = models.CharField(
        max_length=30,
        choices=AppointmentType.choices,
        help_text="Appointment type.",
    )

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=DEFAULT_APPOINTMENT_STATUS,
        db_index=True,
        help_text="Appointment status.",
    )

    priority = models.CharField(
        max_length=20,
        choices=AppointmentPriority.choices,
        default=DEFAULT_APPOINTMENT_PRIORITY,
        help_text="Appointment priority.",
    )

    scheduled_start = models.DateTimeField(
        help_text="Scheduled appointment start.",
    )

    scheduled_end = models.DateTimeField(
        help_text="Scheduled appointment end.",
    )

    duration_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Appointment duration in minutes.",
    )

    reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Reason for appointment.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional appointment notes.",
    )

    check_in_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Patient check-in time.",
    )

    check_out_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Patient check-out time.",
    )

    cancellation_reason = models.TextField(
        blank=True,
        help_text="Reason for cancellation.",
    )

    is_virtual = models.BooleanField(
        default=False,
        help_text="Whether this is a virtual appointment.",
    )

    meeting_url = models.URLField(
        blank=True,
        help_text="Virtual meeting URL.",
    )

    class Meta:
        db_table = "appointments"

        verbose_name = "Appointment"

        verbose_name_plural = "Appointments"

        ordering = (
            "-scheduled_start",
        )

        indexes = [
            models.Index(
                fields=[
                    "appointment_number",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                ],
            ),
            models.Index(
                fields=[
                    "scheduled_start",
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
                    "provider",
                    "scheduled_start",
                ],
            ),
            models.Index(
                fields=[
                    "patient",
                    "scheduled_start",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "appointment_number",
                ],
                name="unique_appointment_number_per_organization",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return appointment title.
        """

        return (
            f"{self.appointment_number} | "
            f"{self.patient.full_name} | "
            f"{self.provider.employee.full_name}"
        )

    def __str__(
        self,
    ) -> str:
        """
        Return appointment display string.
        """

        return (
            f"{self.appointment_number} | "
            f"{self.patient.full_name} | "
            f"{self.provider.employee.full_name}"
        )


__all__ = [
    "Appointment",
]
