"""Serializers for Patient Document access audit records."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocumentAccessLog,
)


class PatientDocumentAccessLogSerializer(
    serializers.ModelSerializer,
):
    """Serialize immutable document access audit records."""

    class Meta:
        """Serializer metadata."""

        model = PatientDocumentAccessLog
        fields = (
            "id",
            "patient_document",
            "user",
            "action",
            "accessed_at",
            "ip_address",
            "user_agent",
            "metadata",
        )
        read_only_fields = fields


__all__ = ("PatientDocumentAccessLogSerializer",)
