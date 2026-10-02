"""Patient Document creation serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.constants import (
    PatientDocumentCategory,
)


class PatientDocumentCreateSerializer(
    serializers.Serializer,
):
    """Validate Patient Document creation input."""

    patient_id = serializers.UUIDField()
    title = serializers.CharField(
        max_length=255,
    )
    storage_key = serializers.CharField(
        max_length=500,
    )
    category = serializers.ChoiceField(
        choices=PatientDocumentCategory.choices,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    original_filename = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    mime_type = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )
    file_size = serializers.IntegerField(
        min_value=0,
        required=False,
        default=0,
    )
    checksum = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    is_confidential = serializers.BooleanField(
        required=False,
        default=False,
    )
    metadata = serializers.JSONField(
        required=False,
        default=dict,
    )


__all__ = ("PatientDocumentCreateSerializer",)
