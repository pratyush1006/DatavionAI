"""
Serializer field definitions for Organization Branding.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------
# List Serializer
# ---------------------------------------------------------------------

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "logo",
    "primary_color",
    "theme_mode",
)

# ---------------------------------------------------------------------
# Detail Serializer
# ---------------------------------------------------------------------

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "logo",
    "favicon",
    "primary_color",
    "font_family",
    "theme_mode",
    "created_at",
    "updated_at",
)

# ---------------------------------------------------------------------
# Create Serializer
# ---------------------------------------------------------------------

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "logo",
    "favicon",
    "primary_color",
    "font_family",
    "theme_mode",
)

# ---------------------------------------------------------------------
# Update Serializer
# ---------------------------------------------------------------------

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "logo",
    "favicon",
    "primary_color",
    "font_family",
    "theme_mode",
)

__all__: tuple[str, ...] = (
    "_LIST_FIELDS",
    "_DETAIL_FIELDS",
    "_WRITE_FIELDS",
    "_UPDATE_FIELDS",
)
