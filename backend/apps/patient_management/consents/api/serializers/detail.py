"""
Detail serializer for Patient Consents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.consents.models import Consent

__all__ = [
    "ConsentDetailSerializer",
]


class ConsentDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Detailed serializer for a consent.
    """

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    consent_type_display = serializers.CharField(
        source="get_consent_type_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    method_display = serializers.CharField(
        source="get_method_display",
        read_only=True,
    )

    source_display = serializers.CharField(
        source="get_source_display",
        read_only=True,
    )

    class Meta:
        model = Consent

        fields = "__all__"
