"""Constants for Revenue Cycle analytics."""

from __future__ import annotations

from django.db import models


class AnalyticsPeriod(models.TextChoices):
    """Supported analytics aggregation periods."""

    DAY = "DAY", "Day"
    WEEK = "WEEK", "Week"
    MONTH = "MONTH", "Month"
    QUARTER = "QUARTER", "Quarter"
    YEAR = "YEAR", "Year"


__all__ = ("AnalyticsPeriod",)
