"""Canonical Clinical Appointment model."""

from __future__ import annotations

from datetime import timedelta
from decimal import ROUND_HALF_UP, Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.clinical.appointments.constants import (
    AppointmentPriority,
    AppointmentStatus,
    AppointmentType,
)
from apps.clinical.providers.models import Provider
from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class Appointment(BaseModel):
    """Store an organization-scoped clinical appointment."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="clinical_appointments",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="clinical_appointments",
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        related_name="clinical_appointments",
    )
    appointment_number = models.CharField(
        max_length=64,
        unique=True,
    )
    client_booking_key = models.CharField(max_length=128, blank=True, default="")
    booking_request_fingerprint = models.CharField(
        max_length=64, blank=True, default=""
    )
    appointment_type = models.CharField(
        max_length=32,
        choices=AppointmentType.choices,
        default=AppointmentType.IN_PERSON,
    )
    status = models.CharField(
        max_length=32,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED,
        db_index=True,
    )
    priority = models.CharField(
        max_length=32,
        choices=AppointmentPriority.choices,
        default=AppointmentPriority.ROUTINE,
        db_index=True,
    )
    scheduled_start = models.DateTimeField(db_index=True)
    scheduled_end = models.DateTimeField(db_index=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    reschedule_count = models.PositiveSmallIntegerField(default=0)
    consultation_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    deposit_invoice_id = models.UUIDField(null=True, blank=True)
    final_invoice_id = models.UUIDField(null=True, blank=True)
    deposit_paid = models.BooleanField(default=False)
    tracking_token_hash = models.CharField(max_length=64, blank=True, default="")
    reason = models.TextField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    check_in_at = models.DateTimeField(null=True, blank=True)
    check_out_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, default="")
    is_virtual = models.BooleanField(default=False)
    meeting_url = models.URLField(blank=True, default="")

    class Meta:
        """Define database indexes and constraints."""

        ordering = ("scheduled_start", "appointment_number")
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "client_booking_key"),
                condition=~models.Q(client_booking_key=""),
                name="appt_org_client_booking_key_uniq",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    scheduled_end__gt=models.F("scheduled_start"),
                ),
                name="appointment_end_after_start",
            ),
            models.CheckConstraint(
                condition=models.Q(duration_minutes__gt=0),
                name="appointment_duration_positive",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "scheduled_start"),
                name="appt_org_start_idx",
            ),
            models.Index(
                fields=("provider", "scheduled_start"),
                name="appt_provider_start_idx",
            ),
            models.Index(
                fields=("patient", "scheduled_start"),
                name="appt_patient_start_idx",
            ),
        )

    def clean(self) -> None:
        """Validate appointment invariants."""

        errors = {}

        if self.scheduled_end <= self.scheduled_start:
            errors["scheduled_end"] = "Appointment end time must be after start time."

        duration = int(
            (self.scheduled_end - self.scheduled_start).total_seconds() // 60
        )

        if duration <= 0:
            errors["duration_minutes"] = (
                "Appointment duration must be greater than zero."
            )

        if self.is_virtual and not self.meeting_url:
            errors["meeting_url"] = "Meeting URL is required for virtual appointments."

        if (
            self.status == AppointmentStatus.CANCELLED
            and not self.cancellation_reason.strip()
        ):
            errors["cancellation_reason"] = "Cancellation reason is required."

        self.duration_minutes = max(duration, 1)

        if errors:
            raise ValidationError(errors)

    @property
    def is_terminal(self) -> bool:
        """Return whether the appointment is in a terminal state."""

        return self.status in {
            AppointmentStatus.COMPLETED,
            AppointmentStatus.CANCELLED,
            AppointmentStatus.NO_SHOW,
        }

    @property
    def deposit_amount(self) -> Decimal:
        """Return the 50% booking deposit rounded to currency precision."""

        return (self.consultation_fee / Decimal("2")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def tracking_token(self) -> str:
        """Return the one-time plaintext tracking token for a new booking."""

        return getattr(self, "_tracking_token", "")

    @tracking_token.setter
    def tracking_token(self, value: str) -> None:
        self._tracking_token = value

    @property
    def can_reschedule(self) -> bool:
        """Return whether rescheduling remains inside policy limits."""

        return (
            not self.is_terminal
            and self.reschedule_count == 0
            and timezone.now() < self.scheduled_start - timedelta(hours=6)
        )

    def __str__(self) -> str:
        """Return the appointment number."""

        return self.appointment_number


__all__ = ("Appointment",)
