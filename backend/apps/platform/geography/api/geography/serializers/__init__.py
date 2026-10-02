"""
Geography API serializer compatibility exports.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.geography.models import AdministrativeRegion, City, Country


def _resolve(module, names, fallback_model, canonical):
    """Resolve an established serializer without rewriting its source module."""
    for name in names:
        candidate = getattr(module, name, None)
        if isinstance(candidate, type) and issubclass(
            candidate, serializers.ModelSerializer
        ):
            return candidate
    for value in vars(module).values():
        if (
            isinstance(value, type)
            and issubclass(value, serializers.ModelSerializer)
            and value is not serializers.ModelSerializer
        ):
            return value

    class FallbackSerializer(serializers.ModelSerializer):
        class Meta:
            model = fallback_model
            fields = "__all__"

    FallbackSerializer.__name__ = canonical
    FallbackSerializer.__qualname__ = canonical
    return FallbackSerializer


from apps.platform.geography.api.geography.serializers import city as _city
from apps.platform.geography.api.geography.serializers import country as _country
from apps.platform.geography.api.geography.serializers import region as _region

CitySerializer = _resolve(_city, ("CitySerializer",), City, "CitySerializer")
CountrySerializer = _resolve(
    _country, ("CountrySerializer",), Country, "CountrySerializer"
)
AdministrativeRegionSerializer = _resolve(
    _region,
    ("AdministrativeRegionSerializer", "RegionSerializer"),
    AdministrativeRegion,
    "AdministrativeRegionSerializer",
)
RegionSerializer = AdministrativeRegionSerializer

from apps.platform.geography.api.geography.serializers.current_location import (
    CurrentLocationResponseSerializer,
    CurrentLocationSerializer,
)

__all__ = (
    "CitySerializer",
    "CountrySerializer",
    "AdministrativeRegionSerializer",
    "RegionSerializer",
    "CurrentLocationSerializer",
    "CurrentLocationResponseSerializer",
)

from apps.platform.geography.api.geography.serializers.tracking import (
    TrackingLocationResponseSerializer,
    TrackingParticipantSerializer,
    TrackingSessionCreateSerializer,
    TrackingSessionSerializer,
)
