"""
Shift scheduling constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class ShiftAssignmentStatus(TextChoices):
    """
    Shift assignment workflow status choices.
    """

    SCHEDULED = "scheduled", "Scheduled"
    COMPLETED = "completed", "Completed"
    ABSENT = "absent", "Absent"
    SWAPPED = "swapped", "Swapped"
    CANCELLED = "cancelled", "Cancelled"


DEFAULT_SHIFT_ASSIGNMENT_STATUS = ShiftAssignmentStatus.SCHEDULED


__all__ = [
    "ShiftAssignmentStatus",
    "DEFAULT_SHIFT_ASSIGNMENT_STATUS",
]
