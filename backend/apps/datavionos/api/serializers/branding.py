"""
Platform branding serializer.
"""

from __future__ import annotations

from rest_framework import serializers


class BrandingSerializer(serializers.Serializer):
    """
    Serializer for platform branding.
    """

    application_name = serializers.CharField()

    organization_name = serializers.CharField()

    logo = serializers.CharField(
        allow_null=True,
        required=False,
    )

    favicon = serializers.CharField(
        allow_null=True,
        required=False,
    )

    primary_color = serializers.CharField()

    secondary_color = serializers.CharField()

    theme = serializers.CharField()


__all__ = [
    "BrandingSerializer",
]
