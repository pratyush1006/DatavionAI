"""
Patient Consent creation serializer.

Validation and payload preparation only.

Patient Consent creation is performed by PatientConsentCreationWorkflow.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.consents.api.serializers.base import (
    PatientConsentBaseSerializer,
)
from apps.patient_management.consents.constants import (
    ConsentPurpose,
)
from apps.patient_management.consents.validators import (
    validate_consent_dates,
    validate_consent_notes,
)


class PatientConsentCreateSerializer(
    PatientConsentBaseSerializer,
):
    """
    Validate Patient Consent creation input.
    """

    class Meta(PatientConsentBaseSerializer.Meta):
        """
        Configure creation serializer fields.
        """

        fields = (
            "organization",
            "patient",
            "purpose",
            "expires_at",
            "notes",
            "version",
            "evidence_reference",
        )
        extra_kwargs = {
            "organization": {
                "required": True,
            },
            "patient": {
                "required": True,
            },
            "purpose": {
                "required": True,
            },
        }

    def validate_purpose(
        self,
        value,
    ):
        """
        Validate the requested consent purpose.
        """
        if value not in ConsentPurpose.values:
            raise serializers.ValidationError(
                "Unsupported consent purpose.",
            )
        return value

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
        Validate consent date relationships.
        """
        validate_consent_dates(
            expires_at=attrs.get(
                "expires_at",
            ),
        )
        return attrs


__all__ = ("PatientConsentCreateSerializer",)
