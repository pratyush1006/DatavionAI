"""
Country API serializer.
"""

from __future__ import annotations

from rest_framework.serializers import ModelSerializer

from apps.platform.geography.models import Country


class CountrySerializer(
    ModelSerializer,
):
    """
    Read-only country representation used by platform APIs.
    """

    class Meta:
        model = Country

        fields = (
            "id",
            "code",
            "name",
            "iso3",
            "phone_code",
        )

        read_only_fields = fields


__all__: tuple[str, ...] = ("CountrySerializer",)
