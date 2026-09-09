"""Constants and enumerations for Patient Preferences."""

from __future__ import annotations

from enum import StrEnum


class PreferenceChannel(StrEnum):
    """Supported patient communication channels."""

    EMAIL = "EMAIL"
    SMS = "SMS"
    PHONE = "PHONE"
    PUSH = "PUSH"
    PORTAL = "PORTAL"


class PreferenceLanguage(StrEnum):
    """Common supported language identifiers."""

    ENGLISH = "en"
    HINDI = "hi"


class PreferenceDateFormat(StrEnum):
    """Supported display date formats."""

    ISO = "YYYY-MM-DD"
    DMY = "DD-MM-YYYY"
    MDY = "MM-DD-YYYY"


class PreferenceTimeFormat(StrEnum):
    """Supported display time formats."""

    TWELVE_HOUR = "12H"
    TWENTY_FOUR_HOUR = "24H"


DEFAULT_LANGUAGE = PreferenceLanguage.ENGLISH
DEFAULT_TIMEZONE = "UTC"
DEFAULT_DATE_FORMAT = PreferenceDateFormat.ISO
DEFAULT_TIME_FORMAT = PreferenceTimeFormat.TWENTY_FOUR_HOUR

__all__ = (
    "DEFAULT_DATE_FORMAT",
    "DEFAULT_LANGUAGE",
    "DEFAULT_TIMEZONE",
    "DEFAULT_TIME_FORMAT",
    "PreferenceChannel",
    "PreferenceDateFormat",
    "PreferenceLanguage",
    "PreferenceTimeFormat",
)
