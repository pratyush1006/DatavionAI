"""
Serializer for retrieving patient emergency contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)


class EmergencyContactDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Detailed read representation of a patient emergency contact.

    This serializer is read-only and contains no mutation behavior.
    """

    patient_id = serializers.UUIDField(
        source="patient_id",
        read_only=True,
    )

    organization_id = serializers.UUIDField(
        source="organization_id",
        read_only=True,
    )

    class Meta:
        model = EmergencyContact

        fields = (
            "id",
            "organization_id",
            "patient_id",
            "emergency_contact_number",
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
            "status",
            "is_verified",
            "verified_at",
            "verified_by",
            "is_legal_guardian",
            "has_medical_power_of_attorney",
            "notes",
            "created_at",
            "updated_at",
            "deleted_at",
        )

        read_only_fields = fields


__all__ = ("EmergencyContactDetailSerializer",)
