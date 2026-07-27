"""
Detail serializers for the Patient Preferences module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)


class PatientPreferenceDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Detail serializer.
    """

    class Meta:
        model = PatientPreference

        fields = "__all__"

        read_only_fields = (
            "id",
            "uuid",
            "created_at",
            "updated_at",
        )


class PatientCommunicationPreferenceDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Detail serializer.
    """

    class Meta:
        model = PatientCommunicationPreference

        fields = "__all__"

        read_only_fields = (
            "id",
            "uuid",
            "created_at",
            "updated_at",
        )
