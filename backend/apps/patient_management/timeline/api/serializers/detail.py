"""
Patient Timeline detail serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.timeline.models.timeline import TimelineEntry


class TimelineDetailSerializer(serializers.ModelSerializer):
    """Serialize a complete timeline entry."""

    class Meta:
        """Configure detail serializer fields."""

        model = TimelineEntry
        fields = (
            "id",
            "organization",
            "patient",
            "event_type",
            "title",
            "description",
            "occurred_at",
            "status",
            "metadata",
            "created_by",
            "created_at",
            "updated_at",
            "is_active",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
        )


__all__ = ("TimelineDetailSerializer",)
