"""
Patient Timeline update serializer.

Validation and payload preparation only.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.timeline.models import TimelineEntry


class TimelineUpdateSerializer(serializers.ModelSerializer):
    """Validate mutable Patient Timeline fields."""

    class Meta:
        """Configure update serializer fields."""

        model = TimelineEntry
        fields = (
            "event_type",
            "title",
            "description",
            "occurred_at",
            "metadata",
        )


__all__ = ("TimelineUpdateSerializer",)
