"""
List serializer for Patient Consents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.consents.models import Consent

__all__ = [
    "ConsentListSerializer",
]


class ConsentListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing consents.
    """

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

    class Meta:
        model = Consent

        fields = (
            "id",
            "consent_number",
            "patient_name",
            "title",
            "consent_type",
            "consent_type_display",
            "status",
            "status_display",
            "version",
            "effective_date",
            "expiry_date",
            "is_required",
            "is_active",
        )
