"""
Constants and enumerations for Patient Timeline.
"""

from __future__ import annotations

from django.db import models


class TimelineEventType(models.TextChoices):
    """Supported patient timeline event types."""

    CLINICAL = "clinical", "Clinical"
    APPOINTMENT = "appointment", "Appointment"
    MEDICATION = "medication", "Medication"
    DOCUMENT = "document", "Document"
    COMMUNICATION = "communication", "Communication"
    SYSTEM = "system", "System"


class TimelineStatus(models.TextChoices):
    """Lifecycle states for timeline entries."""

    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"


__all__ = (
    "TimelineEventType",
    "TimelineStatus",
)
