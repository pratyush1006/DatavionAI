"""
Filters for the Patient Preferences API.
"""

from __future__ import annotations

from django_filters import rest_framework as filters

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)


class PatientPreferenceFilter(
    filters.FilterSet,
):
    """
    Filter set for patient preferences.
    """

    patient = filters.UUIDFilter(
        field_name="patient__uuid",
    )

    organization = filters.UUIDFilter(
        field_name="organization__uuid",
    )

    language = filters.CharFilter()

    status = filters.CharFilter()

    class Meta:
        model = PatientPreference

        fields = (
            "organization",
            "patient",
            "language",
            "status",
        )


class PatientCommunicationPreferenceFilter(
    filters.FilterSet,
):
    """
    Filter set for patient communication preferences.
    """

    patient = filters.UUIDFilter(
        field_name="patient__uuid",
    )

    organization = filters.UUIDFilter(
        field_name="organization__uuid",
    )

    channel = filters.CharFilter()

    enabled = filters.BooleanFilter()

    class Meta:
        model = PatientCommunicationPreference

        fields = (
            "organization",
            "patient",
            "channel",
            "enabled",
        )


__all__ = [
    "PatientCommunicationPreferenceFilter",
    "PatientPreferenceFilter",
]
