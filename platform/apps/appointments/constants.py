"""
Appointment constants.
"""

from __future__ import annotations

from django.db import models


class AppointmentStatus(
    models.TextChoices,
):
    """
    Appointment lifecycle status.
    """

    SCHEDULED = (
        "scheduled",
        "Scheduled",
    )

    CONFIRMED = (
        "confirmed",
        "Confirmed",
    )

    CHECKED_IN = (
        "checked_in",
        "Checked In",
    )

    IN_PROGRESS = (
        "in_progress",
        "In Progress",
    )

    COMPLETED = (
        "completed",
        "Completed",
    )

    CANCELLED = (
        "cancelled",
        "Cancelled",
    )

    NO_SHOW = (
        "no_show",
        "No Show",
    )


class AppointmentType(
    models.TextChoices,
):
    """
    Appointment types.
    """

    CONSULTATION = (
        "consultation",
        "Consultation",
    )

    FOLLOW_UP = (
        "follow_up",
        "Follow-up",
    )

    EMERGENCY = (
        "emergency",
        "Emergency",
    )

    SURGERY = (
        "surgery",
        "Surgery",
    )

    PROCEDURE = (
        "procedure",
        "Procedure",
    )

    TELECONSULTATION = (
        "teleconsultation",
        "Teleconsultation",
    )


class AppointmentPriority(
    models.TextChoices,
):
    """
    Appointment priority.
    """

    LOW = (
        "low",
        "Low",
    )

    NORMAL = (
        "normal",
        "Normal",
    )

    HIGH = (
        "high",
        "High",
    )

    URGENT = (
        "urgent",
        "Urgent",
    )


DEFAULT_APPOINTMENT_STATUS = AppointmentStatus.SCHEDULED


DEFAULT_APPOINTMENT_PRIORITY = AppointmentPriority.NORMAL


__all__ = [
    "AppointmentPriority",
    "AppointmentStatus",
    "AppointmentType",
    "DEFAULT_APPOINTMENT_PRIORITY",
    "DEFAULT_APPOINTMENT_STATUS",
]
