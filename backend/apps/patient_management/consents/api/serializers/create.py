"""
Create serializer for Patient Consents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.consents.models import Consent
from apps.patient_management.consents.services import (
    create_consent,
)

__all__ = [
    "ConsentCreateSerializer",
]


class ConsentCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating a consent.
    """

    class Meta:
        model = Consent

        exclude = (
            "id",
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data,
    ):
        return create_consent(
            **validated_data,
        )
