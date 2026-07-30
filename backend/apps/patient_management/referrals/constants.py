"""
Constants for the Referrals module.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.constants import (
    ReferralPriority,
    ReferralStatus,
)


class ReferralUrgency(models.TextChoices):
    """
    Clinical urgency of the referral.
    """

    ROUTINE = "routine", "Routine"

    PRIORITY = "priority", "Priority"

    URGENT = "urgent", "Urgent"


__all__ = [
    "ReferralPriority",
    "ReferralStatus",
    "ReferralUrgency",
]
