"""
Serializer for listing patient emergency contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)


class EmergencyContactListSerializer(
    serializers.ModelSerializer,
):
    """
    Lightweight read representation for emergency contact lists.
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
            "mobile_number",
            "alternate_mobile_number",
            "home_phone",
            "work_phone",
            "email",
            "preferred_contact_method",
            "is_primary",
            "priority_order",
            "availability",
            "status",
            "is_verified",
            "is_legal_guardian",
            "has_medical_power_of_attorney",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = ("EmergencyContactListSerializer",)
