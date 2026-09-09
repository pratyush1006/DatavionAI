"""
Serializer for updating patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.constants import (
    ContactPurpose,
    ContactType,
)
from apps.patient_management.contacts.models import Contact


class ContactUpdateSerializer(serializers.ModelSerializer):
    """
    Validate mutable patient contact fields.

    The following fields are intentionally excluded from generic update:

    - organization: immutable ownership boundary
    - patient: immutable patient relationship
    - status: lifecycle/verification workflow
    - source: immutable provenance
    - is_primary: dedicated set-primary workflow

    Lifecycle mutations must use their dedicated workflow endpoints.
    """

    contact_type = serializers.ChoiceField(
        choices=ContactType.choices,
        required=False,
    )

    purpose = serializers.ChoiceField(
        choices=ContactPurpose.choices,
        required=False,
    )

    class Meta:
        model = Contact

        fields = (
            "contact_type",
            "purpose",
            "value",
            "is_preferred",
        )

    def validate_value(
        self,
        value: str,
    ) -> str:
        """
        Normalize and validate the contact value.
        """

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Contact value cannot be empty.",
            )

        return value


__all__ = ("ContactUpdateSerializer",)
