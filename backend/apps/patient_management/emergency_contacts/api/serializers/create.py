"""
Serializer for creating patient emergency contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency_contacts.constants import (
    PreferredContactMethod,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)


class EmergencyContactCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Write serializer for EmergencyContact creation.

    Organization, status, verification state, and the generated
    emergency contact number are backend-controlled.
    """

    patient_id = serializers.UUIDField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = EmergencyContact

        fields = (
            "patient_id",
            "first_name",
            "middle_name",
            "last_name",
            "relationship",
            "date_of_birth",
            "mobile_number",
            "alternate_mobile_number",
            "home_phone",
            "work_phone",
            "email",
            "preferred_contact_method",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_primary",
            "priority_order",
            "availability",
            "is_legal_guardian",
            "has_medical_power_of_attorney",
            "notes",
        )

    def validate_email(
        self,
        value: str,
    ) -> str:
        return value.strip().lower()

    def validate(
        self,
        attrs: dict,
    ) -> dict:
        preferred_method = attrs.get(
            "preferred_contact_method",
            PreferredContactMethod.MOBILE,
        )

        has_channel = any(
            (
                attrs.get("mobile_number"),
                attrs.get("alternate_mobile_number"),
                attrs.get("home_phone"),
                attrs.get("work_phone"),
                attrs.get("email"),
            )
        )

        if not has_channel:
            raise serializers.ValidationError(
                {"contact": ("At least one emergency contact channel is required.")}
            )

        channel_available = {
            PreferredContactMethod.MOBILE: bool(attrs.get("mobile_number")),
            PreferredContactMethod.HOME_PHONE: bool(attrs.get("home_phone")),
            PreferredContactMethod.WORK_PHONE: bool(attrs.get("work_phone")),
            PreferredContactMethod.EMAIL: bool(attrs.get("email")),
            PreferredContactMethod.SMS: bool(attrs.get("mobile_number")),
            PreferredContactMethod.WHATSAPP: bool(attrs.get("mobile_number")),
            PreferredContactMethod.ANY: has_channel,
        }

        if not channel_available.get(
            preferred_method,
            False,
        ):
            raise serializers.ValidationError(
                {
                    "preferred_contact_method": (
                        "The selected preferred contact method "
                        "does not have a corresponding contact "
                        "detail."
                    )
                }
            )

        return attrs


__all__ = ("EmergencyContactCreateSerializer",)
