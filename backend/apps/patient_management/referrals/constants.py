"""
Constants and lifecycle definitions for Patient Referrals.
"""

from __future__ import annotations

from django.db import models


class ReferralPriority(models.TextChoices):
    """Priority assigned to a patient referral."""

    ROUTINE = "ROUTINE", "Routine"
    URGENT = "URGENT", "Urgent"
    STAT = "STAT", "Stat"


class ReferralUrgency(models.TextChoices):
    """Clinical urgency assigned to a referral."""

    ROUTINE = "ROUTINE", "Routine"
    URGENT = "URGENT", "Urgent"
    EMERGENT = "EMERGENT", "Emergent"


class ReferralStatus(models.TextChoices):
    """Lifecycle states supported by a referral."""

    DRAFT = "DRAFT", "Draft"
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    SCHEDULED = "SCHEDULED", "Scheduled"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    DECLINED = "DECLINED", "Declined"
    CANCELLED = "CANCELLED", "Cancelled"


REFERRAL_TRANSITIONS = {
    ReferralStatus.DRAFT: frozenset(
        {
            ReferralStatus.PENDING,
            ReferralStatus.CANCELLED,
        }
    ),
    ReferralStatus.PENDING: frozenset(
        {
            ReferralStatus.ACCEPTED,
            ReferralStatus.DECLINED,
            ReferralStatus.CANCELLED,
        }
    ),
    ReferralStatus.ACCEPTED: frozenset(
        {
            ReferralStatus.SCHEDULED,
            ReferralStatus.CANCELLED,
        }
    ),
    ReferralStatus.SCHEDULED: frozenset(
        {
            ReferralStatus.IN_PROGRESS,
            ReferralStatus.CANCELLED,
        }
    ),
    ReferralStatus.IN_PROGRESS: frozenset(
        {
            ReferralStatus.COMPLETED,
            ReferralStatus.CANCELLED,
        }
    ),
    ReferralStatus.COMPLETED: frozenset(),
    ReferralStatus.DECLINED: frozenset(),
    ReferralStatus.CANCELLED: frozenset(),
}


def is_valid_referral_transition(
    current_status: str,
    target_status: str,
) -> bool:
    """Return whether a referral may move between two lifecycle states."""

    if current_status == target_status:
        return True

    return target_status in REFERRAL_TRANSITIONS.get(
        current_status,
        frozenset(),
    )


__all__ = (
    "REFERRAL_TRANSITIONS",
    "ReferralPriority",
    "ReferralStatus",
    "ReferralUrgency",
    "is_valid_referral_transition",
)
