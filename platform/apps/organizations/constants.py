"""
Organization-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class OrganizationType(models.TextChoices):
    """
    Supported organization types.
    """

    HOSPITAL = "hospital", "Hospital"
    CLINIC = "clinic", "Clinic"
    LABORATORY = "laboratory", "Laboratory"
    CORPORATE = "corporate", "Corporate"


DEFAULT_ORGANIZATION_TYPE: Final[str] = OrganizationType.HOSPITAL


__all__ = [
    "DEFAULT_ORGANIZATION_TYPE",
    "OrganizationType",
]
