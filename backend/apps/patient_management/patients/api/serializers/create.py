"""
Patient creation serializer.

Validation and payload preparation only.

Patient creation is performed by PatientCreationWorkflow.
"""

from __future__ import annotations

from apps.patient_management.patients.api.serializers.base import (
    PatientBaseSerializer,
)


class PatientCreateSerializer(PatientBaseSerializer):
    """
    Validate Patient creation input.

    The organization is explicitly supplied so the workflow can enforce
    tenant and organization boundaries.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = (
            "organization",
            "mrn",
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
            "middle_name": {
                "required": False,
                "allow_blank": True,
            },
            "preferred_name": {
                "required": False,
                "allow_blank": True,
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


__all__ = ("PatientCreateSerializer",)
