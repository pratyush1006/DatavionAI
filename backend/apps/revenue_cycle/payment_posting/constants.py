"""Constants and lifecycle values for payment posting."""

from __future__ import annotations

from django.db import models


class PaymentPostingStatus(models.TextChoices):
    """Lifecycle states for a posted payment."""

    PENDING = "pending", "Pending"
    POSTED = "posted", "Posted"
    REVERSED = "reversed", "Reversed"
    VOIDED = "voided", "Voided"


class PaymentPostingSource(models.TextChoices):
    """Supported payment posting sources."""

    MANUAL = "manual", "Manual"
    ERA = "era", "ERA"
    EOB = "eob", "EOB"
    PATIENT = "patient", "Patient"
    ADJUSTMENT = "adjustment", "Adjustment"


__all__ = ("PaymentPostingSource", "PaymentPostingStatus")
