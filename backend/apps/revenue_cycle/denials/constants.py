"""Denial lifecycle and domain constants."""

from __future__ import annotations

from django.db import models


class DenialStatus(models.TextChoices):
    """Supported denial lifecycle states."""

    OPEN = "open", "Open"
    UNDER_REVIEW = "under_review", "Under Review"
    ACTION_REQUIRED = "action_required", "Action Required"
    APPEAL_PENDING = "appeal_pending", "Appeal Pending"
    RESOLVED = "resolved", "Resolved"
    WRITTEN_OFF = "written_off", "Written Off"


class DenialPriority(models.TextChoices):
    """Operational denial priorities."""

    LOW = "low", "Low"
    NORMAL = "normal", "Normal"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


DENIAL_TRANSITIONS = {
    DenialStatus.OPEN: {
        DenialStatus.UNDER_REVIEW,
        DenialStatus.ACTION_REQUIRED,
        DenialStatus.WRITTEN_OFF,
    },
    DenialStatus.UNDER_REVIEW: {
        DenialStatus.ACTION_REQUIRED,
        DenialStatus.APPEAL_PENDING,
        DenialStatus.RESOLVED,
        DenialStatus.WRITTEN_OFF,
    },
    DenialStatus.ACTION_REQUIRED: {
        DenialStatus.UNDER_REVIEW,
        DenialStatus.APPEAL_PENDING,
        DenialStatus.RESOLVED,
        DenialStatus.WRITTEN_OFF,
    },
    DenialStatus.APPEAL_PENDING: {
        DenialStatus.UNDER_REVIEW,
        DenialStatus.RESOLVED,
        DenialStatus.WRITTEN_OFF,
    },
    DenialStatus.RESOLVED: set(),
    DenialStatus.WRITTEN_OFF: set(),
}
__all__ = ("DenialStatus", "DenialPriority", "DENIAL_TRANSITIONS")
