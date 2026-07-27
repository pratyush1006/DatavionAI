"""
Update serializer for Patient Documents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.services import (
    update_patient_document,
)


class PatientDocumentUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating patient documents.
    """

    class Meta:
        model = PatientDocument

        fields = (
            "title",
            "description",
            "category",
            "visibility",
            "tags",
            "expires_at",
            "status",
        )

    def update(
        self,
        instance,
        validated_data,
    ):
        """
        Update a patient document.
        """

        return update_patient_document(
            document=instance,
            **validated_data,
        )
