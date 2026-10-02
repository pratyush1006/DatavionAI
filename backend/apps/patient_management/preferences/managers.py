"""Managers for Patient Preferences."""

from __future__ import annotations

from apps.core.models.managers import SoftDeleteManager
from apps.patient_management.preferences.querysets import (
    PatientCommunicationPreferenceQuerySet,
    PatientPreferenceQuerySet,
)


class PatientPreferenceManager(SoftDeleteManager):
    """Default manager for alive Patient Preference records."""

    _queryset_class = PatientPreferenceQuerySet


class PatientCommunicationPreferenceManager(SoftDeleteManager):
    """Default manager for alive communication preference records."""

    _queryset_class = PatientCommunicationPreferenceQuerySet


__all__ = (
    "PatientCommunicationPreferenceManager",
    "PatientPreferenceManager",
)
