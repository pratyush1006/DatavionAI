"""
City API serializer.
"""

from __future__ import annotations

from rest_framework.serializers import ModelSerializer

from apps.platform.geography.models import City


class CitySerializer(
    ModelSerializer,
):
    """
    Read-only city representation.

    Country and region identifiers are exposed so consumers can
    maintain the Geography hierarchy without additional requests.
    """

    class Meta:
        model = City

        fields = (
            "id",
            "country",
            "region",
            "name",
            "latitude",
            "longitude",
            "timezone",
        )

        read_only_fields = fields


__all__: tuple[str, ...] = ("CitySerializer",)
