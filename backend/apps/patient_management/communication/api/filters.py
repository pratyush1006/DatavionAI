"""Patient Communication API filters."""

from __future__ import annotations

from django_filters import rest_framework as filters

from apps.patient_management.communication.models import PatientCommunication


class CommunicationFilter(filters.FilterSet):
    """Filter communications by patient, channel, status and type."""

    class Meta:
        """Filter metadata."""

        model = PatientCommunication
        fields = (
            "patient",
            "organization",
            "channel",
            "direction",
            "communication_type",
            "status",
        )


__all__ = ("CommunicationFilter",)
