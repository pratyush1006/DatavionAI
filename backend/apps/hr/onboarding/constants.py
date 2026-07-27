"""
Onboarding/offboarding constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class LifecycleProcessType(TextChoices):
    """
    Whether a lifecycle process is bringing an employee in or
    taking them out.
    """

    ONBOARDING = "onboarding", "Onboarding"
    OFFBOARDING = "offboarding", "Offboarding"


class LifecycleProcessStatus(TextChoices):
    """
    Overall workflow status of a lifecycle process.
    """

    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class LifecycleTaskStatus(TextChoices):
    """
    Workflow status of a single lifecycle task.
    """

    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    SKIPPED = "skipped", "Skipped"


class LifecycleTaskCategory(TextChoices):
    """
    Functional area responsible for a lifecycle task.
    """

    HR = "hr", "HR"
    IT = "it", "IT"
    FACILITIES = "facilities", "Facilities"
    FINANCE = "finance", "Finance"
    MANAGER = "manager", "Manager"
    OTHER = "other", "Other"


DEFAULT_LIFECYCLE_PROCESS_STATUS = LifecycleProcessStatus.IN_PROGRESS
DEFAULT_LIFECYCLE_TASK_STATUS = LifecycleTaskStatus.PENDING
DEFAULT_LIFECYCLE_TASK_CATEGORY = LifecycleTaskCategory.HR


__all__ = [
    "LifecycleProcessType",
    "LifecycleProcessStatus",
    "LifecycleTaskStatus",
    "LifecycleTaskCategory",
    "DEFAULT_LIFECYCLE_PROCESS_STATUS",
    "DEFAULT_LIFECYCLE_TASK_STATUS",
    "DEFAULT_LIFECYCLE_TASK_CATEGORY",
]
