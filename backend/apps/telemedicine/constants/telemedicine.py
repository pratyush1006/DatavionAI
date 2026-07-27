"""
Telemedicine-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class SessionStatus(models.TextChoices):
    """
    Telemedicine session lifecycle status.
    """

    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No Show"
    FAILED = "failed", "Failed"


class SessionType(models.TextChoices):
    """
    Supported telemedicine session types.
    """

    VIDEO = "video", "Video"
    AUDIO = "audio", "Audio"
    CHAT = "chat", "Chat"


class ParticipantType(models.TextChoices):
    """
    Types of participants in a telemedicine session.
    """

    PATIENT = "patient", "Patient"
    PROVIDER = "provider", "Provider"
    NURSE = "nurse", "Nurse"
    INTERPRETER = "interpreter", "Interpreter"
    OBSERVER = "observer", "Observer"


class ConnectionQuality(models.TextChoices):
    """
    Connection quality ratings.
    """

    EXCELLENT = "excellent", "Excellent"
    GOOD = "good", "Good"
    POOR = "poor", "Poor"
    DISCONNECTED = "disconnected", "Disconnected"


DEFAULT_SESSION_STATUS: Final[str] = SessionStatus.SCHEDULED


__all__ = [
    "ConnectionQuality",
    "DEFAULT_SESSION_STATUS",
    "ParticipantType",
    "SessionStatus",
    "SessionType",
]
