"""
Constants for the Geography bounded context.
"""

from __future__ import annotations

from django.db import models


class AdministrativeRegionType(
    models.TextChoices,
):
    """
    Administrative region classification.

    Values are intentionally generic so the model can represent
    administrative divisions across different countries.
    """

    STATE = "state", "State"
    PROVINCE = "province", "Province"
    TERRITORY = "territory", "Territory"
    REGION = "region", "Region"
    DISTRICT = "district", "District"


DEFAULT_REGION_TYPE = AdministrativeRegionType.STATE


__all__: tuple[str, ...] = (
    "AdministrativeRegionType",
    "DEFAULT_REGION_TYPE",
)
