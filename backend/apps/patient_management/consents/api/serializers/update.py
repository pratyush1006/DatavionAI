"""
Patient Consent update serializer.

Lifecycle fields remain workflow-controlled.
"""

from __future__ import annotations

from apps.patient_management.consents.api.serializers.base import (
    PatientConsentBaseSerializer,
)
from apps.patient_management.consents.validators import (
    validate_consent_dates,
    validate_consent_notes,
)


class PatientConsentUpdateSerializer(
    PatientConsentBaseSerializer,
):
    """
    Validate mutable Patient Consent fields.
    """

    class Meta(PatientConsentBaseSerializer.Meta):
        """
        Configure update serializer fields.
        """

        fields = (
            "purpose",
            "expires_at",
            "notes",
            "version",
            "evidence_reference",
        )

    def validate_notes(
        self,
        value,
    ):
        """
        Validate and normalize consent notes.
        """
        return validate_consent_notes(
            value,
        )

    def validate(
        self,
        attrs,
    ):
        """
        Validate update-side consent dates.
        """
        validate_consent_dates(
            expires_at=attrs.get(
                "expires_at",
            ),
        )
        return attrs


__all__ = ("PatientConsentUpdateSerializer",)
