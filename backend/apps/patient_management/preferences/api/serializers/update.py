"""
Update serializers for the Patient Preferences module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)
from apps.patient_management.preferences.services import (
    update_communication_preference,
    update_patient_preference,
)


class PatientPreferenceUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Update serializer.
    """

    class Meta:
        model = PatientPreference

        exclude = (
            "id",
            "uuid",
            "organization",
            "patient",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance,
        validated_data,
    ):
        return update_patient_preference(
            preference=instance,
            **validated_data,
        )


class PatientCommunicationPreferenceUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Update serializer.
    """

    class Meta:
        model = PatientCommunicationPreference

        exclude = (
            "id",
            "uuid",
            "organization",
            "patient",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance,
        validated_data,
    ):
        return update_communication_preference(
            preference=instance,
            **validated_data,
        )
