"""Filtering support for patient emergency API endpoints."""

from __future__ import annotations

from django_filters import rest_framework as filters

from apps.patient_management.emergency.models import EmergencyContact


class EmergencyFilter(filters.FilterSet):
    """Filter emergency contacts by patient, status, and priority."""

    class Meta:
        """Define filterable emergency fields."""

        model = EmergencyContact
        fields = (
            "patient",
            "status",
            "priority",
            "relationship",
        )


__all__ = ("EmergencyFilter",)
