"""Patient Communication creation serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationCreateSerializer(serializers.ModelSerializer):
    """Validate Patient Communication creation payloads."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = (
            "organization",
            "patient",
            "channel",
            "direction",
            "communication_type",
            "subject",
            "content",
            "external_reference",
            "occurred_at",
            "metadata",
        )


__all__ = ("CommunicationCreateSerializer",)
