"""
Create serializer for Patient Documents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.services import (
    create_patient_document,
)


class PatientDocumentCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating patient documents.
    """

    class Meta:
        model = PatientDocument

        fields = (
            "organization",
            "patient",
            "document_number",
            "title",
            "description",
            "category",
            "source",
            "visibility",
            "storage_backend",
            "tags",
            "expires_at",
        )

    def create(
        self,
        validated_data,
    ):
        """
        Create a patient document.
        """

        return create_patient_document(
            **validated_data,
        )
