"""
Filters for Patient Timeline API queries.
"""

from __future__ import annotations

from django_filters import rest_framework as filters

from apps.patient_management.timeline.models.timeline import TimelineEntry


class TimelineFilter(filters.FilterSet):
    """Filter timeline entries by patient and event attributes."""

    patient = filters.UUIDFilter(field_name="patient_id")
    event_type = filters.CharFilter(field_name="event_type")
    status = filters.CharFilter(field_name="status")

    class Meta:
        """Configure filterable TimelineEntry fields."""

        model = TimelineEntry
        fields = (
            "patient",
            "event_type",
            "status",
        )


__all__ = ("TimelineFilter",)
