"""
Tenant detail serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.tenancy.models import (
    Tenant,
)


class TenantDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Tenant representation.
    """

    class Meta:
        model = Tenant

        fields = (
            "id",
            "name",
            "slug",
            "tenant_type",
            "status",
            "created_at",
            "updated_at",
        )


__all__ = ("TenantDetailSerializer",)
