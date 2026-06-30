"""
Shared choice constants used across Datavion.
"""

from django.db import models


class StatusChoices(models.TextChoices):
    """
    Common active/inactive status choices.
    """

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


YES_NO = (
    (True, "Yes"),
    (False, "No"),
)


__all__ = [
    "StatusChoices",
    "YES_NO",
]
