"""
Constants for the Patient Preferences module.
"""

from __future__ import annotations

from django.db.models import TextChoices


class Language(TextChoices):
    """
    Supported patient languages.
    """

    ENGLISH = (
        "en",
        "English",
    )

    HINDI = (
        "hi",
        "Hindi",
    )

    TAMIL = (
        "ta",
        "Tamil",
    )

    TELUGU = (
        "te",
        "Telugu",
    )

    KANNADA = (
        "kn",
        "Kannada",
    )

    MALAYALAM = (
        "ml",
        "Malayalam",
    )

    BENGALI = (
        "bn",
        "Bengali",
    )

    MARATHI = (
        "mr",
        "Marathi",
    )

    GUJARATI = (
        "gu",
        "Gujarati",
    )

    PUNJABI = (
        "pa",
        "Punjabi",
    )


class CommunicationChannel(TextChoices):
    """
    Preferred communication channels.
    """

    EMAIL = (
        "email",
        "Email",
    )

    SMS = (
        "sms",
        "SMS",
    )

    WHATSAPP = (
        "whatsapp",
        "WhatsApp",
    )

    PHONE = (
        "phone",
        "Phone Call",
    )

    PUSH = (
        "push",
        "Push Notification",
    )


class ReminderPreference(TextChoices):
    """
    Appointment reminder preferences.
    """

    NONE = (
        "none",
        "None",
    )

    ONE_HOUR = (
        "1h",
        "1 Hour Before",
    )

    SIX_HOURS = (
        "6h",
        "6 Hours Before",
    )

    TWELVE_HOURS = (
        "12h",
        "12 Hours Before",
    )

    ONE_DAY = (
        "24h",
        "1 Day Before",
    )

    TWO_DAYS = (
        "48h",
        "2 Days Before",
    )


class ThemePreference(TextChoices):
    """
    Patient portal theme.
    """

    SYSTEM = (
        "system",
        "System",
    )

    LIGHT = (
        "light",
        "Light",
    )

    DARK = (
        "dark",
        "Dark",
    )


class PreferenceStatus(TextChoices):
    """
    Preference status.
    """

    ACTIVE = (
        "active",
        "Active",
    )

    INACTIVE = (
        "inactive",
        "Inactive",
    )


__all__ = [
    "CommunicationChannel",
    "Language",
    "PreferenceStatus",
    "ReminderPreference",
    "ThemePreference",
]
