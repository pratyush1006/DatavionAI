"""
Patient Timeline creation serializer.

Validation and payload preparation only.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.timeline.constants import TimelineEventType
from apps.patient_management.timeline.models import TimelineEntry


class TimelineCreateSerializer(serializers.ModelSerializer):
    """Validate Patient Timeline creation input."""

    patient_id = serializers.UUIDField()
    organization_id = serializers.UUIDField()

    class Meta:
        """Configure creation serializer fields."""

        model = TimelineEntry
        fields = (
            "organization_id",
            "patient_id",
            "event_type",
            "title",
            "description",
            "occurred_at",
            "metadata",
        )

    def validate_event_type(
        self,
        value: str,
    ) -> str:
        """Validate the supplied event type."""

        valid_values = {choice[0] for choice in TimelineEventType.choices}

        if value not in valid_values:
            raise serializers.ValidationError(
                "Unsupported timeline event type.",
            )

        return value


__all__ = ("TimelineCreateSerializer",)
