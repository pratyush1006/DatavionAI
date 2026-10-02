"""Patient Document update serializer."""

from __future__ import annotations

from rest_framework import serializers


class PatientDocumentUpdateSerializer(
    serializers.Serializer,
):
    """Validate mutable Patient Document fields."""

    title = serializers.CharField(
        max_length=255,
        required=False,
    )
    category = serializers.CharField(
        max_length=40,
        required=False,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    is_confidential = serializers.BooleanField(
        required=False,
    )
    metadata = serializers.JSONField(
        required=False,
    )


__all__ = ("PatientDocumentUpdateSerializer",)
