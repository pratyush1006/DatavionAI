"""
Patient update serializer.

Only mutable Patient profile fields are exposed.

Lifecycle fields are deliberately excluded and must be changed through
their dedicated workflows.
"""

from __future__ import annotations

from apps.patient_management.patients.api.serializers.base import (
    PatientBaseSerializer,
)


class PatientUpdateSerializer(PatientBaseSerializer):
    """
    Validate Patient profile updates.

    Status, organization, MRN, and is_active cannot be changed through
    the generic update endpoint.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "preferred_name",
            "date_of_birth",
            "gender",
            "marital_status",
            "blood_group",
            "phone",
            "email",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
        )

        extra_kwargs = {
            "first_name": {
                "required": False,
            },
            "middle_name": {
                "required": False,
                "allow_blank": True,
            },
            "last_name": {
                "required": False,
            },
            "preferred_name": {
                "required": False,
                "allow_blank": True,
            },
            "date_of_birth": {
                "required": False,
            },
            "gender": {
                "required": False,
            },
            "marital_status": {
                "required": False,
                "allow_blank": True,
            },
            "blood_group": {
                "required": False,
                "allow_blank": True,
            },
            "phone": {
                "required": False,
                "allow_blank": True,
            },
            "email": {
                "required": False,
                "allow_blank": True,
            },
            "address": {
                "required": False,
                "allow_blank": True,
            },
            "city": {
                "required": False,
                "allow_blank": True,
            },
            "state": {
                "required": False,
                "allow_blank": True,
            },
            "country": {
                "required": False,
                "allow_blank": True,
            },
            "postal_code": {
                "required": False,
                "allow_blank": True,
            },
        }


__all__ = ("PatientUpdateSerializer",)
