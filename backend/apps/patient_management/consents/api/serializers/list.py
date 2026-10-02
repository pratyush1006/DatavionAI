"""
Patient Consent list serializer.
"""

from __future__ import annotations

from apps.patient_management.consents.api.serializers.base import (
    PatientConsentBaseSerializer,
)


class PatientConsentListSerializer(
    PatientConsentBaseSerializer,
):
    """
    Serialize Patient Consent records for collection endpoints.
    """

    class Meta(PatientConsentBaseSerializer.Meta):
        """
        Configure list serializer fields.
        """

        fields = (
            "id",
            "patient",
            "purpose",
            "status",
            "granted_at",
            "revoked_at",
            "expires_at",
            "version",
            "created_at",
        )


__all__ = ("PatientConsentListSerializer",)
