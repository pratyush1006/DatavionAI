"""
Create serializers for the Patient Preferences module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)
from apps.patient_management.preferences.services import (
    create_communication_preference,
    create_patient_preference,
)


class PatientPreferenceCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating patient preferences.
    """

    class Meta:
        model = PatientPreference

        fields = (
            "organization",
            "patient",
            "language",
            "timezone",
            "preferred_name",
            "portal_theme",
            "appointment_reminder",
            "accessibility_mode",
            "ai_personalization",
            "data_sharing_consent",
            "status",
        )

    def create(
        self,
        validated_data,
    ) -> PatientPreference:
        return create_patient_preference(
            **validated_data,
        )


class PatientCommunicationPreferenceCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating communication preferences.
    """

    class Meta:
        model = PatientCommunicationPreference

        fields = (
            "organization",
            "patient",
            "channel",
            "priority",
            "enabled",
            "appointment_notifications",
            "clinical_notifications",
            "laboratory_notifications",
            "radiology_notifications",
            "pharmacy_notifications",
            "billing_notifications",
            "insurance_notifications",
            "marketing_notifications",
            "emergency_notifications",
            "ai_assistant_notifications",
        )

    def create(
        self,
        validated_data,
    ) -> PatientCommunicationPreference:
        return create_communication_preference(
            **validated_data,
        )
