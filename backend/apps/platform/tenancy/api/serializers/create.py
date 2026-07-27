"""
Tenant creation serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.tenancy.constants import (
    TenantType,
)


class TenantCreateSerializer(
    serializers.Serializer,
):
    """
    Create tenant payload.
    """

    name = serializers.CharField(
        max_length=255,
    )

    slug = serializers.SlugField(
        max_length=100,
    )

    tenant_type = serializers.ChoiceField(
        choices=TenantType.choices,
        default=TenantType.CLINIC,
    )


__all__ = ("TenantCreateSerializer",)
