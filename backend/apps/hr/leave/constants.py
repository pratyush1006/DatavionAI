"""
Leave constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class LeaveRequestStatus(TextChoices):
    """
    Leave request workflow status choices.
    """

    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    CANCELLED = "cancelled", "Cancelled"


DEFAULT_LEAVE_REQUEST_STATUS = LeaveRequestStatus.PENDING


__all__ = [
    "LeaveRequestStatus",
    "DEFAULT_LEAVE_REQUEST_STATUS",
]
