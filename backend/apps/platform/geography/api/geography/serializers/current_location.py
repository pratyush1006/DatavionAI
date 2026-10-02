"""
Serializers for the one-time current-location endpoint.
"""

from __future__ import annotations

from rest_framework import serializers


class CurrentLocationSerializer(serializers.Serializer):
    """Validate browser/device coordinates."""

    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        min_value=-90,
        max_value=90,
    )
    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        min_value=-180,
        max_value=180,
    )
    accuracy_meters = serializers.FloatField(
        required=False,
        allow_null=True,
        min_value=0,
    )


class CurrentLocationResponseSerializer(serializers.Serializer):
    """Canonical reverse-geocoding response."""

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    accuracy_meters = serializers.FloatField(allow_null=True)
    formatted_address = serializers.CharField(allow_blank=True)
    country = serializers.CharField(allow_blank=True)
    country_code = serializers.CharField(allow_blank=True)
    state = serializers.CharField(allow_blank=True)
    district = serializers.CharField(allow_blank=True)
    city = serializers.CharField(allow_blank=True)
    postal_code = serializers.CharField(allow_blank=True)
    timezone = serializers.CharField(required=False, allow_blank=True, default="")
    provider = serializers.CharField()
    reference = serializers.DictField()
