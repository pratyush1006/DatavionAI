"""
Constants for the Patient Consents domain.
"""

from __future__ import annotations

from django.db import models


class ConsentPurpose(models.TextChoices):
    """
    Supported purposes for a patient consent.
    """

    TREATMENT = "treatment", "Treatment"
    PAYMENT = "payment", "Payment"
    OPERATIONS = "operations", "Operations"
    RESEARCH = "research", "Research"


class ConsentStatus(models.TextChoices):
    """
    Lifecycle states for a patient consent.
    """

    PENDING = "pending", "Pending"
    GRANTED = "granted", "Granted"
    REVOKED = "revoked", "Revoked"
    EXPIRED = "expired", "Expired"


__all__ = (
    "ConsentPurpose",
    "ConsentStatus",
)
