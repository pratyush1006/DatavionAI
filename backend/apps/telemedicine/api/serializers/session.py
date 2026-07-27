"""
Telemedicine session serializers.
"""

from __future__ import annotations

from typing import Final

from rest_framework import serializers

from apps.telemedicine.models import TelemedicineSession
from apps.telemedicine.services import SessionService


class TelemedicineSessionBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared normalization logic for session serializers.
    """

    class Meta:
        model = TelemedicineSession
        fields: tuple[str, ...] = ()

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        """
        Normalize a text value.
        """

        return value.strip()


LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "session_id",
    "patient",
    "provider",
    "status",
    "session_type",
    "scheduled_start",
    "scheduled_end",
    "actual_start",
    "actual_end",
    "recording_consent",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "session_id",
    "organization",
    "patient",
    "provider",
    "appointment",
    "status",
    "session_type",
    "scheduled_start",
    "scheduled_end",
    "actual_start",
    "actual_end",
    "connection_url",
    "connection_id",
    "recording_url",
    "recording_consent",
    "notes",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "patient",
    "provider",
    "appointment",
    "scheduled_start",
    "scheduled_end",
    "session_type",
    "connection_url",
    "connection_id",
    "recording_url",
    "recording_consent",
    "notes",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "scheduled_start",
    "scheduled_end",
    "status",
    "session_type",
    "connection_url",
    "connection_id",
    "recording_url",
    "recording_consent",
    "notes",
)

READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "session_id",
    "actual_start",
    "actual_end",
    "created_at",
    "updated_at",
)


class TelemedicineSessionListSerializer(
    TelemedicineSessionBaseSerializer,
):
    """
    Serializer used for listing sessions.
    """

    class Meta(TelemedicineSessionBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class TelemedicineSessionDetailSerializer(
    TelemedicineSessionBaseSerializer,
):
    """
    Serializer used for retrieving session details.
    """

    class Meta(TelemedicineSessionBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class TelemedicineSessionCreateSerializer(
    TelemedicineSessionBaseSerializer,
):
    """
    Serializer used for creating sessions.
    """

    class Meta(TelemedicineSessionBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a session.
        """

        return SessionService.create(
            validated_data=validated_data,
        )


class TelemedicineSessionUpdateSerializer(
    TelemedicineSessionBaseSerializer,
):
    """
    Serializer used for updating sessions.
    """

    class Meta(TelemedicineSessionBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: TelemedicineSession,
        validated_data: dict[str, object],
    ) -> TelemedicineSession:
        """
        Update a session.
        """

        return SessionService.update(
            instance=instance,
            validated_data=validated_data,
        )


class TelemedicineSessionSerializer(
    TelemedicineSessionBaseSerializer,
):
    """
    Generic session serializer.
    """

    class Meta(TelemedicineSessionBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "READ_ONLY_FIELDS",
    "UPDATE_FIELDS",
    "WRITE_FIELDS",
    "TelemedicineSessionBaseSerializer",
    "TelemedicineSessionCreateSerializer",
    "TelemedicineSessionDetailSerializer",
    "TelemedicineSessionListSerializer",
    "TelemedicineSessionSerializer",
    "TelemedicineSessionUpdateSerializer",
]
