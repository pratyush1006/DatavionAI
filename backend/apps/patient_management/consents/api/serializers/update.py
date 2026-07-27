"""
Update serializer for Patient Consents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.consents.models import Consent
from apps.patient_management.consents.services import (
    update_consent,
)

__all__ = [
    "ConsentUpdateSerializer",
]


class ConsentUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating a consent.
    """

    class Meta:
        model = Consent

        exclude = (
            "id",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance,
        validated_data,
    ):
        return update_consent(
            consent=instance,
            **validated_data,
        )
