"""
Reusable choice constants shared across the application.
"""

from __future__ import annotations

from django.db import models


class ActiveStatusChoices(models.TextChoices):
    """
    Common active/inactive status choices.
    """

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


YES_NO: tuple[tuple[bool, str], ...] = (
    (True, "Yes"),
    (False, "No"),
)


__all__ = [
    "ActiveStatusChoices",
    "YES_NO",
]
