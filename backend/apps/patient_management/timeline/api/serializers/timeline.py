"""
Serializers for the Timeline module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.timeline.models import PatientTimelineEvent

WRITE_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "event_type",
    "title",
    "description",
    "occurred_at",
    "visibility",
    "reference_type",
    "reference_id",
    "created_by",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "id",
    "organization",
    "patient",
    "event_type",
    "title",
    "description",
    "occurred_at",
    "visibility",
    "reference_type",
    "reference_id",
    "created_by",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "id",
    "patient",
    "event_type",
    "title",
    "occurred_at",
    "visibility",
    "is_active",
)

READ_ONLY_FIELDS: tuple[str, ...] = (
    "id",
    "created_at",
    "updated_at",
)


class PatientTimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTimelineEvent
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientTimelineEventCreateSerializer(
    PatientTimelineEventSerializer,
):
    class Meta(PatientTimelineEventSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientTimelineEventUpdateSerializer(
    PatientTimelineEventSerializer,
):
    class Meta(PatientTimelineEventSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientTimelineEventListSerializer(
    PatientTimelineEventSerializer,
):
    class Meta(PatientTimelineEventSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


PatientTimelineEventDetailSerializer = PatientTimelineEventSerializer


__all__ = [
    "PatientTimelineEventCreateSerializer",
    "PatientTimelineEventDetailSerializer",
    "PatientTimelineEventListSerializer",
    "PatientTimelineEventSerializer",
    "PatientTimelineEventUpdateSerializer",
]
