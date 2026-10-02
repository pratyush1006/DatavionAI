"""
Patient Consent detail serializer.
"""

from __future__ import annotations

from apps.patient_management.consents.api.serializers.base import (
    PatientConsentBaseSerializer,
)


class PatientConsentDetailSerializer(
    PatientConsentBaseSerializer,
):
    """
    Serialize a complete Patient Consent representation.
    """

    class Meta(PatientConsentBaseSerializer.Meta):
        """
        Configure detail serializer fields.
        """

        fields = PatientConsentBaseSerializer.Meta.fields


__all__ = ("PatientConsentDetailSerializer",)
