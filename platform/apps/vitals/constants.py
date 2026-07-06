"""
Constants for the Vitals application.
"""

from __future__ import annotations

from django.db import models


class VitalStatus(models.TextChoices):
    """
    Status of a vital record.
    """

    PRELIMINARY = "preliminary", "Preliminary"

    FINAL = "final", "Final"

    AMENDED = "amended", "Amended"

    CANCELLED = "cancelled", "Cancelled"


DEFAULT_VITAL_STATUS = VitalStatus.FINAL


class TemperatureUnit(models.TextChoices):
    """
    Unit of temperature measurement.
    """

    CELSIUS = "celsius", "Celsius"

    FAHRENHEIT = "fahrenheit", "Fahrenheit"


DEFAULT_TEMPERATURE_UNIT = TemperatureUnit.CELSIUS


MIN_PAIN_SCORE = 0

MAX_PAIN_SCORE = 10

MIN_SPO2 = 0

MAX_SPO2 = 100

MIN_HEART_RATE = 0

MIN_RESPIRATORY_RATE = 0

MIN_SYSTOLIC_BP = 0

MIN_DIASTOLIC_BP = 0
