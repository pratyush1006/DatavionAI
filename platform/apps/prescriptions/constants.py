"""
Prescription constants.
"""

from __future__ import annotations

from django.db import models


class PrescriptionStatus(models.TextChoices):
    """
    Prescription status choices.
    """

    ACTIVE = (
        "active",
        "Active",
    )

    COMPLETED = (
        "completed",
        "Completed",
    )

    CANCELLED = (
        "cancelled",
        "Cancelled",
    )

    ON_HOLD = (
        "on_hold",
        "On Hold",
    )

    EXPIRED = (
        "expired",
        "Expired",
    )


class PrescriptionFrequency(models.TextChoices):
    """
    Prescription frequency choices.
    """

    ONCE_DAILY = (
        "once_daily",
        "OD - Once Daily",
    )

    TWICE_DAILY = (
        "twice_daily",
        "BD - Twice Daily",
    )

    THREE_TIMES_DAILY = (
        "three_times_daily",
        "TDS - Three Times Daily",
    )

    FOUR_TIMES_DAILY = (
        "four_times_daily",
        "QID - Four Times Daily",
    )

    EVERY_OTHER_DAY = (
        "every_other_day",
        "Alternate Days",
    )

    WEEKLY = (
        "weekly",
        "Weekly",
    )

    MONTHLY = (
        "monthly",
        "Monthly",
    )

    AS_NEEDED = (
        "as_needed",
        "SOS - As Needed",
    )

    BEDTIME = (
        "bedtime",
        "HS - Bedtime",
    )


DEFAULT_PRESCRIPTION_STATUS = (
    PrescriptionStatus.ACTIVE
)

DEFAULT_PRESCRIPTION_FREQUENCY = (
    PrescriptionFrequency.ONCE_DAILY
)


__all__ = [
    "DEFAULT_PRESCRIPTION_FREQUENCY",
    "DEFAULT_PRESCRIPTION_STATUS",
    "PrescriptionFrequency",
    "PrescriptionStatus",
]