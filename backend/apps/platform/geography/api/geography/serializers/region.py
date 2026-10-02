"""
Administrative region API serializer.
"""

from __future__ import annotations

from rest_framework.serializers import ModelSerializer

from apps.platform.geography.models import AdministrativeRegion


class AdministrativeRegionSerializer(
    ModelSerializer,
):
    """
    Read-only administrative region representation.
    """

    class Meta:
        model = AdministrativeRegion

        fields = (
            "id",
            "country",
            "code",
            "name",
            "region_type",
        )

        read_only_fields = fields


__all__: tuple[str, ...] = ("AdministrativeRegionSerializer",)
