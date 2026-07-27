"""
Performance management constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class ReviewCycleStatus(TextChoices):
    """
    Performance review cycle status choices.
    """

    UPCOMING = "upcoming", "Upcoming"
    ACTIVE = "active", "Active"
    CLOSED = "closed", "Closed"


class PerformanceReviewStatus(TextChoices):
    """
    Performance review workflow status choices.
    """

    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    ACKNOWLEDGED = "acknowledged", "Acknowledged"
    COMPLETED = "completed", "Completed"


class GoalStatus(TextChoices):
    """
    Performance goal progress status choices.
    """

    NOT_STARTED = "not_started", "Not Started"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    DEFERRED = "deferred", "Deferred"


DEFAULT_REVIEW_CYCLE_STATUS = ReviewCycleStatus.UPCOMING
DEFAULT_PERFORMANCE_REVIEW_STATUS = PerformanceReviewStatus.DRAFT
DEFAULT_GOAL_STATUS = GoalStatus.NOT_STARTED


__all__ = [
    "ReviewCycleStatus",
    "PerformanceReviewStatus",
    "GoalStatus",
    "DEFAULT_REVIEW_CYCLE_STATUS",
    "DEFAULT_PERFORMANCE_REVIEW_STATUS",
    "DEFAULT_GOAL_STATUS",
]
