"""
Serializer for creating patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.constants import (
    ContactPurpose,
    ContactSource,
    ContactType,
)
from apps.patient_management.contacts.models import Contact


class ContactCreateSerializer(serializers.ModelSerializer):
    """
    Validate API input for patient contact creation.

    Organization ownership is resolved from the authenticated request
    context and is never accepted from the client.

    Contact lifecycle status is controlled by the domain model/workflow.

    Source provenance is assigned automatically as API and cannot be
    spoofed by the caller.
    """

    patient_id = serializers.UUIDField(
        write_only=True,
        required=True,
    )

    contact_type = serializers.ChoiceField(
        choices=ContactType.choices,
        required=True,
    )

    purpose = serializers.ChoiceField(
        choices=ContactPurpose.choices,
        required=False,
        default=ContactPurpose.PRIMARY,
    )

    source = serializers.HiddenField(
        default=ContactSource.API,
    )

    is_primary = serializers.BooleanField(
        required=False,
        default=False,
    )

    is_preferred = serializers.BooleanField(
        required=False,
        default=False,
    )

    class Meta:
        model = Contact

        fields = (
            "patient_id",
            "contact_type",
            "purpose",
            "value",
            "source",
            "is_primary",
            "is_preferred",
        )

    def validate_value(
        self,
        value: str,
    ) -> str:
        """
        Normalize and validate that the contact value is non-empty.

        Type-specific validation is enforced by the Contact domain model
        and service layer.
        """

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Contact value cannot be empty.",
            )

        return value


__all__ = ("ContactCreateSerializer",)
