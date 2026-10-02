"""Patient Preferences API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.preferences.constants import PreferenceChannel
from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)


class PatientPreferenceListSerializer(serializers.ModelSerializer):
    """Serialize preferences for collection responses."""

    class Meta:
        """Serializer configuration."""

        model = PatientPreference
        fields = (
            "id",
            "patient",
            "organization",
            "language",
            "timezone",
            "date_format",
            "time_format",
            "is_active",
            "created_at",
            "updated_at",
        )


class PatientPreferenceDetailSerializer(serializers.ModelSerializer):
    """Serialize a complete patient preference."""

    communication_preferences = serializers.SerializerMethodField()

    class Meta:
        """Serializer configuration."""

        model = PatientPreference
        fields = (
            "id",
            "patient",
            "organization",
            "language",
            "timezone",
            "date_format",
            "time_format",
            "accessibility",
            "notification_preferences",
            "communication_preferences",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_communication_preferences(self, obj):
        """Return channel preference data."""

        queryset = obj.communication_preferences.filter(is_deleted=False)
        return PatientCommunicationPreferenceSerializer(
            queryset,
            many=True,
        ).data


class PatientPreferenceCreateSerializer(serializers.Serializer):
    """Validate patient preference creation payloads."""

    patient_id = serializers.UUIDField()
    language = serializers.CharField(required=False)
    timezone = serializers.CharField(required=False)
    date_format = serializers.CharField(required=False)
    time_format = serializers.CharField(required=False)
    accessibility = serializers.JSONField(required=False)
    notification_preferences = serializers.JSONField(required=False)


class PatientPreferenceUpdateSerializer(serializers.Serializer):
    """Validate patient preference update payloads."""

    language = serializers.CharField(required=False)
    timezone = serializers.CharField(required=False)
    date_format = serializers.CharField(required=False)
    time_format = serializers.CharField(required=False)
    accessibility = serializers.JSONField(required=False)
    notification_preferences = serializers.JSONField(required=False)


class PatientCommunicationPreferenceSerializer(serializers.ModelSerializer):
    """Serialize one communication channel preference."""

    class Meta:
        """Serializer configuration."""

        model = PatientCommunicationPreference
        fields = (
            "id",
            "channel",
            "enabled",
            "appointment_reminders",
            "clinical_updates",
            "administrative_updates",
            "marketing_messages",
            "is_active",
        )


class PatientCommunicationPreferenceRequestSerializer(serializers.Serializer):
    """Validate communication preference mutation payloads."""

    channel = serializers.ChoiceField(
        choices=[item.value for item in PreferenceChannel],
    )
    enabled = serializers.BooleanField(required=False)
    appointment_reminders = serializers.BooleanField(required=False)
    clinical_updates = serializers.BooleanField(required=False)
    administrative_updates = serializers.BooleanField(required=False)
    marketing_messages = serializers.BooleanField(required=False)


__all__ = (
    "PatientCommunicationPreferenceRequestSerializer",
    "PatientCommunicationPreferenceSerializer",
    "PatientPreferenceCreateSerializer",
    "PatientPreferenceDetailSerializer",
    "PatientPreferenceListSerializer",
    "PatientPreferenceUpdateSerializer",
)
