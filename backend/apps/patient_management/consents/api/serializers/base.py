"""
Base Patient Consent serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.consents.models import (
    PatientConsent,
)


class PatientConsentBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Common serialization contract for Patient Consents.
    """

    class Meta:
        """
        Configure shared Patient Consent serializer fields.
        """

        model = PatientConsent
        fields = (
            "id",
            "organization",
            "patient",
            "purpose",
            "status",
            "granted_at",
            "revoked_at",
            "expires_at",
            "granted_by",
            "notes",
            "version",
            "evidence_reference",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "granted_at",
            "revoked_at",
            "granted_by",
            "created_at",
            "updated_at",
        )


__all__ = ("PatientConsentBaseSerializer",)
