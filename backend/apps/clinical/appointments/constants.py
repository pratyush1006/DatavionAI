"""Constants for Clinical Appointments."""

from __future__ import annotations

from django.db import models


class AppointmentType(models.TextChoices):
    """Supported appointment types."""

    IN_PERSON = "in_person", "In Person"
    VIRTUAL = "virtual", "Virtual"
    FOLLOW_UP = "follow_up", "Follow Up"
    CONSULTATION = "consultation", "Consultation"
    PROCEDURE = "procedure", "Procedure"
    EMERGENCY = "emergency", "Emergency"


class AppointmentStatus(models.TextChoices):
    """Supported appointment lifecycle states."""

    SCHEDULED = "scheduled", "Scheduled"
    CONFIRMED = "confirmed", "Confirmed"
    CHECKED_IN = "checked_in", "Checked In"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No Show"


class AppointmentPriority(models.TextChoices):
    """Supported appointment priorities."""

    ROUTINE = "routine", "Routine"
    URGENT = "urgent", "Urgent"
    EMERGENCY = "emergency", "Emergency"


__all__ = (
    "AppointmentPriority",
    "AppointmentStatus",
    "AppointmentType",
)
