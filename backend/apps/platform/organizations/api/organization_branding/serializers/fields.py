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
    "logo_path",
    "primary_color",
    "theme_mode",
)

# ---------------------------------------------------------------------
# Detail Serializer
# ---------------------------------------------------------------------

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "logo_path",
    "favicon_path",
    "primary_color",
    "secondary_color",
    "accent_color",
    "font_family",
    "theme_mode",
    "login_message",
    "created_at",
    "updated_at",
)

# ---------------------------------------------------------------------
# Create Serializer
# ---------------------------------------------------------------------

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "logo_path",
    "favicon_path",
    "primary_color",
    "secondary_color",
    "accent_color",
    "font_family",
    "theme_mode",
    "login_message",
)

# ---------------------------------------------------------------------
# Update Serializer
# ---------------------------------------------------------------------

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "logo_path",
    "favicon_path",
    "primary_color",
    "secondary_color",
    "accent_color",
    "font_family",
    "theme_mode",
    "login_message",
)

__all__: tuple[str, ...] = (
    "_LIST_FIELDS",
    "_DETAIL_FIELDS",
    "_WRITE_FIELDS",
    "_UPDATE_FIELDS",
)
