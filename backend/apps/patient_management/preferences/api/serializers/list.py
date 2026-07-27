"""
List serializers for the Patient Preferences module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)


class PatientPreferenceListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing patient preferences.
    """

    class Meta:
        model = PatientPreference

        fields = (
            "uuid",
            "patient",
            "language",
            "timezone",
            "portal_theme",
            "status",
        )

        read_only_fields = fields


class PatientCommunicationPreferenceListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing communication preferences.
    """

    class Meta:
        model = PatientCommunicationPreference

        fields = (
            "uuid",
            "channel",
            "priority",
            "enabled",
        )

        read_only_fields = fields
