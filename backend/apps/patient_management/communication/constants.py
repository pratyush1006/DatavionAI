"""
Constants for the Communication module.
"""

from __future__ import annotations

from django.db import models


class CommunicationChannel(models.TextChoices):
    """
    Channel used for patient communication.
    """

    EMAIL = "email", "Email"

    SMS = "sms", "SMS"

    PHONE = "phone", "Phone"

    PORTAL = "portal", "Patient Portal"

    POST = "post", "Postal Mail"

    IN_APP = "in_app", "In App"


class CommunicationDirection(models.TextChoices):
    """
    Direction of the communication.
    """

    INBOUND = "inbound", "Inbound"

    OUTBOUND = "outbound", "Outbound"


class CommunicationStatus(models.TextChoices):
    """
    Delivery status of the communication.
    """

    PENDING = "pending", "Pending"

    SENT = "sent", "Sent"

    DELIVERED = "delivered", "Delivered"

    READ = "read", "Read"

    FAILED = "failed", "Failed"


__all__ = [
    "CommunicationChannel",
    "CommunicationDirection",
    "CommunicationStatus",
]
