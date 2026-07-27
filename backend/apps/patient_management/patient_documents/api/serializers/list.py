"""
List serializer for Patient Documents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


class PatientDocumentListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing patient documents.
    """

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    class Meta:
        model = PatientDocument

        fields = (
            "id",
            "document_number",
            "title",
            "patient",
            "patient_name",
            "category",
            "status",
            "visibility",
            "current_version",
            "created_at",
        )

        read_only_fields = fields
