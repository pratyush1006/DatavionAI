"""
Tenant list serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.tenancy.models import (
    Tenant,
)


class TenantListSerializer(
    serializers.ModelSerializer,
):
    """
    Tenant list response.
    """

    class Meta:
        model = Tenant

        fields = (
            "id",
            "name",
            "slug",
            "tenant_type",
            "status",
        )


__all__ = ("TenantListSerializer",)
