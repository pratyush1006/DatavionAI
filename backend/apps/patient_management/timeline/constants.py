"""
Constants for the Timeline module.
"""

from __future__ import annotations

from django.db import models


class TimelineEventType(models.TextChoices):
    """
    Category of timeline event.
    """

    REGISTRATION = "registration", "Registration"

    APPOINTMENT = "appointment", "Appointment"

    ENCOUNTER = "encounter", "Encounter"

    DIAGNOSIS = "diagnosis", "Diagnosis"

    MEDICATION = "medication", "Medication"

    LAB = "lab", "Lab Result"

    DOCUMENT = "document", "Document"

    COMMUNICATION = "communication", "Communication"

    CONSENT = "consent", "Consent"

    REFERRAL = "referral", "Referral"

    NOTE = "note", "Note"

    SYSTEM = "system", "System"


class TimelineEventVisibility(models.TextChoices):
    """
    Visibility of the timeline event.
    """

    PUBLIC = "public", "Public"

    INTERNAL = "internal", "Internal"

    PATIENT = "patient", "Patient Visible"


__all__ = [
    "TimelineEventVisibility",
    "TimelineEventType",
]
