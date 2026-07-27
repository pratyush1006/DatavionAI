"""
Organization branding constants.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class OrganizationBrandingThemeMode(
    StrEnum,
):
    """
    Supported branding theme modes.
    """

    LIGHT = "light"

    DARK = "dark"

    SYSTEM = "system"

    @classmethod
    def choices(
        cls,
    ) -> tuple[tuple[str, str], ...]:
        """
        Return Django-compatible choices.
        """
        return (
            (cls.LIGHT, "Light"),
            (cls.DARK, "Dark"),
            (cls.SYSTEM, "Follow System"),
        )


DEFAULT_ORGANIZATION_BRANDING_THEME_MODE: Final[str] = (
    OrganizationBrandingThemeMode.LIGHT
)

DEFAULT_ORGANIZATION_BRANDING_PRIMARY_COLOR: Final[str] = "#1A73E8"

DEFAULT_ORGANIZATION_BRANDING_FONT_FAMILY: Final[str] = "Inter"


__all__: tuple[str, ...] = (
    "OrganizationBrandingThemeMode",
    "DEFAULT_ORGANIZATION_BRANDING_THEME_MODE",
    "DEFAULT_ORGANIZATION_BRANDING_PRIMARY_COLOR",
    "DEFAULT_ORGANIZATION_BRANDING_FONT_FAMILY",
)
