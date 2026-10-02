"""
Holiday calendar constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class HolidayType(TextChoices):
    """
    Whether a holiday applies to everyone or is optional/
    restricted, where employees choose whether to take it.
    """

    MANDATORY = "mandatory", "Mandatory"
    OPTIONAL = "optional", "Optional"


DEFAULT_HOLIDAY_TYPE = HolidayType.MANDATORY


__all__ = [
    "HolidayType",
    "DEFAULT_HOLIDAY_TYPE",
]
