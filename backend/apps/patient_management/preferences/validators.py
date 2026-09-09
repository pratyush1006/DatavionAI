"""Validation helpers for Patient Preferences."""

from __future__ import annotations

from apps.patient_management.preferences.constants import (
    PreferenceDateFormat,
    PreferenceLanguage,
    PreferenceTimeFormat,
)
from apps.patient_management.preferences.exceptions import PreferenceValidationError


def validate_preference_data(data):
    """Validate supported display preference values."""

    language = data.get("language")
    date_format = data.get("date_format")
    time_format = data.get("time_format")

    if language and language not in {item.value for item in PreferenceLanguage}:
        raise PreferenceValidationError("Unsupported preference language.")

    if date_format and date_format not in {item.value for item in PreferenceDateFormat}:
        raise PreferenceValidationError("Unsupported preference date format.")

    if time_format and time_format not in {item.value for item in PreferenceTimeFormat}:
        raise PreferenceValidationError("Unsupported preference time format.")

    return data


__all__ = ("validate_preference_data",)
