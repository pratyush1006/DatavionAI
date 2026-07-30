"""
Serializers for the Communication module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import (
    PatientCommunication,
)

WRITE_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "channel",
    "direction",
    "status",
    "subject",
    "message",
    "recipient",
    "sent_at",
    "read_at",
    "template",
    "reference_id",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "id",
    "organization",
    "patient",
    "channel",
    "direction",
    "status",
    "subject",
    "message",
    "recipient",
    "sent_at",
    "read_at",
    "template",
    "reference_id",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "id",
    "patient",
    "channel",
    "direction",
    "status",
    "subject",
    "sent_at",
    "is_active",
)

READ_ONLY_FIELDS: tuple[str, ...] = (
    "id",
    "created_at",
    "updated_at",
)


class PatientCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCommunication
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientCommunicationCreateSerializer(
    PatientCommunicationSerializer,
):
    class Meta(PatientCommunicationSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientCommunicationUpdateSerializer(
    PatientCommunicationSerializer,
):
    class Meta(PatientCommunicationSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientCommunicationListSerializer(
    PatientCommunicationSerializer,
):
    class Meta(PatientCommunicationSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


PatientCommunicationDetailSerializer = PatientCommunicationSerializer


__all__ = [
    "PatientCommunicationCreateSerializer",
    "PatientCommunicationDetailSerializer",
    "PatientCommunicationListSerializer",
    "PatientCommunicationSerializer",
    "PatientCommunicationUpdateSerializer",
]
