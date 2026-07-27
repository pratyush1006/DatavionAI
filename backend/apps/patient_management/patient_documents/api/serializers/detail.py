"""
Detail serializer for Patient Documents.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


class PatientDocumentDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for retrieving patient document details.
    """

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = PatientDocument

        fields = (
            "id",
            "organization",
            "organization_name",
            "patient",
            "patient_name",
            "document_number",
            "title",
            "description",
            "category",
            "source",
            "status",
            "visibility",
            "storage_backend",
            "current_version",
            "tags",
            "expires_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields
