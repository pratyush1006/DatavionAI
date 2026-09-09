"""
Serializer for updating patient emergency contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)


class EmergencyContactUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Write serializer for mutable emergency contact fields.

    Lifecycle state, verification, primary designation,
    organization, patient association, and generated identifiers
    are managed by dedicated workflows.
    """

    class Meta:
        model = EmergencyContact

        fields = (
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
            "priority_order",
            "availability",
            "is_legal_guardian",
            "has_medical_power_of_attorney",
            "notes",
        )

        extra_kwargs = {
            field: {
                "required": False,
            }
            for field in fields
        }

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize email before passing data to the workflow.
        """

        return value.strip().lower()


__all__ = ("EmergencyContactUpdateSerializer",)
