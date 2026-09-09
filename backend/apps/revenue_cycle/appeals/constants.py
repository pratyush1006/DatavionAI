"""
Lifecycle constants for Revenue Cycle Appeals.
"""

from __future__ import annotations

from django.db import models


class AppealStatus(models.TextChoices):
    """Supported appeal lifecycle states."""

    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    UNDER_REVIEW = "under_review", "Under Review"
    PENDING_INFORMATION = "pending_information", "Pending Information"
    APPROVED = "approved", "Approved"
    PARTIALLY_APPROVED = "partially_approved", "Partially Approved"
    DENIED = "denied", "Denied"
    WITHDRAWN = "withdrawn", "Withdrawn"
    CLOSED = "closed", "Closed"


ALLOWED_TRANSITIONS = {
    AppealStatus.DRAFT: {
        AppealStatus.SUBMITTED,
        AppealStatus.WITHDRAWN,
    },
    AppealStatus.SUBMITTED: {
        AppealStatus.UNDER_REVIEW,
        AppealStatus.PENDING_INFORMATION,
        AppealStatus.WITHDRAWN,
    },
    AppealStatus.UNDER_REVIEW: {
        AppealStatus.PENDING_INFORMATION,
        AppealStatus.APPROVED,
        AppealStatus.PARTIALLY_APPROVED,
        AppealStatus.DENIED,
    },
    AppealStatus.PENDING_INFORMATION: {
        AppealStatus.UNDER_REVIEW,
        AppealStatus.WITHDRAWN,
    },
    AppealStatus.APPROVED: {AppealStatus.CLOSED},
    AppealStatus.PARTIALLY_APPROVED: {AppealStatus.CLOSED},
    AppealStatus.DENIED: {AppealStatus.CLOSED},
    AppealStatus.WITHDRAWN: set(),
    AppealStatus.CLOSED: set(),
}


__all__ = ("AppealStatus", "ALLOWED_TRANSITIONS")
