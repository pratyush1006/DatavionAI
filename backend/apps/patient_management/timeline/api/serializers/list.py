"""
Patient Timeline list serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.timeline.models.timeline import TimelineEntry


class TimelineListSerializer(serializers.ModelSerializer):
    """Serialize timeline entries for collection responses."""

    class Meta:
        """Configure list serializer fields."""

        model = TimelineEntry
        fields = (
            "id",
            "patient",
            "event_type",
            "title",
            "occurred_at",
            "status",
        )


__all__ = ("TimelineListSerializer",)
