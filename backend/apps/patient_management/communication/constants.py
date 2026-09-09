"""Patient Communication domain constants."""

from __future__ import annotations

from django.db import models


class CommunicationChannel(models.TextChoices):
    """Supported patient communication channels."""

    SMS = "sms", "SMS"
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"
    PORTAL = "portal", "Patient Portal"
    LETTER = "letter", "Letter"
    IN_PERSON = "in_person", "In Person"
    OTHER = "other", "Other"


class CommunicationDirection(models.TextChoices):
    """Direction of a communication interaction."""

    OUTBOUND = "outbound", "Outbound"
    INBOUND = "inbound", "Inbound"


class CommunicationStatus(models.TextChoices):
    """Lifecycle status of a communication interaction."""

    DRAFT = "draft", "Draft"
    QUEUED = "queued", "Queued"
    SENT = "sent", "Sent"
    DELIVERED = "delivered", "Delivered"
    READ = "read", "Read"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"
    ARCHIVED = "archived", "Archived"


class CommunicationType(models.TextChoices):
    """Business classification for a communication."""

    GENERAL = "general", "General"
    APPOINTMENT = "appointment", "Appointment"
    CLINICAL = "clinical", "Clinical"
    BILLING = "billing", "Billing"
    FOLLOW_UP = "follow_up", "Follow Up"
    REMINDER = "reminder", "Reminder"
    ADMINISTRATIVE = "administrative", "Administrative"


__all__ = (
    "CommunicationChannel",
    "CommunicationDirection",
    "CommunicationStatus",
    "CommunicationType",
)
